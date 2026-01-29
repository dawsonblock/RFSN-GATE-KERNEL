"""A simple driver to tick the thalamic gate and update the CGW state."""

from __future__ import annotations

from typing import Optional

from .event_bus import SimpleEventBus
from .thalamic_gate import ThalamusGate
from .cgw_state import CGWRuntime
from .types import Candidate, ForcedCandidate, SelfModel, SelectionReason


class Runtime:
    """Drive the thalamic gate and CGW state one cycle at a time."""

    def __init__(self, gate: ThalamusGate, cgw: CGWRuntime, self_model_provider: Optional[callable] = None) -> None:
        self.gate = gate
        self.cgw = cgw
        self.self_model_provider = self_model_provider or (lambda: SelfModel())

    def tick(self) -> bool:
        """Execute one decision cycle. Returns True if a winner was selected."""
        winner, reason = self.gate.select_winner()
        if winner is None:
            return False
        self_model = self.self_model_provider()
        self.cgw.update(winner, reason, self_model)
        return True
