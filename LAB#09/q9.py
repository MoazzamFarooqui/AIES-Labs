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

# Weighted road network graph
print("Road Network, A -> G")
roads = {
    'A': [('B', 4), ('C', 2)], 
    'B': [('D', 7)], 
    'C': [('D', 3), ('E', 8)],
    'D': [('E', 2)], 
    'E': [('G', 4)], 
    'G': []
}

path, total, n = ucs(roads, 'A', 'G')
print("Final path :", " -> ".join(path))
print("Total cost :", total)


