#!/usr/bin/env python3
"""
GuardianAI - Agent Learning Demonstration
Shows how agents learn from the OpenEnv environment through step()/reset() API.
No game - pure research/training demo.
"""

import sys
from guardianai import FraudDetectionEnv
from agents import BaseAgent, BalancedAgent, ConservativeAgent, AggressiveAgent
import numpy as np

def demo_single_episode(difficulty="medium"):
    """Demonstrate one episode of agent learning"""
    
    print(f"\n{'='*70}")
    print(f"GUARDIANAI - AGENT LEARNING DEMO ({difficulty.upper()})")
    print(f"{'='*70}\n")
    
    # Create environment
    env = FraudDetectionEnv(
        num_accounts=100,
        num_merchants=1000,
        fraud_rate=0.05,
        difficulty=difficulty,
        max_episode_length=100
    )
    
    # Reset environment
    observation, info = env.reset()
    print(f"✅ Environment initialized")
    print(f"   Observation space: {list(observation.keys())}")
    print(f"   Action space: Discrete(2) - 0=Legitimate, 1=Fraudulent\n")
    
    # Create agent
    agent = BalancedAgent()
    print(f"✅ Agent created: {agent.name}\n")
    
    # Run episode
    print(f"Running episode with {env.max_episode_length} transactions...\n")
    
    done = False
    step = 0
    total_reward = 0.0
    predictions = []
    ground_truth = []
    
    while not done:
        # Agent observes state
        action = agent.decide(observation)
        
        # Environment step
        observation, reward, terminated, truncated, info = env.step(action)
        
        done = terminated or truncated
        step += 1
        total_reward += reward
        
        # Track for evaluation
        true_label = 1 if info.get("is_fraud_ground_truth", False) else 0
        predictions.append(action)
        ground_truth.append(true_label)
        
        if step % 20 == 0:
            print(f"Step {step:3d}: Action={action}, Reward={reward:+.2f}, Total Reward={total_reward:+.1f}")
    
    print(f"\n{'─'*70}\n")
    
    # Evaluate agent
    summary = env.get_episode_summary()
    
    print("📊 EPISODE RESULTS")
    print(f"   Total steps: {step}")
    print(f"   Total reward: {total_reward:+.1f}")
    print(f"\n📈 ACCURACY METRICS")
    print(f"   Accuracy:  {summary['accuracy']:.1%}")
    print(f"   Precision: {summary['precision']:.1%}")
    print(f"   Recall:    {summary['fraud_detection_rate']:.1%}")
    print(f"   F1-Score:  {summary.get('f1_score', 0.0):.1%}")
    print(f"\n🎯 FRAUD DETECTION")
    print(f"   Frauds detected: {summary.get('frauds_caught', 0)}")
    print(f"   False positives: {summary.get('false_positives', 0)}")
    print(f"   True negatives:  {summary.get('legitimate_allowed', 0)}")
    
    env.close()
    return summary

def compare_agents():
    """Compare different agent strategies"""
    
    print(f"\n{'='*70}")
    print("AGENT COMPARISON - LEARNING FROM ENVIRONMENT")
    print(f"{'='*70}\n")
    
    agents = [
        ConservativeAgent(),
        BalancedAgent(),
        AggressiveAgent(),
    ]
    
    results = {}
    
    for agent in agents:
        print(f"\n▶ Testing {agent.name}...\n")
        
        env = FraudDetectionEnv(
            num_accounts=100,
            difficulty="medium",
            max_episode_length=200
        )
        
        observation, info = env.reset()
        done = False
        step = 0
        total_reward = 0.0
        
        while not done:
            action = agent.decide(observation)
            observation, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            step += 1
            total_reward += reward
            
            if step % 50 == 0:
                print(f"  Step {step}: Reward={reward:+.2f}")
        
        summary = env.get_episode_summary()
        results[agent.name] = summary
        
        print(f"\n  ✅ {agent.name} RESULTS:")
        print(f"     Accuracy: {summary['accuracy']:.1%}")
        print(f"     Precision: {summary['precision']:.1%}")
        print(f"     Recall: {summary['fraud_detection_rate']:.1%}")
        print(f"     Total Reward: {total_reward:+.1f}")
        
        env.close()
    
    # Ranking
    print(f"\n{'─'*70}")
    print("📊 RANKING BY ACCURACY")
    sorted_results = sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True)
    for rank, (agent_name, summary) in enumerate(sorted_results, 1):
        print(f"  {rank}. {agent_name:<25} - {summary['accuracy']:.1%} accuracy")

def show_learning_progression():
    """Show agent learning across difficulty levels"""
    
    print(f"\n{'='*70}")
    print("LEARNING PROGRESSION - CURRICULUM DIFFICULTY")
    print(f"{'='*70}\n")
    
    agent = BalancedAgent()
    difficulties = ["easy", "medium", "hard"]
    
    print(f"Agent: {agent.name}")
    print(f"Testing across difficulty levels...\n")
    
    for difficulty in difficulties:
        env = FraudDetectionEnv(
            num_accounts=100,
            difficulty=difficulty,
            max_episode_length=150
        )
        
        observation, info = env.reset()
        done = False
        total_reward = 0.0
        
        while not done:
            action = agent.decide(observation)
            observation, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            total_reward += reward
        
        summary = env.get_episode_summary()
        
        print(f"DIFFICULTY: {difficulty.upper()}")
        print(f"  Accuracy:  {summary['accuracy']:.1%}")
        print(f"  Precision: {summary['precision']:.1%}")
        print(f"  Recall:    {summary['fraud_detection_rate']:.1%}")
        print(f"  Reward:    {total_reward:+.1f}\n")
        
        env.close()

def show_environment_api():
    """Show the standard Gymnasium API"""
    
    print(f"\n{'='*70}")
    print("GYMNASIUM API - How Agents Learn")
    print(f"{'='*70}\n")
    
    print("Code example:")
    print("""
    # 1. CREATE ENVIRONMENT
    env = FraudDetectionEnv(difficulty='medium')
    
    # 2. RESET (Initialize episode)
    observation, info = env.reset()
    
    # 3. AGENT LEARNING LOOP
    done = False
    while not done:
        # Agent observes state
        action = agent.decide(observation)
        
        # Environment step (agent gets reward feedback for learning)
        observation, reward, terminated, truncated, info = env.step(action)
        
        done = terminated or truncated
    
    # 4. EVALUATE PERFORMANCE
    summary = env.get_episode_summary()
    print(f"Accuracy: {summary['accuracy']:.1%}")
    """)
    
    print("\nKey Points:")
    print("  ✓ reset() - Initialize episode with random state")
    print("  ✓ step(action) - Agent action gets reward feedback")
    print("  ✓ observation - Agent's view (not ground truth)")
    print("  ✓ reward - Signal for agent learning")
    print("  ✓ info - Ground truth (logging only)\n")

def main():
    """Main demo"""
    
    # Show API
    show_environment_api()
    
    # Run demo
    print("\n" + "="*70)
    print("RUNNING SINGLE EPISODE")
    print("="*70)
    demo_single_episode(difficulty="medium")
    
    # Compare agents
    print("\n" + "="*70)
    print("COMPARING AGENT STRATEGIES")
    print("="*70)
    compare_agents()
    
    # Show learning progression
    print("\n" + "="*70)
    print("LEARNING ACROSS DIFFICULTY LEVELS")
    print("="*70)
    show_learning_progression()
    
    # Summary
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE")
    print("="*70)
    print("\nGuardianAI Environment Features:")
    print("  ✓ Standard Gymnasium API (reset, step)")
    print("  ✓ Rich observation space (10+ features)")
    print("  ✓ Reward signal for agent learning")
    print("  ✓ 3 difficulty levels for curriculum learning")
    print("  ✓ Multiple agent strategies included")
    print("  ✓ Reproducible with fixed seeds")
    print("\nFor more details, see README.md or docs/")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
