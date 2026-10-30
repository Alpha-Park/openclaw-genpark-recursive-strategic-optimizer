# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkRecursiveStrategicOptimizer

client = OpenClawGenParkRecursiveStrategicOptimizer()

TOOLS = [
    {
        "name": "compute_regret_matching_equilibrium",
        "description": "Calculates regret-matching correlated equilibrium strategy profile for bimatrix games.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "payoff_matrix_a": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
                "payoff_matrix_b": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
                "iterations": {"type": "integer"}
            },
            "required": ["payoff_matrix_a", "payoff_matrix_b"]
        }
    },
    {
        "name": "filter_dominated_strategies",
        "description": "Prunes strictly dominated strategies via Iterated Elimination (IESDS).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "payoff_matrix": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
                "action_labels": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["payoff_matrix"]
        }
    },
    {
        "name": "compute_pareto_frontier_payoffs",
        "description": "Extracts non-dominated Pareto frontier points from joint candidate payoffs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "payoff_pairs": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["payoff_pairs"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "compute_regret_matching_equilibrium":
            res = client.compute_regret_matching_equilibrium(args["payoff_matrix_a"], args["payoff_matrix_b"], args.get("iterations", 100))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "filter_dominated_strategies":
            res = client.filter_dominated_strategies(args["payoff_matrix"], args.get("action_labels"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "compute_pareto_frontier_payoffs":
            res = client.compute_pareto_frontier_payoffs(args["payoff_pairs"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
