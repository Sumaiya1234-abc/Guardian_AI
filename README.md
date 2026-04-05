# GuardianAI - Fraud Detection Environment

A real-world OpenEnv environment for AI agents to detect fraudulent behavior in digital transactions. The environment simulates banking and UPI transactions with realistic fraud patterns.

## Features

- **Realistic Transaction Simulation**: Models banking and UPI transaction patterns
- **Multi-dimensional Fraud**:
  - Unusual transaction amounts
  - Anomalous merchant behavior
  - Geographic inconsistencies
  - Account compromise patterns
  - Coordinated fraud rings
  - Behavioral deviations

- **Real-time Agent Interaction**: Agents receive transaction data and must make fraud/legitimate decisions
- **Scalable Design**: Handle hundreds to millions of simulated transactions
- **Configurable Difficulty**: Adjust fraud complexity and subtlety levels

## Environment Architecture

```
GuardianAI Environment
├── Transaction Generator (simulates real banking patterns)
├── Fraud Injector (adds realistic fraud patterns)
├── Agent Interface (OpenEnv-based interaction)
├── State Management (tracks account & transaction history)
├── Reward System (feedback on decisions)
└── Monitoring & Metrics (performance tracking)
```

## Quick Start

```python
from guardianai import FraudDetectionEnv

# Initialize environment
env = FraudDetectionEnv(
    num_accounts=1000,
    fraud_rate=0.05,
    difficulty='medium'
)

# Reset and get initial state
state = env.reset()

# Agent decision loop
while not done:
    action = agent.decide(state)  # 0=legitimate, 1=fraudulent
    state, reward, done, info = env.step(action)
```

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

- `guardianai/` - Core environment package
- `agents/` - Example agent implementations
- `notebooks/` - Jupyter notebooks for exploration
- `tests/` - Unit tests
- `examples/` - Usage examples
- `data/` - Sample datasets

## Documentation

See `docs/` for detailed documentation on:
- Environment API reference
- Transaction patterns
- Reward function specification
- Agent development guide
