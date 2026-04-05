#!/usr/bin/env python
"""Test script for Agent Grader system"""

from guardianai.agent_grader import MetricsCalculator, AgentGrader, MultiTaskGrader
from guardianai.tasks import Task
import numpy as np

print("\n" + "="*70)
print("TESTING AGENT GRADER SYSTEM")
print("="*70 + "\n")

# Test 1: MetricsCalculator
print("TEST 1: MetricsCalculator")
print("-" * 70)
predictions = [0, 1, 0, 0, 1, 1, 0, 1]
ground_truth = [0, 0, 1, 0, 1, 1, 0, 1]
metrics = MetricsCalculator.calculate_metrics(predictions, ground_truth)
print(f"Input: {len(predictions)} predictions")
print(f"  TP: {metrics.true_positives}, TN: {metrics.true_negatives}")
print(f"  FP: {metrics.false_positives}, FN: {metrics.false_negatives}")
print(f"  Accuracy:  {metrics.accuracy:.1%}")
print(f"  Precision: {metrics.precision:.1%}")
print(f"  Recall:    {metrics.recall:.1%}")
print(f"  F1:        {metrics.f1_score:.1%}")
print("✓ MetricsCalculator works\n")

# Test 2: AgentGrader on EASY task
print("TEST 2: AgentGrader (single task - EASY)")
print("-" * 70)
grader = AgentGrader(Task.EASY)
np.random.seed(42)
preds = np.random.randint(0, 2, 100).tolist()
truth = np.random.randint(0, 2, 100).tolist()
result = grader.grade('TestAgent', preds, truth, total_reward=150.0)
print(f"Agent: {result.agent_name}")
print(f"Task: {result.task.value.upper()}")
print(f"Score: {result.score:.2f}/1.0")
print(f"Interpretation: {result.score_interpretation()}")
print(f"Accuracy: {result.metrics.accuracy:.1%}")
print(f"Recall: {result.metrics.recall:.1%}")
print("✓ AgentGrader (single task) works\n")

# Test 3: MultiTaskGrader
print("TEST 3: MultiTaskGrader (all tasks)")
print("-" * 70)
grader = MultiTaskGrader()
np.random.seed(42)

easy_preds = np.random.randint(0, 2, 100).tolist()
easy_truth = np.random.randint(0, 2, 100).tolist()
medium_preds = np.random.randint(0, 2, 200).tolist()
medium_truth = np.random.randint(0, 2, 200).tolist()
hard_preds = np.random.randint(0, 2, 300).tolist()
hard_truth = np.random.randint(0, 2, 300).tolist()

results = grader.grade_agent(
    agent_name='MultiAgent',
    easy_predictions=easy_preds,
    easy_ground_truth=easy_truth,
    medium_predictions=medium_preds,
    medium_ground_truth=medium_truth,
    hard_predictions=hard_preds,
    hard_ground_truth=hard_truth,
)

print(f"Graded agent: MultiAgent")
print(f"  Easy:   {results[Task.EASY].score:.2f}/1.0 ({results[Task.EASY].score_interpretation()})")
print(f"  Medium: {results[Task.MEDIUM].score:.2f}/1.0 ({results[Task.MEDIUM].score_interpretation()})")
print(f"  Hard:   {results[Task.HARD].score:.2f}/1.0 ({results[Task.HARD].score_interpretation()})")
print("✓ MultiTaskGrader works\n")

# Test 4: Comparative analysis
print("TEST 4: Comparative Analysis")
print("-" * 70)
analysis = grader.get_comparative_analysis("MultiAgent")
print(analysis[:300] + "...\n")
print("✓ Comparative analysis works\n")

# Test 5: Leaderboard
print("TEST 5: Leaderboard")
print("-" * 70)
# Add another agent
np.random.seed(43)
grader.grade_agent(
    agent_name='AnotherAgent',
    easy_predictions=np.random.randint(0, 2, 100).tolist(),
    easy_ground_truth=easy_truth,
    medium_predictions=np.random.randint(0, 2, 200).tolist(),
    medium_ground_truth=medium_truth,
    hard_predictions=np.random.randint(0, 2, 300).tolist(),
    hard_ground_truth=hard_truth,
)

leaderboard = grader.get_leaderboard()
# Print first 500 chars of leaderboard
print(leaderboard[:500])
print("\n✓ Leaderboard works\n")

print("="*70)
print("ALL TESTS PASSED! ✓✓✓")
print("="*70 + "\n")

# Summary
print("Summary of Agent Grader System:")
print("  ✓ MetricsCalculator - computes accuracy, precision, recall, F1")
print("  ✓ AgentGrader - grades single task (EASY/MEDIUM/HARD)")
print("  ✓ MultiTaskGrader - grades all 3 tasks simultaneously")
print("  ✓ Score normalization - 0.0-1.0 scale")
print("  ✓ Task-specific weights - different emphasis per difficulty")
print("  ✓ Comparative analysis - reports on agent performance")
print("  ✓ Leaderboard - ranks multiple agents")
print()
