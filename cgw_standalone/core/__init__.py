"""Core CGW components."""

from .event_bus import SimpleEventBus
from .types import (
    Candidate,
    ForcedCandidate,
    SelectionReason,
    SelectionEvent,
    CGWState,
    CausalTrace,
    AttendedContent,
    SelfModel,
)
from .thalamic_gate import ThalamusGate
from .cgw_state import CGWRuntime
from .runtime import Runtime
from .monitors import SerialityMonitor

__all__ = [
    "SimpleEventBus",
    "ThalamusGate",
    "Candidate",
    "ForcedCandidate",
    "SelectionReason",
    "SelectionEvent",
    "CGWRuntime",
    "CGWState",
    "CausalTrace",
    "AttendedContent",
    "SelfModel",
    "Runtime",
    "SerialityMonitor",
]
