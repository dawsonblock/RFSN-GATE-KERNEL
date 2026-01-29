# RFSN-GATE-KERNEL

**Conscious Global Workspace (CGW) - Serial Decision Architecture for Autonomous Coding**

A self-contained Python library implementing the CGW serial decision architecture with learning, memory, and event persistence.

## Core Features

| Feature | Component | Description |
|:---|:---|:---|
| 🧠 **Serial Decision Loop** | `ThalamusGate` | Exactly one decision per cycle |
| 🎰 **Strategy Bandit** | `CGWBandit` | Thompson Sampling learns optimal actions |
| 🛡️ **Regression Firewall** | `CGWActionMemory` | Blocks consistently failing approaches |
| 📊 **Event Persistence** | `CGWEventStore` | SQLite-backed logging for replay |
| 🐳 **Docker Sandbox** | `DockerSandbox` | Isolated code execution |

## Architecture

```
┌─────────────────────────────────────────────────┐
│              IntegratedCGWAgent                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┐    ┌─────────────┐            │
│  │  Proposals  │───▶│ ThalamusGate│───▶ Winner │
│  │ (Generators)│    │   (Gate)    │            │
│  └─────────────┘    └─────────────┘            │
│         │                  │                    │
│         ▼                  ▼                    │
│  ┌─────────────┐    ┌─────────────┐            │
│  │  CGWBandit  │    │  CGWRuntime │            │
│  │  (Learning) │    │   (State)   │            │
│  └─────────────┘    └─────────────┘            │
│         │                  │                    │
│         ▼                  ▼                    │
│  ┌─────────────┐    ┌─────────────┐            │
│  │ActionMemory │    │  Executor   │            │
│  │ (Firewall)  │    │ (Blocking)  │            │
│  └─────────────┘    └─────────────┘            │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Installation

```bash
# Basic install
pip install -e .

# With Docker support
pip install -e ".[docker]"

# With LLM support (OpenAI/DeepSeek)
pip install -e ".[llm]"

# Everything
pip install -e ".[all]"
```

## Quick Start

```python
from cgw_standalone.core import SimpleEventBus, ThalamusGate, CGWRuntime, Candidate
from cgw_standalone.agent import CGWBandit, CGWActionMemory, CGWEventStore

# Create components
event_bus = SimpleEventBus()
gate = ThalamusGate(event_bus)
cgw = CGWRuntime(event_bus)

# Learning + Memory (persists to ~/.cgw/)
bandit = CGWBandit()       # Thompson Sampling
memory = CGWActionMemory()  # Regression firewall
events = CGWEventStore()    # Event persistence

# Submit candidates
gate.submit_candidate(Candidate(
    slot_id="fix_1",
    source_module="patch_gen",
    content_payload=b"fix code",
    saliency=0.8,
    urgency=0.5,
))

# Select winner (serial guarantee)
winner, reason = gate.select_winner()
```

## Data Persistence

All learning persists across sessions:

| Component | Database | Default Location |
|:---|:---|:---|
| Bandit | SQLite | `~/.cgw/bandit.db` |
| Memory | SQLite | `~/.cgw/memory.db` |
| Events | SQLite | `~/.cgw/events.db` |

## Key Invariants

1. **Serial Execution**: Exactly one decision per cycle
2. **Forced Override**: Safety signals bypass competition
3. **Atomic State**: CGW uses swap-on-write
4. **Learning Contained**: Bandits influence *what*, never *how*

## License

MIT
