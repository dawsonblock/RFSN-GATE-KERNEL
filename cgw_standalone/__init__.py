"""CGW Standalone - Serial Decision Architecture for Autonomous Coding.

This package provides the Conscious Global Workspace (CGW) implementation
with all Phase 2 features:
- Strategy Bandit (learning between sessions)
- Action Outcome Memory (regression firewall)
- Persistent Event Logging

Quick Start:
    from cgw_standalone import IntegratedCGWAgent

    agent = IntegratedCGWAgent(goal="Fix failing tests")
    result = agent.run()
    print(result.summary())
"""

# Core exports
from cgw_standalone.core import (
    SimpleEventBus,
    ThalamusGate,
    Candidate,
    ForcedCandidate,
    SelectionReason,
    CGWRuntime,
    CGWState,
    AttendedContent,
    CausalTrace,
    SelfModel,
    Runtime,
    SerialityMonitor,
)

# Agent exports
from cgw_standalone.agent import (
    IntegratedCGWAgent,
    CodingAgentRuntime,
    AgentConfig,
    AgentResult,
    CodingAction,
    BlockingExecutor,
    CGWBandit,
    CGWActionMemory,
    CGWEventStore,
    CGWConfig,
    load_config,
)

__version__ = "1.0.0"
__all__ = [
    # Core
    "SimpleEventBus",
    "ThalamusGate",
    "Candidate",
    "ForcedCandidate",
    "SelectionReason",
    "CGWRuntime",
    "CGWState",
    "AttendedContent",
    "CausalTrace",
    "SelfModel",
    "Runtime",
    "SerialityMonitor",
    # Agent
    "IntegratedCGWAgent",
    "CodingAgentRuntime",
    "AgentConfig",
    "AgentResult",
    "CodingAction",
    "BlockingExecutor",
    "CGWBandit",
    "CGWActionMemory",
    "CGWEventStore",
    "CGWConfig",
    "load_config",
]
