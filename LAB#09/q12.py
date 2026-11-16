import heapq
from collections import deque

def ucs(graph, start, goal, trace=True):
    cost, parent = {start: 0}, {start: None}
    pq, done, expanded = [(0, start)], set(), 0
    if trace: 
        print(f"{'Current':<9}{'g(n)':<6}{'Parent':<8}Priority queue after expansion")
    while pq:
        g, cur = heapq.heappop(pq)
        if cur in done: continue                 
        done.add(cur); expanded += 1
        if cur == goal:
            if trace: 
                print(f"{cur:<9}{g:<6}{str(parent[cur]):<8}GOAL REACHED")
            path = []
            while cur is not None: 
                path.append(cur)
                cur = parent[cur]
            return path[::-1], g, expanded
        for nb, w in graph.get(cur, []):
            new = g + w
            if new < cost.get(nb, float('inf')):
                cost[nb] = new
                parent[nb] = cur
                heapq.heappush(pq, (new, nb))
        if trace:
            live = sorted((c, n) for c, n in pq if n not in done and c == cost[n])
            print(f"{cur:<9}{g:<6}{str(parent[cur]):<8}{[(n, c) for c, n in live]}")
    return None, float('inf'), expanded

def bfs(graph, start, goal):
    parent, q, expanded = {start: None}, deque([start]), 0
    while q:
        cur = q.popleft(); expanded += 1
        if cur == goal:
            path = []
            while cur is not None: 
                path.append(cur)
                cur = parent[cur]
            return path[::-1], expanded
        for nb, _ in graph.get(cur, []):
            if nb not in parent: 
                parent[nb] = cur
                q.append(nb)

def path_cost(graph, path):
    return sum(dict(graph[a])[b] for a, b in zip(path, path[1:]))

def undirected(edges):
    g = {}
    for a, b, w in edges:
        g.setdefault(a, []).append((b, w))
        g.setdefault(b, []).append((a, w))
    return g

deliv = undirected([
    ('A','B',3), ('A','C',10), ('B','D',4), ('B','E',12),
    ('C','G',25), ('D','F',6), ('E','G',8), ('F','G',5)
])

path, total, n = ucs(deliv, 'A', 'G')
print("CFS route :", " -> ".join(path), "| cost =", total, "| nodes expanded =", n)

bp, bn = bfs(deliv, 'A', 'G')
print("BFS route :", " -> ".join(bp), "| cost =", path_cost(deliv, bp), "| nodes expanded =", bn)

print(f"CFS saves {path_cost(deliv, bp) - total} cost units even though it uses {len(path)-len(bp)} more edges.")


