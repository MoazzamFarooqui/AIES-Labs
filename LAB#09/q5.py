def dfs_recursive(graph, node, visited=None, order=None, depth=0):
    if visited is None: visited, order = set(), []
    visited.add(node); order.append(node)
    print(f"{'  ' * depth}visit {node:<3} | visited={sorted(visited)}")
    for nb in graph[node]:
        if nb not in visited:
            dfs_recursive(graph, nb, visited, order, depth + 1)
    if depth: print(f"{'  ' * depth}backtrack from {node}")
    return order
 
def dfs_stack(graph, start):
    stack, visited, order = [start], set(), []
    print(f"{'Popped':<8}{'Stack after step':<20}Visited")
    while stack:
        node = stack.pop()
        if node in visited: continue
        visited.add(node); order.append(node)
        for nb in reversed(graph[node]):          # reversed => same order as recursion
            if nb not in visited: stack.append(nb)
        print(f"{node:<8}{str(stack):<20}{order}")
    return order

# Graph representing the computer network
net = {
    'A': ['B', 'C'], 
    'B': ['A', 'D', 'E'], 
    'C': ['A', 'F'],
    'D': ['B'], 
    'E': ['B'], 
    'F': ['C']
}

print("Network, recursive DFS from Router A")
o1 = dfs_recursive(net, 'A')
print("Final traversal (recursive):", " -> ".join(o1))

print("\nNetwork, DFS with explicit stack")
o2 = dfs_stack(net, 'A')
print("Final traversal (stack)    :", " -> ".join(o2))

