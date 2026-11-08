import heapq
from typing import Dict, List, Tuple, Optional, Any

# Graph representation: node -> list of (neighbor, edge_cost)
GRAPH: Dict[str, List[Tuple[str, int]]] = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": [],
}

HEURISTIC: Dict[str, int] = {
    "S": 5,
    "A": 4,
    "B": 4,
    "C": 2,
    "G": 0,
}

START, GOAL = "S", "G"


def reconstruct_path(came_from: Dict[str, str], current: str) -> List[str]:
    """Reconstructs the optimal path from start to goal using parent pointers."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def search(
    graph: Dict[str, List[Tuple[str, int]]],
    heuristic: Dict[str, int],
    start: str = START,
    goal: str = GOAL,
    label: str = "A*",
) -> Optional[Dict[str, Any]]:
    """Runs A* / UCS search with priority queue tracking and detailed traces."""
    print(f"\n{'=' * 20} {label} {'=' * 20}")
    
    # Priority Queue stores: (f_score, g_score, current_node)
    pq: List[Tuple[int, int, str]] = [(heuristic[start], 0, start)]
    best_g: Dict[str, int] = {start: 0}
    came_from: Dict[str, str] = {}
    
    processed: List[str] = []
    expanded: List[str] = []

    while pq:
        f, g, node = heapq.heappop(pq)

        # Skip stale entries pushed with worse g-values
        if g > best_g.get(node, float("inf")):
            print(f"Skip stale entry: node={node}, g={g}, f={f}")
            continue

        processed.append(node)
        current_path = reconstruct_path(came_from, node)
        print(f"Process {node}: g={g}, h={heuristic[node]}, f={f}, path={' -> '.join(current_path)}")

        if node == goal:
            final_path = current_path
            # Calculate path cost independently from graph edge weights
            indep_cost = sum(
                next(w for nxt, w in graph[u] if nxt == v)
                for u, v in zip(final_path, final_path[1:])
            )
            print(f"Goal reached. Path={' -> '.join(final_path)}, cost={g}, independent_cost={indep_cost}")
            print(f"Processed trace: {processed}")
            print(f"Expanded nodes: {expanded}")
            print(f"Expansion count: {len(expanded)}")
            return {
                "path": final_path,
                "cost": g,
                "independent_cost": indep_cost,
                "processed": processed,
                "expanded": expanded,
                "expansion_count": len(expanded),
            }

        expanded.append(node)

        for nxt, weight in graph.get(node, []):
            new_g = g + weight
            if new_g < best_g.get(nxt, float("inf")):
                best_g[nxt] = new_g
                came_from[nxt] = node
                new_f = new_g + heuristic[nxt]
                heapq.heappush(pq, (new_f, new_g, nxt))
                print(f"  -> Update {nxt}: g={new_g}, h={heuristic[nxt]}, f={new_f}")

    print("No path found.")
    return None


def main():
    # 1. A* with provided heuristic
    astar_result = search(GRAPH, HEURISTIC, label="A* (Supplied Heuristic)")

    # 2. Uniform Cost Search (h = 0 everywhere)
    zero_h = {node: 0 for node in GRAPH}
    ucs_result = search(GRAPH, zero_h, label="UCS Control (h=0)")

    # 3. Inadmissible heuristic experiment: h(C) = 10 overestimates h*(C) = 3
    bad_h = dict(HEURISTIC)
    bad_h["C"] = 10
    overestimate_result = search(GRAPH, bad_h, label="A* Overestimate Experiment (h(C)=10)")

    # Summary Table
    print("\n" + "=" * 50)
    print(f"{'Experiment':<25} | {'Path':<18} | {'Cost':<5} | {'Expansions'}")
    print("-" * 50)
    for name, res in [
        ("A*", astar_result),
        ("UCS", ucs_result),
        ("A* (h(C)=10)", overestimate_result),
    ]:
        if res:
            path_str = " -> ".join(res["path"])
            print(f"{name:<25} | {path_str:<18} | {res['cost']:<5} | {res['expansion_count']}")
    print("=" * 50)


if __name__ == "__main__":
    main()