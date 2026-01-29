#!/usr/bin/env python3
"""Basic usage example for CGW Standalone.

This demonstrates how to use the IntegratedCGWAgent with all Phase 2 features:
- Strategy Bandit (learning between sessions)
- Action Memory (regression firewall)
- Event Logging (persistence for replay)
"""

from cgw_standalone import IntegratedCGWAgent, CGWConfig

def main():
    # Create default config
    config = CGWConfig()
    config.agent.max_cycles = 50
    config.agent.goal = "Fix failing tests"
    
    # Enable all Phase 2 features
    config.bandit.enabled = True
    config.memory.enabled = True
    config.event_store.enabled = True
    
    # Create the integrated agent
    agent = IntegratedCGWAgent(
        config=config,
        goal="Fix failing tests",
    )
    
    print("Starting CGW Agent...")
    print(f"  Max cycles: {config.agent.max_cycles}")
    print(f"  Bandit enabled: {config.bandit.enabled}")
    print(f"  Memory enabled: {config.memory.enabled}")
    print(f"  Events enabled: {config.event_store.enabled}")
    print()
    
    # Run the agent
    # result = agent.run()
    # print(result.summary())
    
    print("Agent initialized successfully!")
    print()
    print("To run with a real repository, use:")
    print("  cgw run --repo https://github.com/user/repo --goal 'Fix failing tests'")

if __name__ == "__main__":
    main()
