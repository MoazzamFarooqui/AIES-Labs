from collections import deque

def bfs_path(graph, start, goal):
    parent, queue = {start: None}, deque([start])
    while queue:
        cur = queue.popleft()
        if cur == goal:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]
        for nb in graph[cur]:
            if nb not in parent:
                parent[nb] = cur
                queue.append(nb)
    return None

hospital = {
    'Emergency': ['Triage', 'Radiology', 'Pharmacy'], 
    'Triage': ['Emergency', 'Surgery'],
    'Radiology': ['Emergency', 'Lab', 'Surgery'], 
    'Pharmacy': ['Emergency', 'Ward'],
    'Lab': ['Radiology', 'Ward'], 
    'Surgery': ['Triage', 'Radiology', 'ICU'],
    'Ward': ['Pharmacy', 'Lab', 'ICU'], 
    'ICU': ['Surgery', 'Ward']
}

p = bfs_path(hospital, 'Emergency', 'ICU')
print("Shortest path :", " -> ".join(p))
print("Corridor connections (edges):", len(p) - 1)

