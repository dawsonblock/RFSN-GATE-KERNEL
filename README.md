# RFSN-GATE-KERNEL

<p align="center">
  <strong>Conscious Global Workspace (CGW) — Serial Decision Architecture for Autonomous Coding</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#features">Features</a> •
  <a href="#api-reference">API</a>
</p>

---

## Overview

A self-contained Python library implementing the **CGW serial decision architecture** — a control-first approach to autonomous coding agents that guarantees:

- ✅ **Exactly one decision per cycle** (no race conditions)
- ✅ **Forced overrides** for safety-critical signals
- ✅ **Learning confined to proposal space** (bandits influence *what*, not *how*)
- ✅ **Full auditability** via persistent event logging

## Features

| Component | Purpose | Persistence |
|:---|:---|:---|
| 🧠 **ThalamusGate** | Arbitrates between competing proposals | — |
| 🎰 **CGWBandit** | Thompson Sampling strategy selection | `~/.cgw/bandit.db` |
| 🛡️ **CGWActionMemory** | Regression firewall blocks failing patterns | `~/.cgw/memory.db` |
| 📊 **CGWEventStore** | Event logging for replay & debugging | `~/.cgw/events.db` |
| 🐳 **DockerSandbox** | Isolated code execution | — |
| 🤖 **LLM Integration** | DeepSeek/OpenAI/Gemini for patch generation | — |

## Installation

```bash
# Clone the repository
git clone https://github.com/dawsonblock/RFSN-GATE-KERNEL.git
cd RFSN-GATE-KERNEL

# Basic install
pip install -e .

# With Docker sandbox support
pip install -e ".[docker]"

# With LLM support (OpenAI/DeepSeek)
pip install -e ".[llm]"

# Everything
pip install -e ".[all]"
```

**Requirements:** Python 3.9+

## Quick Start

```python
from cgw_standalone.core import SimpleEventBus, ThalamusGate, CGWRuntime, Candidate
from cgw_standalone.agent import CGWBandit, CGWActionMemory

# Initialize core components
event_bus = SimpleEventBus()
gate = ThalamusGate(event_bus)
cgw = CGWRuntime(event_bus)

# Initialize learning (persists to ~/.cgw/)
bandit = CGWBandit()        # Learns optimal action selection
memory = CGWActionMemory()   # Blocks consistently failing actions

# Submit a proposal
gate.submit_candidate(Candidate(
    slot_id="patch_001",
    source_module="llm_generator",
    content_payload=b'{"action": "apply_patch", "diff": "..."}',
    saliency=0.85,
    urgency=0.3,
    surprise=0.1,
))

# Gate selects winner (exactly one per cycle)
winner, reason = gate.select_winner()
print(f"Winner: {winner.slot_id}, Reason: {reason}")
```

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     Serial Decision Cycle                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐                                               │
│   │   Forced     │──────────────────────┐                        │
│   │   Queue      │ (safety bypass)      │                        │
│   └──────────────┘                      ▼                        │
│                                  ┌─────────────┐                 │
│   ┌──────────────┐               │             │                 │
│   │  Proposals   │──────────────▶│   THALAMUS  │──▶ Winner       │
│   │ (generators) │  competition  │    GATE     │                 │
│   └──────────────┘               │             │                 │
│         │                        └─────────────┘                 │
│         │ saliency boost              │                          │
│         │                             ▼                          │
│   ┌─────┴────────┐              ┌─────────────┐                  │
│   │  CGWBandit   │              │  CGWRuntime │                  │
│   │  (Thompson)  │              │   (atomic   │                  │
│   └──────────────┘              │    state)   │                  │
│         │                             │                          │
│         │ blocked?                    ▼                          │
│         │                       ┌─────────────┐                  │
│   ┌─────┴────────┐              │  Blocking   │                  │
│   │ ActionMemory │              │  Executor   │                  │
│   │ (firewall)   │              │  (serial)   │                  │
│   └──────────────┘              └─────────────┘                  │
│                                       │                          │
│                                       ▼                          │
│                               ┌─────────────┐                    │
│                               │ EventStore  │                    │
│                               │ (persist)   │                    │
│                               └─────────────┘                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Decision Cycle

1. **Collect** — Generators submit `Candidate` proposals
2. **Gate** — `ThalamusGate` selects winner (forced signals first, then by score)
3. **Commit** — Winner committed to `CGWRuntime` (atomic swap)
4. **Execute** — `BlockingExecutor` runs action synchronously
5. **Learn** — Outcome recorded to `CGWBandit` and `CGWActionMemory`

## API Reference

### Core Components

| Class | Description |
|:---|:---|
| `SimpleEventBus` | Pub/sub event system |
| `ThalamusGate` | Decision gate with forced override |
| `CGWRuntime` | Atomic state management |
| `Candidate` | Proposal with saliency/urgency/surprise |
| `ForcedCandidate` | Bypass candidate (safety signals) |

### Agent Components

| Class | Description |
|:---|:---|
| `CGWBandit` | Thompson Sampling for action selection |
| `CGWActionMemory` | Similarity-based memory + regression firewall |
| `CGWEventStore` | SQLite event persistence |
| `BlockingExecutor` | Serial action execution |
| `CodingAgentRuntime` | Full decision loop orchestration |

### Key Methods

```python
# Gate operations
gate.submit_candidate(candidate)           # Submit for competition
gate.inject_forced_signal(source, payload) # Bypass competition
winner, reason = gate.select_winner()      # Select winner

# Bandit learning
bandit.select_action(method="thompson")    # Pick action type
bandit.update(action_type, reward)         # Record outcome
bandit.get_saliency_boost(action_type)     # Get learned boost

# Memory operations
memory.is_blocked(action_type, action_key) # Check firewall
memory.record_outcome(...)                 # Store result
priors = memory.get_action_priors(context) # Similarity lookup

# Event persistence
events.record(event_type, data)            # Log event
events.get_session_events(session_id)      # Query events
events.export_jsonl(path)                  # Export for analysis
```

## Configuration

Create `cgw.yaml` in your working directory:

```yaml
agent:
  max_cycles: 100
  max_patches: 10
  total_timeout: 3600.0

bandit:
  enabled: true
  exploration_bonus: 0.1

memory:
  enabled: true
  regression_threshold: 0.2

event_store:
  enabled: true
  db_path: ~/.cgw/events.db
```

## Key Invariants

| Invariant | Enforcement |
|:---|:---|
| **Serial execution** | `BlockingExecutor` + `_is_executing` flag |
| **Atomic state** | `CGWRuntime` uses swap-on-write |
| **Forced override** | `ThalamusGate` checks forced queue first |
| **Learning containment** | Bandits only adjust saliency, never execute |

## Project Structure

```
cgw_standalone/
├── core/                 # Base CGW library
│   ├── event_bus.py      # Pub/sub events
│   ├── thalamic_gate.py  # Decision gate
│   ├── cgw_state.py      # Atomic state
│   ├── types.py          # Dataclasses
│   └── monitors.py       # Seriality checks
│
├── agent/                # Coding agent
│   ├── integrated_runtime.py  # Full agent
│   ├── cgw_bandit.py          # Thompson Sampling
│   ├── action_memory.py       # Regression firewall
│   ├── event_store.py         # Persistence
│   ├── executor.py            # Blocking execution
│   └── proposal_generators.py # Action proposals
│
└── examples/
    └── basic_usage.py    # Quick start
```

## License

MIT

---

<p align="center">
  <sub>Built with the RFSN Framework</sub>
</p>
