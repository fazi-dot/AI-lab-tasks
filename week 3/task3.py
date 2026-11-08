
from collections import deque
import heapq

# SECTION 1: UNWEIGHTED GRAPH SEARCHES (BFS & DFS)

graph_unweighted = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": [],
}


def bfs(start, goal):
    """Breadth-First Search (Queue / FIFO)"""
    q = deque([(start, [start])])
    seen = {start}
    order = []

    while q:
        node, path = q.popleft()
        order.append(node)
        if node == goal:
            return path, order

        for n in graph_unweighted[node]:
            if n not in seen:
                seen.add(n)
                q.append((n, path + [n]))
    return None, order


def dfs(start, goal):
    """Depth-First Search (Stack / LIFO)"""
    stack = [(start, [start])]
    seen = set()
    order = []

    while stack:
        node, path = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)

        if node == goal:
            return path, order

        # Reverse order pushes children so left-most child is popped first
        for n in reversed(graph_unweighted[node]):
            if n not in seen:
                stack.append((n, path + [n]))
    return None, order


print("=" * 50)
print("PRE-TASK: BFS & DFS")
print("=" * 50)
bfs_path, bfs_order = bfs("A", "G")
print("BFS Path:", bfs_path)
print("BFS Exploration Order:", bfs_order)

dfs_path, dfs_order = dfs("A", "G")
print("DFS Path:", dfs_path)
print("DFS Exploration Order:", dfs_order)



# TASK 1: DEPTH-LIMITED SEARCH (DLS) & ITERATIVE DEEPENING SEARCH (IDDFS)

def dls(node, goal, limit, path):
    """Depth-Limited Search with cutoff detection"""
    if node == goal:
        return "FOUND", path
    if limit == 0:
        if graph_unweighted[node]:
            return "CUTOFF", None
        return "FAILURE", None

    cutoff = False
    for child in graph_unweighted[node]:
        if child in path:
            continue
        status, result = dls(child, goal, limit - 1, path + [child])
        if status == "FOUND":
            return status, result
        if status == "CUTOFF":
            cutoff = True

    if cutoff:
        return "CUTOFF", None
    return "FAILURE", None


def iddfs(start, goal, max_depth):
    """Iterative Deepening Depth-First Search"""
    for limit in range(max_depth + 1):
        status, path = dls(start, goal, limit, [start])
        print(f"Limit: {limit} | Status: {status} | Path: {path}")
        if status == "FOUND":
            return path
    return None


print("\n" + "=" * 50)
print("TASK 1: DLS & IDDFS")
print("=" * 50)
print("--- DLS Runs by Limit ---")
for limit in [1, 2, 3, 4]:
    status, path = dls("A", "G", limit, ["A"])
    print(f"DLS limit {limit}: Status = {status}, Path = {path}")

print("\n--- IDDFS Execution ---")
iddfs_solution = iddfs("A", "G", 4)
print("IDDFS Found Path:", iddfs_solution)



# TASK 2: UNIFORM COST SEARCH (UCS)

# Weighted graph: node -> [(neighbor, edge_cost)]
graph_weighted = {
    "A": [("B", 1), ("C", 2)],
    "B": [("D", 4), ("E", 1)],
    "C": [("F", 5), ("G", 10)],
    "D": [],
    "E": [("G", 1)],
    "F": [],
    "G": [],
}


def ucs(start, goal):
    """Uniform Cost Search (Dijkstra-style lowest g(n) expansion)"""
    pq = [(0, start, [start])]
    best = {start: 0}
    order = []

    while pq:
        cost, node, path = heapq.heappop(pq)

        if cost > best.get(node, float("inf")):
            continue

        order.append(node)

        if node == goal:
            return path, cost, order

        for nxt, weight in graph_weighted[node]:
            new_cost = cost + weight
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(pq, (new_cost, nxt, path + [nxt]))

    return None, float("inf"), order


print("\n" + "=" * 50)
print("TASK 2: UNIFORM COST SEARCH (UCS)")
print("=" * 50)
ucs_path, ucs_cost, ucs_order = ucs("A", "G")
print("UCS Path:", ucs_path)
print("Total Cost:", ucs_cost)
print("Processing Order:", ucs_order)



# TASK 3: INFORMED SEARCH (GREEDY BEST-FIRST & A* SEARCH)
# Admissible heuristic estimates h(n) towards destination 'G'
heuristics = {"A": 2, "B": 1, "C": 8, "D": 6, "E": 1, "F": 5, "G": 0}


def greedy_best_first_search(start, goal):
    """Greedy Best-First Search: picks lowest heuristic h(n)"""
    pq = [(heuristics[start], start, [start], 0)]
    visited = set()
    order = []

    while pq:
        h_val, node, path, cost = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)
        order.append(node)

        if node == goal:
            return path, cost, order

        for nxt, weight in graph_weighted[node]:
            if nxt not in visited:
                heapq.heappush(
                    pq,
                    (
                        heuristics.get(nxt, 0),
                        nxt,
                        path + [nxt],
                        cost + weight,
                    ),
                )

    return None, float("inf"), order


def a_star_search(start, goal):
    """A* Search: combines exact path cost and heuristic f(n) = g(n) + h(n)"""
    g_costs = {start: 0}
    f_start = heuristics.get(start, 0)
    pq = [(f_start, 0, start, [start])]
    order = []

    while pq:
        f_val, g_val, node, path = heapq.heappop(pq)

        if g_val > g_costs.get(node, float("inf")):
            continue

        order.append(node)

        if node == goal:
            return path, g_val, order

        for nxt, weight in graph_weighted[node]:
            new_g = g_val + weight
            if new_g < g_costs.get(nxt, float("inf")):
                g_costs[nxt] = new_g
                f_nxt = new_g + heuristics.get(nxt, 0)
                heapq.heappush(pq, (f_nxt, new_g, nxt, path + [nxt]))

    return None, float("inf"), order


print("\n" + "=" * 50)
print("TASK 3: INFORMED SEARCH (GBFS & A*)")
print("=" * 50)
gbfs_path, gbfs_cost, gbfs_order = greedy_best_first_search("A", "G")
print("GBFS Path:", gbfs_path)
print("GBFS Cost:", gbfs_cost)
print("GBFS Processing Order:", gbfs_order)

print("-" * 30)
astar_path, astar_cost, astar_order = a_star_search("A", "G")
print("A* Path:", astar_path)
print("A* Cost:", astar_cost)
print("A* Processing Order:", astar_order)