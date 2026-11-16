import heapq
from collections import deque

def ucs(graph, start, goal, trace=True):
    cost, parent = {start: 0}, {start: None}
    pq, done, expanded = [(0, start)], set(), 0
    while pq:
        g, cur = heapq.heappop(pq)
        if cur in done: continue
        done.add(cur); expanded += 1
        if cur == goal:
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
    return None, float('inf'), expanded

def path_cost(graph, path):
    return sum(dict(graph[a])[b] for a, b in zip(path, path[1:]))

def undirected(edges):
    g = {}
    for a, b, w in edges:
        g.setdefault(a, []).append((b, w))
        g.setdefault(b, []).append((a, w))
    return g

city_roads = [  # (from, to, distance, traffic, time)
    ('Airport','Downtown',12,8,15), ('Airport','Station',5,1,6), ('Station','Mall',4,2,5),
    ('Station','University',6,1,7), ('Downtown','Stadium',10,9,12), ('Downtown','Hospital',3,6,4),
    ('Mall','Park',3,1,4), ('Mall','Hospital',6,3,7), ('University','Park',4,2,5),
    ('Park','Stadium',5,2,6), ('Hospital','Stadium',7,2,8)
]

print("Road                      Dist Traffic Time Total")
for a, b, d, t, m in city_roads: 
    print(f"{a+' - '+b:<24}{d:<5}{t:<8}{m:<5}{d+t+m}")

city = undirected([(a, b, d + t + m) for a, b, d, t, m in city_roads])
start, dest = 'Airport', 'Stadium'
 
def city_bfs(start, dest):
    parent, q, order = {start: None}, deque([start]), []
    while q:
        cur = q.popleft()
        order.append(cur)
        for nb, _ in sorted(city[cur]):
            if nb not in parent: 
                parent[nb] = cur
                q.append(nb)
    path, cur = [], dest
    while cur: 
        path.append(cur)
        cur = parent[cur]
    return order, path[::-1]

def city_dfs(node, seen, order):
    seen.add(node)
    order.append(node)
    for nb, _ in sorted(city[node]):
        if nb not in seen: 
            city_dfs(nb, seen, order)
    return order
 
order, bpath = city_bfs(start, dest)
print("\nBFS")
print(f"Traversal: {' -> '.join(order)}")
print(f"Fewest-roads route {start} to {dest}: {' -> '.join(bpath)}")
print(f"Shortest Number of Edges: {len(bpath)-1}")

print("\nDFS")
print(f"Traversal: {' -> '.join(city_dfs(start, set(), []))}")

cpath, ctotal, cn = ucs(city, start, dest, trace=False)
print("\nCFS")
print(f"Optimal Cost Path: {' -> '.join(cpath)}")
print(f"Total Cost: {ctotal}")



