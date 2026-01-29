"""Monitoring utilities for the CGW/SSL guard runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class SerialityMonitor:
    """Track the number of commits per cycle to detect parallelism."""
    commits_per_cycle: Dict[int, int] = field(default_factory=dict)

    def on_commit(self, event: Dict) -> None:
        cycle_id = event.get("cycle_id")
        if cycle_id is not None:
            self.commits_per_cycle[cycle_id] = self.commits_per_cycle.get(cycle_id, 0) + 1

    def has_violations(self) -> bool:
        """Check if any cycle had more than one commit."""
        return any(count > 1 for count in self.commits_per_cycle.values())
