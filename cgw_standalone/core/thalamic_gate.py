"""Thalamic gate implementation with forced override.

The gate maintains forced_queue (FIFO bypass) and candidates (normal competition).
Forced signals always win. Normal signals compete via score().
"""

from __future__ import annotations

import time
from collections import deque
from typing import List, Optional, Tuple, Union

from .event_bus import SimpleEventBus
from .types import (
    Candidate,
    ForcedCandidate,
    SelectionEvent,
    SelectionReason,
)


class ThalamusGate:
    """Arbitrate between competing signals for CGW admission."""

    def __init__(self, event_bus: SimpleEventBus) -> None:
        self.event_bus = event_bus
        self.forced_queue: deque[ForcedCandidate] = deque()
        self.candidates: List[Candidate] = []
        self.cycle_counter: int = 0
        self.last_selection_time: float = 0.0
        self.max_candidates_per_cycle: int = 20
        self.competition_cooldown_ms: int = 100

    def inject_forced_signal(self, *, source_module: str, content_payload: bytes, reason: str = "FORCED_OVERRIDE") -> str:
        """Inject a forced signal. Returns the assigned slot id."""
        slot_id = f"forced_{int(time.time() * 1e6)}"
        fc = ForcedCandidate(slot_id=slot_id, source_module=source_module, content_payload=content_payload)
        self.forced_queue.append(fc)
        self.event_bus.emit("FORCED_INJECTION", {
            "slot_id": slot_id,
            "source": source_module,
            "timestamp": time.time(),
            "queue_depth": len(self.forced_queue)
        })
        return slot_id

    def submit_candidate(self, candidate: Candidate) -> None:
        """Submit a normal candidate for competition."""
        if len(self.candidates) >= self.max_candidates_per_cycle:
            self.candidates.sort(key=lambda c: c.score(), reverse=True)
            self.candidates = self.candidates[: self.max_candidates_per_cycle]
        self.candidates.append(candidate)

    def select_winner(self) -> Tuple[Optional[Union[ForcedCandidate, Candidate]], SelectionReason]:
        """Select the next winner based on forced queue or scoring."""
        self.cycle_counter += 1
        now = time.time()

        # Forced queue first
        if self.forced_queue:
            fc = self.forced_queue.popleft()
            reason = SelectionReason.FORCED_OVERRIDE
            loser_ids = [c.slot_id for c in self.candidates]
            event = SelectionEvent(
                cycle_id=self.cycle_counter,
                slot_id=fc.slot_id,
                reason=reason,
                timestamp=now,
                forced_queue_size=len(self.forced_queue),
                losers=loser_ids,
                winner_is_forced=True,
            )
            self.event_bus.emit("GATE_SELECTION", event)
            self.candidates.clear()
            return fc, reason

        # Normal competition
        if self.candidates:
            if (now - self.last_selection_time) * 1000 < self.competition_cooldown_ms:
                return None, SelectionReason.COMPETITION
            self.candidates.sort(key=lambda c: c.score(), reverse=True)
            winner = self.candidates[0]
            loser_ids = [c.slot_id for c in self.candidates[1:]]
            if winner.urgency > 0.8:
                reason = SelectionReason.URGENCY
            elif winner.surprise > 0.8:
                reason = SelectionReason.SURPRISE
            else:
                reason = SelectionReason.COMPETITION
            event = SelectionEvent(
                cycle_id=self.cycle_counter,
                slot_id=winner.slot_id,
                reason=reason,
                timestamp=now,
                forced_queue_size=0,
                losers=loser_ids,
                winner_is_forced=False,
            )
            self.event_bus.emit("GATE_SELECTION", event)
            self.candidates.clear()
            self.last_selection_time = now
            return winner, reason

        return None, SelectionReason.COMPETITION
