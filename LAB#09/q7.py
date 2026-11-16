maze = ["S0101",
        "01000",
        "00010",
        "10110",
        "000G0"]

R, C = len(maze), len(maze[0])
s = next((r, c) for r in range(R) for c in range(C) if maze[r][c] == 'S')
g = next((r, c) for r in range(R) for c in range(C) if maze[r][c] == 'G')

stack, parent, seen = [s], {s: None}, []
found = False

while stack:
    cur = stack.pop()
    if cur in seen: continue
    seen.append(cur)
    if cur == g: found = True; break
    r, c = cur
    for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:   # right, down, left, up
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] != '1' and (nr, nc) not in seen:
            parent[(nr, nc)] = cur                 # last discoverer = DFS tree parent
            stack.append((nr, nc))

print("Path found:", found)
print("Visited cells (", len(seen), "):", seen)

if found:
    path, cur = [], g
    while cur: 
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    print("Final path:", path, "| moves =", len(path) - 1)
    
    grid = [list(row) for row in maze]
    for (r, c) in path[1:-1]: 
        grid[r][c] = '*'
    for row in grid: 
        print("  " + " ".join(row))
else:
    print("No path exists")


