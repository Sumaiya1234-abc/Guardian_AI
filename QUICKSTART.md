# GuardianAI Quick Start Guide

## Installation (2 minutes)

```bash
# Navigate to project
cd c:\Users\hp\Desktop\guardianai

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from guardianai import FraudDetectionEnv; print('✓ Ready!')"
```

## Running Your First Example (1 minute)

```bash
python examples/quickstart.py
```

Output:
```
🎯 GUARDIANAI FRAUD DETECTION - QUICK START
✓ Environment created!
✓ Episode started!
✓ Detector created!
Processing 100 transactions...
Accuracy: 87%
...
✅ Quick start complete!
```

## Understanding the Output

After running, you'll see metrics:

- **Accuracy**: % of correct fraud/legitimate decisions
- **Frauds Caught**: Number of actual frauds detected
- **False Positives**: Legitimate transactions flagged as fraud
- **Precision**: Accuracy of fraud predictions (when we say fraud, how often right?)
- **Fraud Detection Rate**: % of actual frauds we caught

## 5-Minute Hands-On Example

```python
from guardianai import FraudDetectionEnv

# 1. Create environment with 100 accounts
env = FraudDetectionEnv(
    num_accounts=100,
    fraud_rate=0.05,        # 5% fraud
    difficulty="easy",      # Start easy
    max_episode_length=200
)

# 2. Start episode
observation, info = env.reset()

# 3. Simple fraud detection rule
done = False
while not done:
    # If amount is very unusual, flag as fraud
    decision = 1 if observation["amount_zscore"][0] > 2 else 0
    
    # Tell environment our decision
    observation, reward, terminated, truncated, info = env.step(decision)
    done = terminated or truncated

# 4. See results
summary = env.get_episode_summary()
print(f"Accuracy: {summary['accuracy']:.1%}")
print(f"Caught {summary['frauds_caught']} frauds")
```

## Available Examples

### 1. **quickstart.py** ⚡ (Start here!)
   - Simplest possible example
   - Shows basic environment usage
   - Takes < 1 minute
   ```bash
   python examples/quickstart.py
   ```

### 2. **basic_usage.py** 📖
   - Detailed tutorial
   - Multiple difficulty levels
   - Custom agent example
   ```bash
   python examples/basic_usage.py
   ```

### 3. **agent_evaluation.py** 📊
   - Compare different agents
   - Performance metrics
   - Benchmarking
   ```bash
   python examples/agent_evaluation.py
   ```

### 4. **advanced_learning.py** 🧠
   - Machine learning integration
   - Online learning agents
   - Feature importance analysis
   ```bash
   python examples/advanced_learning.py
   ```

## Fraud Types You'll See

The environment simulates 8 real fraud patterns:

1. **Amount Anomaly** - Unusually large transaction (easy to detect)
2. **Geographic Fraud** - Transaction from distant location
3. **Velocity Fraud** - Many transactions in short time
4. **Unusual Merchant** - Transaction with high-risk merchant
5. **Account Compromise** - Multiple fraud indicators together
6. **Test Transaction** - Small test then large transaction
7. **Synthetic Identity** - Completely fake account
8. **Fraud Ring** - Coordinated fraud across accounts

## Key Concepts

### Observations (Input)
Your agent observes transaction details:
```python
observation = {
    "amount_zscore": [2.5],           # Amount very unusual
    "transactions_last_1h": [8.0],    # 8 transactions recently
    "new_merchant": [1.0],            # First time merchant
    "is_international": [1.0],        # International transaction
    # ... more features
}
```

### Decisions (Output)
Your agent decides:
```python
decision = 0  # Predict LEGITIMATE
decision = 1  # Predict FRAUDULENT
```

### Rewards
Environment returns feedback:
```python
observation, reward, terminated, truncated, info = env.step(decision)
# reward: Positive for correct predictions, negative for wrong
# info: Ground truth and transaction details
```

## Common Patterns to Try

### Pattern 1: Rule-Based Detection
```python
def detector(observation):
    if observation["amount_zscore"][0] > 2:
        return 1
    elif observation["transactions_last_1h"][0] > 8:
        return 1
    return 0
```

### Pattern 2: Risk Scoring
```python
def detector(observation):
    risk = 0
    if observation["amount_zscore"][0] > 1.5:
        risk += 0.3
    if observation["new_merchant"][0]:
        risk += 0.2
    if observation["is_international"][0]:
        risk += 0.2
    return 1 if risk > 0.5 else 0
```

### Pattern 3: Weighted Combination
```python
def detector(observation):
    score = (
        0.3 * max(0, observation["amount_zscore"][0] / 3) +
        0.3 * (observation["transactions_last_1h"][0] / 20) +
        0.2 * observation["new_merchant"][0] +
        0.2 * observation["is_international"][0]
    )
    return 1 if score > 0.5 else 0
```

## Performance Tips

### Get Better Accuracy
1. Use multiple features (not just amount)
2. Adjust thresholds based on difficulty
3. Consider feature interactions
4. Look for pattern combinations

### Run Faster
```python
env = FraudDetectionEnv(
    num_accounts=10,       # Reduce accounts
    max_episode_length=50  # Shorter episodes
)
```

### See More Detail
```python
env.render_mode = "console"
env.render()  # Between steps
```

## Next Steps

1. ✅ **Run quickstart.py** - Get comfortable
2. 📖 **Study basic_usage.py** - Understand patterns
3. 🧪 **Modify examples** - Change rules and parameters
4. 📚 **Read docs/AGENT_DEVELOPMENT.md** - Create sophisticated agents
5. 🤖 **Build your own agent** - Implement your logic
6. 📊 **Compare approaches** - Use evaluation script

## Documentation

- **API_REFERENCE.md** - Complete API documentation
- **AGENT_DEVELOPMENT.md** - How to build agents
- **FRAUD_PATTERNS.md** - Detailed fraud descriptions
- **SETUP.md** - Installation and configuration

## Troubleshooting

### ImportError: No module named 'guardianai'
```bash
# Run from project root
cd c:\Users\hp\Desktop\guardianai
python -c "from guardianai import FraudDetectionEnv; print('✓')"
```

### Module not found errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Need more help?
1. Check example files
2. Review test files (tests/test_environment.py)
3. Read the documentation
4. Try the basic usage example

## Environment Difficulties

Choose based on your needs:

### **easy** ⭐
- Obvious fraud patterns
- Large amount deviations
- High velocity
- Best for: Testing, learning
- Expected accuracy: 70-90%

### **medium** ⭐⭐
- Realistic patterns
- Subtle deviations
- Mixed indicators
- Best for: Real development
- Expected accuracy: 50-75%

### **hard** ⭐⭐⭐
- Sophisticated fraud
- Minimal indicators
- Requires ML models
- Best for: Advanced agents
- Expected accuracy: 30-60%

## Ready? Start Here! 🚀

```bash
cd c:\Users\hp\Desktop\guardianai
python examples/quickstart.py
```

Enjoy building your fraud detector! 🎯
