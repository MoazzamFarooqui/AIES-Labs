import heapq

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

def undirected(edges):
    g = {}
    for a, b, w in edges:
        g.setdefault(a, []).append((b, w))
        g.setdefault(b, []).append((a, w))
    return g

links = [
    ('A','B',2,3,1), ('A','C',1,2,1), ('B','D',3,4,2), ('C','D',2,2,2), ('C','E',3,5,3),
    ('D','F',1,2,1), ('E','F',1,1,1), ('D','G',4,6,5), ('F','G',2,3,1), ('E','G',2,2,2)
]

print("Link costs = bandwidth + latency + congestion:")
for a, b, bw, lat, cg in links: 
    print(f"  {a}-{b}: {bw}+{lat}+{cg} = {bw+lat+cg}")

net = undirected([(a, b, bw + lat + cg) for a, b, bw, lat, cg in links])
print()

path, total, n = ucs(net, 'A', 'G')
print("Selected route:", " -> ".join(path))
print("Total cost:", total)

