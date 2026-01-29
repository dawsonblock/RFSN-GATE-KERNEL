"""CGW Coding Agent module.

This module provides the integrated coding agent with all Phase 2 features.
"""

from .action_types import CodingAction, ActionPayload, ExecutionResult, CycleResult
from .coding_agent_runtime import CodingAgentRuntime, AgentConfig, AgentResult
from .integrated_runtime import IntegratedCGWAgent, run_agent
from .executor import BlockingExecutor, ExecutorConfig
from .cgw_bandit import CGWBandit, CGWBanditConfig, get_cgw_bandit
from .action_memory import CGWActionMemory, CGWMemoryConfig, get_action_memory
from .event_store import CGWEventStore, EventStoreConfig, StoredEvent
from .config import CGWConfig, load_config
from .proposal_generators import (
    ProposalContext,
    ProposalGenerator,
    SafetyProposalGenerator,
    PlannerProposalGenerator,
    MemoryProposalGenerator,
    AnalyzerProposalGenerator,
    IdleProposalGenerator,
)

__all__ = [
    # Actions
    "CodingAction",
    "ActionPayload",
    "ExecutionResult",
    "CycleResult",
    # Runtime
    "CodingAgentRuntime",
    "AgentConfig",
    "AgentResult",
    "IntegratedCGWAgent",
    "run_agent",
    # Executor
    "BlockingExecutor",
    "ExecutorConfig",
    # Learning
    "CGWBandit",
    "CGWBanditConfig",
    "get_cgw_bandit",
    "CGWActionMemory",
    "CGWMemoryConfig",
    "get_action_memory",
    # Events
    "CGWEventStore",
    "EventStoreConfig",
    "StoredEvent",
    # Config
    "CGWConfig",
    "load_config",
    # Generators
    "ProposalContext",
    "ProposalGenerator",
    "SafetyProposalGenerator",
    "PlannerProposalGenerator",
    "MemoryProposalGenerator",
    "AnalyzerProposalGenerator",
    "IdleProposalGenerator",
]
