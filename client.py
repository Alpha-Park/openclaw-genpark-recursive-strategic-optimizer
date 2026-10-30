# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Recursive Strategic Optimizer - Regret-Matching Equilibrium & Payoff Matrix Optimizer
Standard Library only: math, typing.
Calculates regret-matching strategy convergence in 2-player bimatrix games, iteratively prunes
strictly dominated strategies (IESDS), and extracts Pareto-optimal payoff frontiers.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkRecursiveStrategicOptimizer:
    def __init__(self):
        pass

    def compute_regret_matching_equilibrium(self, payoff_matrix_a: List[List[float]],
                                           payoff_matrix_b: List[List[float]],
                                           iterations: int = 100) -> Dict[str, Any]:
        """
        Executes Regret-Matching algorithm (Hart & Mas-Colell) for 2-player normal-form games.
        Updates strategy distributions based on positive cumulative regrets:
        sigma_i(a) = max(0, R_i(a)) / sum_{a'} max(0, R_i(a'))
        """
        n_rows = len(payoff_matrix_a)
        n_cols = len(payoff_matrix_a[0]) if n_rows > 0 else 0
        if n_rows == 0 or n_cols == 0:
            return {"error": "Invalid payoff matrices"}

        # Initialize cumulative regrets
        regrets_a = [0.0] * n_rows
        regrets_b = [0.0] * n_cols

        # Cumulative strategy sum for time-average strategy
        strategy_sum_a = [0.0] * n_rows
        strategy_sum_b = [0.0] * n_cols

        for t in range(iterations):
            # Compute current mixed strategy for Player A
            pos_regrets_a = [max(0.0, r) for r in regrets_a]
            sum_pos_a = sum(pos_regrets_a)
            if sum_pos_a > 0:
                strat_a = [r / sum_pos_a for r in pos_regrets_a]
            else:
                strat_a = [1.0 / n_rows] * n_rows

            # Compute current mixed strategy for Player B
            pos_regrets_b = [max(0.0, r) for r in regrets_b]
            sum_pos_b = sum(pos_regrets_b)
            if sum_pos_b > 0:
                strat_b = [r / sum_pos_b for r in pos_regrets_b]
            else:
                strat_b = [1.0 / n_cols] * n_cols

            for i in range(n_rows):
                strategy_sum_a[i] += strat_a[i]
            for j in range(n_cols):
                strategy_sum_b[j] += strat_b[j]

            # Expected payoff of actual mixed profile
            actual_payoff_a = sum(strat_a[i] * strat_b[j] * payoff_matrix_a[i][j] for i in range(n_rows) for j in range(n_cols))
            actual_payoff_b = sum(strat_a[i] * strat_b[j] * payoff_matrix_b[i][j] for i in range(n_rows) for j in range(n_cols))

            # Counterfactual payoffs for pure action deviations
            for i in range(n_rows):
                dev_payoff_a = sum(strat_b[j] * payoff_matrix_a[i][j] for j in range(n_cols))
                regrets_a[i] += (dev_payoff_a - actual_payoff_a)

            for j in range(n_cols):
                dev_payoff_b = sum(strat_a[i] * payoff_matrix_b[i][j] for i in range(n_rows))
                regrets_b[j] += (dev_payoff_b - actual_payoff_b)

        # Average strategy profiles
        tot_a = sum(strategy_sum_a)
        avg_strat_a = [round(s / tot_a, 4) for s in strategy_sum_a]

        tot_b = sum(strategy_sum_b)
        avg_strat_b = [round(s / tot_b, 4) for s in strategy_sum_b]

        expected_utility_a = sum(avg_strat_a[i] * avg_strat_b[j] * payoff_matrix_a[i][j] for i in range(n_rows) for j in range(n_cols))
        expected_utility_b = sum(avg_strat_a[i] * avg_strat_b[j] * payoff_matrix_b[i][j] for i in range(n_rows) for j in range(n_cols))

        return {
            "iterations_run": iterations,
            "player_a_average_strategy": avg_strat_a,
            "player_b_average_strategy": avg_strat_b,
            "expected_payoff_player_a": round(expected_utility_a, 4),
            "expected_payoff_player_b": round(expected_utility_b, 4),
            "convergence_regime": "CORRELATED_EQUILIBRIUM_APPROXIMATION"
        }

    def filter_dominated_strategies(self, payoff_matrix: List[List[float]],
                                    action_labels: List[str] = None) -> Dict[str, Any]:
        """
        Iterated Elimination of Strictly Dominated Strategies (IESDS) for Player A against Player B.
        Action i strictly dominates action k if payoff(i, j) > payoff(k, j) for all j.
        """
        n_rows = len(payoff_matrix)
        n_cols = len(payoff_matrix[0]) if n_rows > 0 else 0
        labels = action_labels or [f"Action_{i}" for i in range(n_rows)]

        active_indices = list(range(n_rows))
        eliminated = []

        changed = True
        while changed:
            changed = False
            for i in active_indices:
                for k in active_indices:
                    if i != k:
                        # Check if i strictly dominates k
                        strictly_dominates = all(payoff_matrix[i][j] > payoff_matrix[k][j] for j in range(n_cols))
                        if strictly_dominates and k in active_indices:
                            active_indices.remove(k)
                            eliminated.append({"eliminated_action": labels[k], "dominated_by": labels[i]})
                            changed = True
                            break
                if changed:
                    break

        surviving = [labels[idx] for idx in active_indices]

        return {
            "initial_strategies_count": n_rows,
            "surviving_strategies_count": len(surviving),
            "surviving_strategies": surviving,
            "eliminated_strategies": eliminated,
            "is_strictly_solvable": len(surviving) == 1
        }

    def compute_pareto_frontier_payoffs(self, payoff_pairs: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Extracts non-dominated Pareto frontier points from candidate joint payoffs.
        A point (u1, u2) dominates (v1, v2) if u1 >= v1 and u2 >= v2 and (u1 > v1 or u2 > v2).
        """
        pareto_optimal = []

        for cand in payoff_pairs:
            u_a = cand.get("payoff_a", 0.0)
            u_b = cand.get("payoff_b", 0.0)
            is_dominated = False

            for other in payoff_pairs:
                v_a = other.get("payoff_a", 0.0)
                v_b = other.get("payoff_b", 0.0)
                if (v_a >= u_a and v_b >= u_b) and (v_a > u_a or v_b > u_b):
                    is_dominated = True
                    break

            if not is_dominated:
                pareto_optimal.append(cand)

        return {
            "total_candidates": len(payoff_pairs),
            "pareto_frontier_count": len(pareto_optimal),
            "pareto_frontier": pareto_optimal
        }
