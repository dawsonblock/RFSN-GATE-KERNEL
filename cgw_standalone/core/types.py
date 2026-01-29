"""Type definitions and dataclasses for the CGW/SSL guard runtime."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class SelectionReason(Enum):
    """Reason a signal won the thalamic gate."""
    FORCED_OVERRIDE = "FORCED_OVERRIDE"
    COMPETITION = "COMPETITION"
    URGENCY = "URGENCY"
    SURPRISE = "SURPRISE"


@dataclass
class Candidate:
    """A normal signal competing for the workspace."""
    slot_id: str
    source_module: str
    content_payload: bytes
    saliency: float
    urgency: float = 0.0
    surprise: float = 0.0

    def score(self) -> float:
        """Compute a heuristic score: 0.5*saliency + 0.3*urgency + 0.2*surprise."""
        return 0.5 * self.saliency + 0.3 * self.urgency + 0.2 * self.surprise


@dataclass
class ForcedCandidate:
    """A forced signal that bypasses competition entirely."""
    slot_id: str
    source_module: str
    content_payload: bytes


@dataclass
class SelectionEvent:
    """Event emitted when the thalamic gate selects a winner."""
    cycle_id: int
    slot_id: str
    reason: SelectionReason
    timestamp: float
    forced_queue_size: int
    losers: List[str]
    winner_is_forced: bool

    def total_candidates(self) -> int:
        return 1 + len(self.losers)


@dataclass(frozen=True)
class AttendedContent:
    """The single authoritative slot in the CGW."""
    slot_id: str
    payload_hash: str
    payload_bytes: bytes
    source_module: str
    timestamp: float


@dataclass
class CausalTrace:
    """Metadata about the winning selection."""
    winner_reason: SelectionReason
    winner_score: Optional[float]
    losers: List[str] = field(default_factory=list)
    forced_override: bool = False


@dataclass
class SelfModel:
    """Persistent self‑state across cycles."""
    goals: List[str] = field(default_factory=list)
    active_intentions: List[str] = field(default_factory=list)
    confidence_estimates: Dict[str, float] = field(default_factory=dict)

    def delta_magnitude(self, other: SelfModel) -> float:
        """Compute a crude magnitude of change between self models."""
        goal_diff = set(self.goals) ^ set(other.goals)
        intent_diff = set(self.active_intentions) ^ set(other.active_intentions)
        conf_diff_keys = set(self.confidence_estimates).union(other.confidence_estimates)
        conf_diff = sum(abs(self.confidence_estimates.get(k, 0) - other.confidence_estimates.get(k, 0))
                        for k in conf_diff_keys)
        return float(len(goal_diff) + len(intent_diff) + conf_diff)


@dataclass
class CGWState:
    """Complete workspace state for one moment."""
    cycle_id: int
    timestamp: float
    attended_content: AttendedContent
    causal_trace: CausalTrace
    self_model: SelfModel

    def content_id(self) -> str:
        return self.attended_content.slot_id

    def content_hash(self) -> str:
        return self.attended_content.payload_hash
