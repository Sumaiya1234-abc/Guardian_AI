#!/usr/bin/env python3
"""
GuardianAI - Modern Web UI with Dark/Light Mode
Clean, simple, and easy-to-understand interface
"""

from flask import Flask, render_template, jsonify, request
from guardianai import FraudDetectionEnv
from agents import BalancedAgent, ConservativeAgent, AggressiveAgent
import numpy as np
import json
from datetime import datetime
import os

# Get the directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.config['JSON_SORT_KEYS'] = False

# Global state
current_env = None
episode_data = None

# Agent classes mapping
AGENTS = {
    "Conservative": ConservativeAgent,
    "Balanced": BalancedAgent,
    "Aggressive": AggressiveAgent
}

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"""
        <html>
        <head><title>GuardianAI - Error</title></head>
        <body style="font-family: Arial; margin: 50px;">
        <h1>❌ Error Loading Interface</h1>
        <p><strong>Error:</strong> {str(e)}</p>
        <p>Make sure you have:</p>
        <ul>
            <li>templates/index.html file</li>
            <li>All dependencies installed (pip install flask)</li>
        </ul>
        </body>
        </html>
        """, 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'message': str(error)}), 404

@app.route('/api/run-episode', methods=['POST'])
def run_episode():
    """Run a single episode and return results"""
    try:
        data = request.json
        difficulty = data.get('difficulty', 'medium')
        agent_name = data.get('agent', 'Balanced')
        num_steps = int(data.get('steps', 100))
        
        # Create environment
        env = FraudDetectionEnv(
            num_accounts=100,
            difficulty=difficulty,
            max_episode_length=num_steps
        )
        
        # Create agent
        agent_class = AGENTS.get(agent_name, BalancedAgent)
        agent = agent_class()
        
        # Reset
        observation, info = env.reset()
        
        # Run episode
        done = False
        step = 0
        rewards_list = []
        predictions = []
        ground_truth = []
        amounts = []
        
        while not done and step < num_steps:
            action = agent.decide(observation)
            observation, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            
            step += 1
            rewards_list.append(float(reward))
            predictions.append(int(action))
            ground_truth.append(1 if info.get("is_fraud_ground_truth", False) else 0)
            amounts.append(float(info.get("amount", 0)))
        
        # Calculate metrics
        correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)
        accuracy = correct / len(predictions) if predictions else 0
        
        # True positives, false positives, etc.
        tp = sum(1 for p, g in zip(predictions, ground_truth) if p == 1 and g == 1)
        fp = sum(1 for p, g in zip(predictions, ground_truth) if p == 1 and g == 0)
        fn = sum(1 for p, g in zip(predictions, ground_truth) if p == 0 and g == 1)
        tn = sum(1 for p, g in zip(predictions, ground_truth) if p == 0 and g == 0)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        cumulative_reward = np.cumsum(rewards_list).tolist()
        
        result = {
            'success': True,
            'agent': agent.name,
            'difficulty': difficulty,
            'steps': step,
            'metrics': {
                'accuracy': round(accuracy, 3),
                'precision': round(precision, 3),
                'recall': round(recall, 3),
                'f1_score': round(f1, 3),
                'total_reward': round(sum(rewards_list), 2),
            },
            'counts': {
                'true_positives': tp,
                'false_positives': fp,
                'false_negatives': fn,
                'true_negatives': tn,
                'correct': correct,
                'total': len(predictions)
            },
            'charts': {
                'rewards': rewards_list[:50],  # First 50 steps
                'cumulative': cumulative_reward[:50],
                'predictions': predictions[:50],
                'ground_truth': ground_truth[:50],
            }
        }
        
        env.close()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/compare-agents', methods=['POST'])
def compare_agents():
    """Compare all three agents"""
    try:
        data = request.json
        difficulty = data.get('difficulty', 'medium')
        num_steps = int(data.get('steps', 100))
        
        results = {}
        
        for agent_name, agent_class in AGENTS.items():
            env = FraudDetectionEnv(
                num_accounts=100,
                difficulty=difficulty,
                max_episode_length=num_steps
            )
            
            agent = agent_class()
            observation, info = env.reset()
            
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
                rewards_list.append(float(reward))
                predictions.append(int(action))
                ground_truth.append(1 if info.get("is_fraud_ground_truth", False) else 0)
            
            # Calculate metrics
            correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)
            accuracy = correct / len(predictions) if predictions else 0
            
            tp = sum(1 for p, g in zip(predictions, ground_truth) if p == 1 and g == 1)
            fp = sum(1 for p, g in zip(predictions, ground_truth) if p == 1 and g == 0)
            fn = sum(1 for p, g in zip(predictions, ground_truth) if p == 0 and g == 1)
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            results[agent_name] = {
                'accuracy': round(accuracy, 3),
                'precision': round(precision, 3),
                'recall': round(recall, 3),
                'f1_score': round(f1, 3),
                'total_reward': round(sum(rewards_list), 2),
                'frauds_caught': tp,
                'false_positives': fp,
            }
            
            env.close()
        
        return jsonify({'success': True, 'results': results})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get project information"""
    return jsonify({
        'project': 'GuardianAI',
        'description': 'Fraud Detection Environment with AI Agents',
        'agents': list(AGENTS.keys()),
        'difficulties': ['easy', 'medium', 'hard'],
        'version': '2.0'
    }
    )# =========================
# OPENENV REQUIRED ENDPOINTS
# =========================

env_instance = None

@app.route('/reset', methods=['POST'])
def reset_environment():
    global env_instance

    env_instance = FraudDetectionEnv(
        num_accounts=100,
        difficulty="medium",
        max_episode_length=100
    )

    observation, info = env_instance.reset()

    return jsonify({
        "observation": observation,
        "state": {
            "step": 0
        }
    }), 200


@app.route('/state', methods=['GET'])
def get_state():
    global env_instance

    if env_instance is None:
        return jsonify({"error": "Environment not initialized"}), 400

    return jsonify({
        "state": {
            "step": env_instance.current_step
        }
    }), 200


@app.route('/step', methods=['POST'])
def step_environment():
    global env_instance

    if env_instance is None:
        return jsonify({"error": "Environment not initialized"}), 400

    data = request.json
    action = data.get("action", 0)

    observation, reward, terminated, truncated, info = env_instance.step(action)

    done = terminated or truncated

    return jsonify({
        "observation": observation,
        "reward": float(reward),
        "done": done,
        "info": info
    }), 200

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  GuardianAI - Web Interface")
    print("="*50)
    print("\n🚀 Starting server...")
    print(f"📁 Template folder: {TEMPLATE_DIR}")
    print(f"📁 Template folder exists: {os.path.exists(TEMPLATE_DIR)}")
    print(f"📁 index.html exists: {os.path.exists(os.path.join(TEMPLATE_DIR, 'index.html') ) }
    print("🛑 Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=7860, use_reloader=False)
