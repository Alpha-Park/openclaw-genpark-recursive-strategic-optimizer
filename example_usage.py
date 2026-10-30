# -*- coding: utf-8 -*-
from client import OpenClawGenParkRecursiveStrategicOptimizer

opt = OpenClawGenParkRecursiveStrategicOptimizer()

# 1. Regret-Matching Equilibrium (Matching Pennies / Coordination)
# Game: Coordination
A = [[3.0, 0.0], [0.0, 2.0]]
B = [[3.0, 0.0], [0.0, 2.0]]
eq = opt.compute_regret_matching_equilibrium(A, B, iterations=100)
print(f"Regret-Matching Convergence: Player A Strat = {eq['player_a_average_strategy']}, Payoff = {eq['expected_payoff_player_a']}")

# 2. Dominated Strategy Pruning (Prisoner's Dilemma)
# Cooperate vs Defect: Defect dominates Cooperate
pd_matrix = [[3.0, 0.0], [5.0, 1.0]] # Row 1: Defect strictly dominates Row 0: Cooperate
pruned = opt.filter_dominated_strategies(pd_matrix, action_labels=["Cooperate", "Defect"])
print(f"\nDominance Pruning: Surviving = {pruned['surviving_strategies']} (Solvable: {pruned['is_strictly_solvable']})")

# 3. Pareto Frontier
pairs = [
    {"label": "Outcome_A", "payoff_a": 10.0, "payoff_b": 2.0},
    {"label": "Outcome_B", "payoff_a": 8.0, "payoff_b": 8.0},
    {"label": "Outcome_C", "payoff_a": 3.0, "payoff_b": 3.0} # dominated by B
]
pareto = opt.compute_pareto_frontier_payoffs(pairs)
print(f"\nPareto Frontier ({pareto['pareto_frontier_count']}): {[p['label'] for p in pareto['pareto_frontier']]}")
