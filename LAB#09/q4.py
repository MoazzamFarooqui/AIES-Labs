from collections import deque

maze = ["S0101",
        "01000",
        "00010",
        "10110",
        "000G0"]

R, C = len(maze), len(maze[0])
for r in range(R):
    for c in range(C):
        if maze[r][c] == 'S': s = (r, c)
        if maze[r][c] == 'G': g = (r, c)

parent, queue, expanded = {s: None}, deque([s]), []
while queue:
    cur = queue.popleft(); expanded.append(cur)
    if cur == g: break
    r, c = cur
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:       # up, down, left, right
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] != '1' and (nr, nc) not in parent:
            parent[(nr, nc)] = cur; queue.append((nr, nc))

if g in parent:
    path, cur = [], g
    while cur: path.append(cur); cur = parent[cur]
    path.reverse()
    print("Shortest path:", path)
    print("Number of moves:", len(path) - 1)
    print("Cells visited (expanded):", len(expanded))
    print(expanded)
    grid = [list(row) for row in maze]
    for (r, c) in path[1:-1]: grid[r][c] = '*'
    print("Solved maze (* = path):")
    for row in grid: print("  " + " ".join(row))
else:
    print("No path exists")

