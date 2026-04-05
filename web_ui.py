#!/usr/bin/env python3
"""
GuardianAI - Web Interface
Research & demonstration interface for fraud detection environment
Shows agent learning through OpenEnv API (no game - purely educational)
"""

import gradio as gr
from guardianai import FraudDetectionEnv
from agents import BalancedAgent, ConservativeAgent, AggressiveAgent
import matplotlib.pyplot as plt
import numpy as np

# Global state
current_env = None
current_agent = None
history = {"steps": [], "rewards": [], "accuracy": []}

def run_single_episode(difficulty, agent_type, num_steps):
    """Run a single episode and return results"""
    try:
        # Create environment
        env = FraudDetectionEnv(
            num_accounts=100,
            difficulty=difficulty,
            max_episode_length=num_steps
        )
        
        # Select agent
        if agent_type == "Conservative":
            agent = ConservativeAgent()
        elif agent_type == "Aggressive":
            agent = AggressiveAgent()
        else:
            agent = BalancedAgent()
        
        # Reset
        observation, info = env.reset()
        
        # Run episode
        done = False
        step = 0
        rewards_list = []
        predictions = []
        ground_truth = []
        
        while not done and step < num_steps:
            action = agent.decide(observation)
            observation, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            
            step += 1
            rewards_list.append(reward)
            predictions.append(action)
            ground_truth.append(1 if info.get("is_fraud_ground_truth", False) else 0)
        
        # Get summary
        summary = env.get_episode_summary()
        
        # Prepare output
        result_text = f"""
**EPISODE RESULTS**

🤖 **Agent**: {agent.name}
📊 **Difficulty**: {difficulty.upper()}
📈 **Steps**: {step}/{num_steps}

**Performance Metrics:**
- Accuracy: {summary['accuracy']:.1%}
- Precision: {summary['precision']:.1%}
- Recall (Fraud Detection Rate): {summary['fraud_detection_rate']:.1%}
- F1-Score: {summary.get('f1_score', 0.0):.1%}

**Results:**
- Total Reward: {sum(rewards_list):+.1f}
- Frauds Detected: {summary.get('frauds_caught', 0)}
- False Positives: {summary.get('false_positives', 0)}
- Correct Predictions: {sum(1 for p, g in zip(predictions, ground_truth) if p == g)}/{len(predictions)}

**Fraud Pattern Distribution:**
- Amount detected as fraud: {len([p for p in predictions if p == 1])}
- Amount detected as legitimate: {len([p for p in predictions if p == 0])}
"""
        
        # Create chart
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        # Rewards over time
        axes[0, 0].plot(rewards_list, linewidth=2, color='blue')
        axes[0, 0].set_title('Reward per Step', fontsize=12, fontweight='bold')
        axes[0, 0].set_xlabel('Step')
        axes[0, 0].set_ylabel('Reward')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Cumulative reward
        cumulative = np.cumsum(rewards_list)
        axes[0, 1].plot(cumulative, linewidth=2, color='green')
        axes[0, 1].set_title('Cumulative Reward', fontsize=12, fontweight='bold')
        axes[0, 1].set_xlabel('Step')
        axes[0, 1].set_ylabel('Total Reward')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Prediction distribution
        pred_fraud = len([p for p in predictions if p == 1])
        pred_legit = len([p for p in predictions if p == 0])
        axes[1, 0].bar(['Fraudulent', 'Legitimate'], [pred_fraud, pred_legit], color=['red', 'green'])
        axes[1, 0].set_title('Predictions Made', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Count')
        
        # Metrics comparison
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        values = [
            summary['accuracy'],
            summary['precision'],
            summary['fraud_detection_rate'],
            summary.get('f1_score', 0.0)
        ]
        axes[1, 1].bar(metrics, values, color=['blue', 'orange', 'green', 'red'])
        axes[1, 1].set_title('Performance Metrics', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Score')
        axes[1, 1].set_ylim([0, 1])
        for i, v in enumerate(values):
            axes[1, 1].text(i, v + 0.02, f'{v:.1%}', ha='center', fontsize=10)
        
        plt.tight_layout()
        
        env.close()
        return result_text, fig
        
    except Exception as e:
        return f"❌ Error: {str(e)}", None

def compare_agents(difficulty, num_steps):
    """Compare all three agent strategies"""
    try:
        agents_list = [
            ("Conservative", ConservativeAgent()),
            ("Balanced", BalancedAgent()),
            ("Aggressive", AggressiveAgent()),
        ]
        
        results = {}
        
        for agent_name, agent in agents_list:
            env = FraudDetectionEnv(
                num_accounts=100,
                difficulty=difficulty,
                max_episode_length=num_steps
            )
            
            observation, info = env.reset()
            done = False
            total_reward = 0.0
            step = 0
            
            while not done:
                action = agent.decide(observation)
                observation, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
                total_reward += reward
                step += 1
            
            summary = env.get_episode_summary()
            results[agent_name] = {
                'accuracy': summary['accuracy'],
                'precision': summary['precision'],
                'recall': summary['fraud_detection_rate'],
                'f1': summary.get('f1_score', 0.0),
                'reward': total_reward,
                'steps': step
            }
            
            env.close()
        
        # Create comparison text
        comparison_text = "**AGENT COMPARISON RESULTS**\n\n"
        comparison_text += f"Difficulty: **{difficulty.upper()}**\n"
        comparison_text += f"Steps: {num_steps}\n\n"
        
        for agent_name, metrics in results.items():
            comparison_text += f"### {agent_name} Agent\n"
            comparison_text += f"- Accuracy: {metrics['accuracy']:.1%}\n"
            comparison_text += f"- Precision: {metrics['precision']:.1%}\n"
            comparison_text += f"- Recall: {metrics['recall']:.1%}\n"
            comparison_text += f"- F1-Score: {metrics['f1']:.1%}\n"
            comparison_text += f"- Total Reward: {metrics['reward']:+.1f}\n\n"
        
        # Ranking
        sorted_by_accuracy = sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True)
        comparison_text += "**Ranking by Accuracy:**\n"
        for rank, (agent_name, metrics) in enumerate(sorted_by_accuracy, 1):
            comparison_text += f"{rank}. **{agent_name}**: {metrics['accuracy']:.1%}\n"
        
        # Create comparison chart
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        agent_names = list(results.keys())
        accuracies = [results[a]['accuracy'] for a in agent_names]
        precisions = [results[a]['precision'] for a in agent_names]
        recalls = [results[a]['recall'] for a in agent_names]
        f1s = [results[a]['f1'] for a in agent_names]
        
        # Accuracy
        axes[0, 0].bar(agent_names, accuracies, color=['red', 'blue', 'green'])
        axes[0, 0].set_title('Accuracy Comparison', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].set_ylim([0, 1])
        for i, v in enumerate(accuracies):
            axes[0, 0].text(i, v + 0.02, f'{v:.1%}', ha='center')
        
        # Precision
        axes[0, 1].bar(agent_names, precisions, color=['red', 'blue', 'green'])
        axes[0, 1].set_title('Precision Comparison', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Precision')
        axes[0, 1].set_ylim([0, 1])
        for i, v in enumerate(precisions):
            axes[0, 1].text(i, v + 0.02, f'{v:.1%}', ha='center')
        
        # Recall
        axes[1, 0].bar(agent_names, recalls, color=['red', 'blue', 'green'])
        axes[1, 0].set_title('Recall (Fraud Detection) Comparison', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Recall')
        axes[1, 0].set_ylim([0, 1])
        for i, v in enumerate(recalls):
            axes[1, 0].text(i, v + 0.02, f'{v:.1%}', ha='center')
        
        # F1-Score
        axes[1, 1].bar(agent_names, f1s, color=['red', 'blue', 'green'])
        axes[1, 1].set_title('F1-Score Comparison', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('F1-Score')
        axes[1, 1].set_ylim([0, 1])
        for i, v in enumerate(f1s):
            axes[1, 1].text(i, v + 0.02, f'{v:.1%}', ha='center')
        
        plt.tight_layout()
        
        return comparison_text, fig
        
    except Exception as e:
        return f"❌ Error: {str(e)}", None

# Create Gradio interface
with gr.Blocks(title="GuardianAI - Fraud Detection Environment") as demo:
    gr.Markdown("""
# 🛡️ GuardianAI - Fraud Detection Environment

**Research interface for OpenEnv fraud detection environment**

This interface demonstrates how agents learn from the environment using standard Gymnasium APIs:
- **reset()** - Initialize episode with random state
- **step(action)** - Agent gets reward feedback for learning
- **observation** - Agent's view of current transaction
- **reward** - Signal for agent to improve

No game mechanics - pure research and educational demonstration.
""")
    
    with gr.Tabs():
        # TAB 1: SINGLE EPISODE
        with gr.Tab("📊 Single Episode"):
            gr.Markdown("""
### Run One Episode
Choose settings and watch an agent run through a fraud detection episode.
""")
            
            with gr.Row():
                difficulty = gr.Dropdown(
                    choices=["easy", "medium", "hard"],
                    value="medium",
                    label="🎯 Difficulty Level",
                    interactive=True
                )
                agent_type = gr.Dropdown(
                    choices=["Conservative", "Balanced", "Aggressive"],
                    value="Balanced",
                    label="🤖 Agent Type",
                    interactive=True
                )
                num_steps = gr.Slider(
                    minimum=50,
                    maximum=500,
                    value=100,
                    step=50,
                    label="📊 Number of Steps",
                    interactive=True
                )
            
            with gr.Row():
                run_btn = gr.Button("▶ Run Episode", size="lg", variant="primary")
                results_text = gr.Markdown()
            
            with gr.Row():
                results_chart = gr.Plot(label="Performance Visualization")
            
            run_btn.click(
                fn=run_single_episode,
                inputs=[difficulty, agent_type, num_steps],
                outputs=[results_text, results_chart],
                api_name="run_episode"
            )
        
        # TAB 2: AGENT COMPARISON
        with gr.Tab("⚖️ Agent Comparison"):
            gr.Markdown("""
### Compare Agent Strategies
Run all three agents side-by-side to see which strategy works best.
""")
            
            with gr.Row():
                cmp_difficulty = gr.Dropdown(
                    choices=["easy", "medium", "hard"],
                    value="medium",
                    label="🎯 Difficulty Level",
                    interactive=True
                )
                cmp_steps = gr.Slider(
                    minimum=50,
                    maximum=300,
                    value=150,
                    step=50,
                    label="📊 Number of Steps",
                    interactive=True
                )
            
            with gr.Row():
                cmp_btn = gr.Button("🔄 Compare Agents", size="lg", variant="primary")
                cmp_text = gr.Markdown()
            
            with gr.Row():
                cmp_chart = gr.Plot(label="Agent Comparison Visualization")
            
            cmp_btn.click(
                fn=compare_agents,
                inputs=[cmp_difficulty, cmp_steps],
                outputs=[cmp_text, cmp_chart],
                api_name="compare_agents"
            )
        
        # TAB 3: DOCUMENTATION
        with gr.Tab("📚 Documentation"):
            gr.Markdown("""
## GuardianAI Fraud Detection Environment

### What is GuardianAI?
A production-grade Gymnasium environment for training AI agents to detect fraud in banking and UPI transactions.

### How Does It Work?

#### 1. **Gymnasium API**
```python
# Initialize
env = FraudDetectionEnv(difficulty='medium')

# Reset episode
observation, info = env.reset()

# Agent learning loop
for step in range(100):
    action = agent.decide(observation)  # Agent decides
    observation, reward, done, _, info = env.step(action)  # Get feedback
```

#### 2. **What Agents See (Observation)**
- Amount Z-score (deviation from usual)
- Transaction amount (INR)
- Transactions in last hour
- New merchant indicator
- Location change
- International transaction
- Fraud history rate
- And 3+ more features

#### 3. **What Agents Get (Reward)**
- **+1.0**: Correctly detected fraud (TP)
- **+0.5**: Correctly allowed legitimate (TN)
- **-0.5**: False positive (FP - flagged legitimate as fraud)
- **-1.0**: Missed fraud (FN - missed actual fraud)

#### 4. **Difficulty Levels**

**EASY** (8% fraud rate)
- Obvious patterns
- Large amount deviations
- High transaction velocity
- Expected accuracy: 70-90%

**MEDIUM** (5% fraud rate)
- Realistic patterns
- Moderate deviations
- Requires pattern recognition
- Expected accuracy: 50-75%

**HARD** (2.5% fraud rate)
- Subtle indicators
- Complex multi-feature patterns
- Requires ML models
- Expected accuracy: 30-60%

### Agent Types

**Conservative Agent**
- Very cautious
- Flags many transactions as fraud
- High precision, lower recall
- Good for sensitive applications

**Balanced Agent**
- Moderate approach
- Balanced between precision and recall
- Good general-purpose agent
- Recommended for most use cases

**Aggressive Agent**
- Aggressive fraud detection
- Flags fewer transactions
- Lower precision, higher recall
- Good for high-fraud environments

### Key Features
✓ Realistic transaction simulation  
✓ 8 different fraud patterns  
✓ 3 graduated difficulty levels  
✓ Multiple agent strategies  
✓ Full type safety with dataclasses  
✓ Fast synthetic data generation (10,000+ tx/sec)  
✓ Standard Gymnasium API compliance  

### Citation
```
@software{guardianai2026,
  title = {GuardianAI: Fraud Detection Environment},
  author = {GuardianAI Team},
  year = {2026},
  url = {https://github.com/guardianai}
}
```
""")

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )
