from collections import deque

# Node names
names = {
    'A': 'Main Gate',
    'B': 'CS Department',
    'C': 'Library',
    'D': 'Cafeteria',
    'E': 'Laboratory',
    'F': 'Administration',
    'G': 'Auditorium',
}

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'G'],
    'F': ['C', 'G'],
    'G': ['E', 'F'],
}

def bfs(graph, start):
    visited = [start]          # nodes discovered so far
    queue = deque([start])     # FIFO queue
    traversal = []             # order in which nodes are processed

    print("Start node:", start, f"({names[start]})")
    print(f"Initial queue: {list(queue)}\n")
    print(f"{'Step':<6}{'Current':<10}{'Queue after step':<25}Visited nodes")
    print("-" * 75)

    step = 0
    while queue:
        current = queue.popleft()          # remove front node
        traversal.append(current)
        step += 1

        for neighbor in graph[current]:    # add unvisited neighbours
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

        print(f"{step:<6}{current:<10}{str(list(queue)):<25}{visited}")

    return traversal

order = bfs(graph, 'A')

print("\nFinal traversal:")
print(" -> ".join(order))
print(" -> ".join(names[n] for n in order))

