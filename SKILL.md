---
name: openclaw-genpark-recursive-strategic-optimizer
description: OpenClaw GenPark Recursive Strategic Optimizer - Regret-matching equilibrium and payoff matrix optimizer with IESDS dominance pruning.
category: Service
version: 1.0.0
license: MIT
tools:
  - compute_regret_matching_equilibrium
  - filter_dominated_strategies
  - compute_pareto_frontier_payoffs
---

# Openclaw Genpark Recursive Strategic Optimizer

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Recursive Strategic Optimizer**.
Your primary directive is to execute: OpenClaw GenPark Recursive Strategic Optimizer - Regret-matching equilibrium and payoff matrix optimizer with IESDS dominance pruning.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `compute_regret_matching_equilibrium`
- `filter_dominated_strategies`
- `compute_pareto_frontier_payoffs`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `compute_regret_matching_equilibrium`
- `filter_dominated_strategies`
- `compute_pareto_frontier_payoffs`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
