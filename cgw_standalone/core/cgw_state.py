"""Implementation of the conscious global workspace state (CGW).

The state is immutable once created: each update constructs a new
CGWState object and swaps it into place atomically.
"""

from __future__ import annotations

import hashlib
import time
from typing import Optional, Union

from .event_bus import SimpleEventBus
from .types import (
    AttendedContent,
    Candidate,
    CGWState,
    CausalTrace,
    ForcedCandidate,
    SelectionReason,
    SelfModel,
)


class CGWRuntime:
    """Manage the current CGW state and commit new states atomically."""

    def __init__(self, event_bus: SimpleEventBus) -> None:
        self.event_bus = event_bus
        self.current_state: Optional[CGWState] = None
        self.cycle_counter: int = 0

    def update(self, winner: Union[ForcedCandidate, Candidate], reason: SelectionReason, self_model: SelfModel) -> CGWState:
        """Commit a new CGWState based on the winning signal."""
        self.cycle_counter += 1
        now = time.time()

        slot_id = winner.slot_id
        payload = winner.content_payload
        source = winner.source_module
        forced = isinstance(winner, ForcedCandidate)
        winner_score = winner.score() if isinstance(winner, Candidate) else None
        payload_hash = hashlib.sha256(payload).hexdigest()
        
        attended = AttendedContent(
            slot_id=slot_id,
            payload_hash=payload_hash,
            payload_bytes=payload,
            source_module=source,
            timestamp=now,
        )
        trace = CausalTrace(
            winner_reason=reason,
            winner_score=winner_score,
            losers=[],
            forced_override=forced,
        )
        new_state = CGWState(
            cycle_id=self.cycle_counter,
            timestamp=now,
            attended_content=attended,
            causal_trace=trace,
            self_model=self_model,
        )
        # Atomic swap
        self.current_state = new_state
        # Emit commit event
        self.event_bus.emit("CGW_COMMIT", {
            "cycle_id": new_state.cycle_id,
            "slot_id": new_state.content_id(),
            "reason": reason.value,
            "forced": forced,
            "timestamp": now,
        })
        return new_state

    def get_current_state(self) -> Optional[CGWState]:
        return self.current_state
