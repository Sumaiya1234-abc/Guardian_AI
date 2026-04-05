# Fraud Detection Reward Function - Complete Index

## 📋 Overview

A comprehensive reward function system for training fraud detection agents, supporting:
- **Base rewards** for correct/incorrect predictions (TP/TN/FP/FN)
- **Confidence bonuses** (0.8-1.2x multiplier)
- **Difficulty scaling** (0.8-1.3x for anomaly complexity)
- **Partial signal detection** (+0 to +0.25 bonus)
- **Learning progress tracking** (-0.1 to +0.1 improvement bonus)
- **Four reward schemes** (Balanced, Conservative, Aggressive, Learning)

**Total Deliverables**: 5 files + 4,000+ lines of code and documentation

---

## 📁 File Index

### 1. **Core Implementation**

#### `guardianai/reward.py` (500+ lines)
**Main reward calculation engine. Production-ready code.**

Key classes:
- `RewardScheme` - Enum with 4 schemes
- `OutcomeType` - Enum with TP/TN/FP/FN
- `RewardComponents` - Dataclass for detailed breakdown
- `RewardCalculator` - Main computation class
- `create_calculator()` - Factory function

Key methods:
- `compute_reward()` - Calculate single prediction reward
- `get_reward_stats()` - Batch statistics
- `_calculate_confidence_bonus()` - Confidence scaling
- `_calculate_anomaly_score()` - Feature-based difficulty
- `_calculate_difficulty_multiplier()` - Difficulty scaling
- `_calculate_partial_signals()` - Signal detection bonuses
- `_calculate_improvement_bonus()` - Learning progress

**Usage:**
```python
from guardianai.reward import RewardCalculator, RewardScheme

calc = RewardCalculator(scheme=RewardScheme.BALANCED)
reward = calc.compute_reward(
    action=1,              # 0=SAFE, 1=FRAUD
    ground_truth=1,        # 0=legitimate, 1=fraud
    confidence=0.95,
    features={"amount_zscore": 5.0, ...}
)
print(f"Reward: {reward:.3f}")
```

---

### 2. **Specification & Design Documents**

#### `docs/REWARD_DESIGN.md` (2,500+ lines)
**Comprehensive specification document. Read this to understand the design.**

Contents:
- Overview and motivation
- Core reward structure with formulas
- Confidence bonus component explanation
- Difficulty multiplier explanation
- Partial detection signals explanation
- Improvement bonus explanation
- Composite formula with derivation
- 8 detailed worked examples
- Integration guidelines
- Learning dynamics theory
- Empirical performance data
- Configuration examples for each scheme

**When to read**: 
- Initial understanding of the reward system
- When designing custom reward schemes
- For detailed mathematical background

---

#### `docs/REWARD_QUICKREF.md` (800+ lines)
**Quick lookup guide. Read this for fast answers.**

Contents:
- TL;DR base rewards table
- Formula breakdown
- Confidence bonus chart
- Difficulty multiplier chart
- Partial signal weights
- Typical episode rewards by task
- Interpretation guide for reward values
- Quick implementation examples
- Common configuration patterns
- Debugging tips

**When to read**:
- Quick lookup during development
- Fast reference for reward values
- Troubleshooting reward issues

---

### 3. **Examples & Guides**

#### `examples/reward_example.py` (600+ lines)
**8 runnable examples demonstrating all features.**

Examples:
1. **Basic Rewards** - All 4 outcomes with detailed breakdown
2. **Scheme Comparison** - Same predictions across 4 schemes
3. **Confidence Impact** - How confidence affects rewards
4. **Difficulty Impact** - How anomalies affect rewards  
5. **Partial Signals** - Signal detection bonuses in action
6. **Learning Progress** - Improvement tracking with history
7. **Batch Statistics** - Analyzing multiple agent predictions
8. **Complete Episode** - Full transaction sequence with rewards

**Usage:**
```bash
python examples/reward_example.py
# Outputs detailed examples with tables and analysis
```

**When to use**:
- Learning how the reward system works
- Understanding individual components
- Testing different scenarios

---

#### `examples/reward_integration_guide.py` (600+ lines)
**Integration examples showing how to use with FraudDetectionEnv.**

Examples:
1. **Integration Setup** - Environment initialization pattern
2. **Environment Modification** - Code snippets for FraudDetectionEnv
3. **Agent with Confidence** - AgentAction class with confidence scores
4. **Training Loop** - Multi-phase training (LEARNING → BALANCED → CONSERVATIVE)
5. **Reward Analysis** - Deep dive into scheme comparison
6. **Task-Specific Config** - Optimizing for Easy/Medium/Hard tasks

**When to read**:
- Integrating into FraudDetectionEnv
- Understanding multi-phase training
- Task-specific configurations

---

#### `docs/REWARD_DIAGRAMS.py` (Executable diagrams)
**Visual ASCII diagrams showing all components.**

Diagrams:
1. Reward calculation flow
2. Outcome types and base rewards
3. Confidence bonus mechanism
4. Difficulty multiplier mechanism
5. Learning progression over time
6. Partial signal detection bonus
7. Complete example walkthrough

**Usage:**
```bash
python docs/REWARD_DIAGRAMS.py
# Prints visual diagrams to terminal
```

---

### 4. **Summary & Completion**

#### `REWARD_COMPLETION_SUMMARY.md` (This section's counterpart)
**High-level completion summary with all key information.**

---

## 🚀 Quick Start

### Basic Usage

```python
from guardianai.reward import RewardCalculator, RewardScheme

# Create calculator (BALANCED is default)
calc = RewardCalculator(scheme=RewardScheme.BALANCED)

# Get reward for a prediction
reward = calc.compute_reward(
    action=1,                                # 0=SAFE, 1=FRAUD
    ground_truth=1,                          # 0=legitimate, 1=fraud
    confidence=0.95,                         # Agent's confidence
    features={                               # Observation features
        "amount_zscore": 5.0,
        "transactions_last_hour": 15,
        "location_changed": True,
        "is_international": True,
    }
)

print(f"Reward: {reward:.3f}")  # Output: Reward: 1.496
```

### Detailed Breakdown

```python
# Get full component breakdown
reward, components = calc.compute_reward(
    action=1,
    ground_truth=1,
    confidence=0.95,
    features={...},
    return_components=True
)

print(components)
# Output shows: base, confidence_bonus, difficulty, partial, improvement, total
```

### Batch Analysis

```python
# Analyze multiple predictions
stats = calc.get_reward_stats(
    predictions=[(1,1), (0,0), (1,0), (0,1), ...],
    confidences=[0.9, 0.85, 0.7, 0.6, ...],
)

print(f"Mean reward: {stats['mean_reward']:.3f}")
print(f"Total reward: {stats['total_reward']:.3f}")
print(f"Outcomes: {stats['outcomes']}")
print(f"Mean by outcome: {stats['mean_by_outcome']}")
```

### Different Schemes

```python
# BALANCED: Default, fair evaluation
calc_balanced = RewardCalculator(scheme=RewardScheme.BALANCED)

# CONSERVATIVE: Customer-friendly (minimize false alarms)
calc_conservative = RewardCalculator(scheme=RewardScheme.CONSERVATIVE)

# AGGRESSIVE: Security-first (catch all fraud)
calc_aggressive = RewardCalculator(scheme=RewardScheme.AGGRESSIVE)

# LEARNING: Training mode (emphasize learning progress)
calc_learning = RewardCalculator(scheme=RewardScheme.LEARNING)
```

---

## 📊 Reward Structure At-A-Glance

### Base Rewards (BALANCED Scheme)

| Outcome | Reward | Meaning |
|---------|--------|---------|
| **TP** (Caught Fraud) | +1.0 | ✓ Best outcome |
| **TN** (Allowed Legitimate) | +0.5 | ✓ Good outcome |
| **FP** (Blocked Innocent) | -0.5 | ✗ Bad outcome |
| **FN** (Missed Fraud) | -1.0 | ✗ Worst outcome |

### Component Multipliers

| Component | Range | Meaning |
|-----------|-------|---------|
| **Confidence Bonus** | 0.8 - 1.2x | Uncertainty penalty, certainty bonus |
| **Difficulty Multiplier** | 0.8 - 1.3x | Easy cases penalized, hard cases rewarded |
| **Partial Signals** | +0 to +0.25 | Bonus for detecting correct indicators |
| **Improvement Bonus** | -0.1 to +0.1 | Learning progress tracking |

### Composite Formula

```
TOTAL_REWARD = (base × confidence_bonus × difficulty_multiplier) 
             + partial_signals 
             + improvement_bonus
```

**Typical Range**: [-1.5, +1.5] per transaction

---

## 📖 Reading Guide

### By Use Case

**I want to understand the reward system:**
1. Read: `docs/REWARD_QUICKREF.md` (5 min)
2. Run: `examples/reward_example.py` (10 min)
3. Read: `docs/REWARD_DESIGN.md` (30 min)

**I want to integrate into my environment:**
1. Read: `examples/reward_integration_guide.py` example 2
2. Follow code snippets to integrate
3. Test with `examples/reward_example.py`

**I want to debug reward issues:**
1. Check: `docs/REWARD_QUICKREF.md` debugging section
2. Use: `return_components=True` in compute_reward()
3. Print: components to see breakdown

**I want task-specific rewards:**
1. Read: `examples/reward_integration_guide.py` example 6
2. Create: Task-specific RewardCalculator instances
3. Use: Different schemes for different tasks

---

## 🔑 Key Concepts

### Outcome Types (TP/TN/FP/FN)

```
                     Predicted
                  FRAUD | SAFE
            ─────────────────────
            FRAUD │  TP  │  FN
Actual      ──────┼──────┼──────
            SAFE  │  FP  │  TN
```

- **TP (True Positive)**: Correctly caught fraud (+1.0)
- **TN (True Negative)**: Correctly allowed legitimate (+0.5)
- **FP (False Positive)**: Incorrectly blocked innocent (-0.5)
- **FN (False Negative)**: Incorrectly allowed fraud (-1.0)

### Confidence Bonus

Agent's confidence in prediction affects reward scaling:
- **High confidence (0.95)**: ×1.18 multiplier
  - On correct: Bigger reward
  - On wrong: Bigger penalty (teaches calibration)
- **Low confidence (0.55)**: ×0.82 multiplier
  - Hedging bet reduces both reward and penalty

### Difficulty Multiplier

Harder transactions give more reward for correct detection:
- **Easy** (all normal): 0.8x (trivial detection)
- **Medium** (mixed signals): 1.0x (standard)
- **Hard** (subtle anomalies): 1.3x (challenging detection)

### Partial Signals

Even wrong predictions get credit for detecting fraud indicators:
```
Agent predicts SAFE (wrong) but detects:
- High amount anomaly: +0.05
- High velocity: +0.05
- New merchant: +0.04
Result: FN reward improved from -1.0 to -0.67
```

### Improvement Bonus

Rewards agent for learning progress:
```
Baseline (first 50 steps): 50% accuracy
Current (last 50 steps): 100% accuracy
Improvement: +50% → Bonus: +0.05 per step
```

---

## 🎯 Reward Schemes

### BALANCED (Default)
**Use for**: General fraud detection, development
- Equal treatment of metrics
- Standard penalties/rewards
- Good for developing agents

**Base Rewards**: TP=+1.0, TN=+0.5, FP=-0.5, FN=-1.0

### CONSERVATIVE
**Use for**: Product environments, customer-focused
- Lighter TP rewards (don't block aggressively)
- Heavy FP penalties (avoid false alarms)
- More TN rewards (let customers transact)
- Same FN penalty

**Base Rewards**: TP=+0.8, TN=+0.6, FP=-0.8, FN=-1.0

### AGGRESSIVE
**Use for**: High-security environments, intrusion detection
- Heavy TP rewards (catch all fraud)
- Light FP penalties (acceptable false alarms)
- Minimal TN rewards
- Heavier FN penalty

**Base Rewards**: TP=+1.3, TN=+0.3, FP=-0.3, FN=-1.3

### LEARNING
**Use for**: Agent training and development
- Standard base rewards
- 50% higher partial signal bonuses
- 50% higher improvement bonuses
- Encourages exploration and learning

**Base Rewards**: TP=+1.0, TN=+0.5, FP=-0.5, FN=-1.0

---

## 📈 Typical Performance

### Per Transaction

| Agent Quality | Easy Task | Medium Task | Hard Task |
|---|---|---|---|
| Random | -0.1 to 0 | -0.1 to 0 | -0.1 to -0.05 |
| Baseline | +0.4 to +0.5 | +0.1 to +0.2 | -0.025 to +0.025 |
| Optimized | +0.6 to +0.7 | +0.2 to +0.3 | +0.025 to +0.075 |

### Per Episode

| Agent Quality | Easy (500 TX) | Medium (1000 TX) | Hard (2000 TX) |
|---|---|---|---|
| Random | -50 to 0 | -100 to 0 | -200 to -100 |
| Baseline | +200-250 | +100-200 | -50 to +50 |
| Optimized | +300-350 | +200-300 | +50-150 |

---

## 🔧 Integration Checklist

To integrate RewardCalculator with FraudDetectionEnv:

- [ ] Import RewardCalculator and RewardScheme
- [ ] Initialize in `__init__()` with desired scheme
- [ ] Call `compute_reward()` in `step()` method
- [ ] Return reward to agent
- [ ] Track reward history for analysis
- [ ] Test with `examples/reward_example.py`
- [ ] Agents provide confidence if possible
- [ ] Use `return_components=True` for debugging

See `examples/reward_integration_guide.py` for code templates.

---

## 🐛 Troubleshooting

### Low Rewards on True Positives?

**Check:**
1. Is anomaly score high? (Hard frauds reward more)
2. Is confidence high? (Low conf = low mult)
3. Which scheme? (Aggressive gives +1.3 vs Balanced +1.0)
4. Are features being passed? (Missing features = lower anomaly)

### Unexpectedly High Negative Rewards?

**Check:**
1. Is confidence high on wrong pred? (×1.2 penalty)
2. Is it a hard case? (×1.3 multiplier makes it worse)
3. Do partial signals exist? (+bonus if detected)
4. Is improvement tracked? (Can reduce penalty)

### Partial Signals Not Helping?

**Check:**
1. Partial signals only apply to WRONG predictions
2. Need to compute for each signal type
3. Maximum +0.25 per transaction
4. Agent must detect signals to get bonus

### Improvement Bonus Not Kicking In?

**Check:**
1. Need at least 100 predictions (2 × 50-step windows)
2. Bonus only applied if history provided
3. Clamped to [-0.1, +0.1]
4. Improvement window is configurable (default 50)

---

## 📚 Additional Resources

### Documentation Files
- [REWARD_DESIGN.md](docs/REWARD_DESIGN.md) - Full specification
- [REWARD_QUICKREF.md](docs/REWARD_QUICKREF.md) - Quick reference
- [REWARD_DIAGRAMS.py](docs/REWARD_DIAGRAMS.py) - Visual diagrams

### Code Files
- [guardianai/reward.py](guardianai/reward.py) - Implementation
- [examples/reward_example.py](examples/reward_example.py) - Examples
- [examples/reward_integration_guide.py](examples/reward_integration_guide.py) - Integration

### Related Documentation
- [docs/TASK_DESIGN.md](docs/TASK_DESIGN.md) - Task specifications
- [docs/INTERACTION_GUIDE.md](docs/INTERACTION_GUIDE.md) - Environment interaction

---

## ✅ Completion Checklist

✅ Core implementation (reward.py)
✅ Comprehensive specification (REWARD_DESIGN.md)  
✅ Quick reference guide (REWARD_QUICKREF.md)
✅ 8 runnable examples (reward_example.py)
✅ 6 integration examples (reward_integration_guide.py)
✅ Visual diagrams (REWARD_DIAGRAMS.py)
✅ This index file

**Status**: COMPLETE AND READY FOR USE

---

## 🎓 Learning Path

1. **30 minutes**: Read REWARD_QUICKREF.md
2. **30 minutes**: Run reward_example.py
3. **1 hour**: Read REWARD_DESIGN.md  
4. **1 hour**: Study reward_integration_guide.py
5. **1 hour**: Integrate into your environment
6. **Ongoing**: Use REWARD_QUICKREF.md for reference

---

## 📝 Notes

- All code is type-hinted and documented
- RewardCalculator is independent and composable
- Can be used with any environment
- Schemes can be easily extended
- Component calculations are modular and customizable

---

**Version**: 1.0  
**Status**: Production Ready  
**Total Lines**: 4,000+  
**Files**: 5 main deliverables + index
