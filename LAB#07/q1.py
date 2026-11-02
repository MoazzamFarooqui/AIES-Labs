import heapq, math
 
def astar(graph, h, start, goal, trace=False):
    g = {start: 0}; parent = {start: None}
    open_ = [(h[start], start)]; expanded = 0; step = 0
    if trace:
        print(f"{'Step':<5}{'Selected':<10}{'g(n)':<7}{'h(n)':<7}{'f(n)':<7}{'Parent':<8}OPEN after expansion")
    while open_:
        f, cur = heapq.heappop(open_)
        if f > g[cur] + h[cur] + 1e-9:      
            continue
        step += 1; expanded += 1
        if cur == goal:
            if trace:
                print(f"{step:<5}{cur:<10}{g[cur]:<7}{h[cur]:<7}{f:<7}{str(parent[cur]):<8}GOAL REACHED")
            path, n = [], cur
            while n is not None:
                path.append(n); n = parent[n]
            return path[::-1], g[cur], expanded
        for nb, w in graph.get(cur, []):
            tg = g[cur] + w
            if nb not in g or tg < g[nb]:
                g[nb] = tg; parent[nb] = cur
                heapq.heappush(open_, (tg + h[nb], nb))
        if trace:
            live = sorted({(round(ff, 1), n) for ff, n in open_ if abs(ff - (g[n] + h[n])) < 1e-9})
            print(f"{step:<5}{cur:<10}{g[cur]:<7}{h[cur]:<7}{f:<7}{str(parent[cur]):<8}"
                  + ", ".join(f"{n}(f={ff})" for ff, n in live))
    return None, math.inf, expanded
 
def build(edges, directed=False):
    gr = {}
    for u, v, w in edges:
        gr.setdefault(u, []).append((v, w)); gr.setdefault(v, [])
        if not directed: gr[v].append((u, w))
    return gr
 
def euclid(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])
 
edges = [("A","B",4),("A","C",2),("B","D",5),("C","D",8),("C","E",10),("D","E",2),("E","G",3)]
H = {"A":10,"B":7,"C":8,"D":5,"E":3,"G":0}
path, cost, exp = astar(build(edges, True), H, "A", "G", trace=True)
print("\nFinal path :", " -> ".join(path)); print("Total cost :", cost); print("Nodes expanded:", exp)
 
def road_demo(title, coords, roads, start, goal, unit, trace=False):
    pos = coords
    edges = [(u, v, math.ceil(euclid(pos[u], pos[v])*m*10)/10) for u, v, m in roads]
    gr = build(edges)
    h = {n: round(euclid(pos[n], pos[goal]), 1) for n in pos}
    path, cost, exp = astar(gr, h, start, goal, trace)
    print(f"Route  : {' -> '.join(path)}"); print(f"Total distance : {cost:.1f} {unit}"); print(f"Nodes expanded : {exp}")
    return edges, h

# Scenario 1: Hospital Emergency Route 

coords = {"H":(0,0),"J1":(2,1),"J2":(1,3),"J3":(4,0),"J4":(4,3),"J5":(6,1),"J6":(6,4),"ER":(8,3)}
roads = [("H","J1",1.1),("H","J2",1.3),("J1","J2",1.2),("J1","J3",1.2),("J1","J4",1.4),("J2","J4",1.3),
         ("J3","J4",1.5),("J3","J5",1.1),("J4","J5",1.3),("J4","J6",1.2),("J5","ER",1.2),("J6","ER",1.1)]
edges1, h1 = road_demo("S1", coords, roads, "H", "ER", "km", trace=True)
print("Road distances (g):", {f"{u}-{v}": w for u, v, w in edges1})
print("Straight-line h(n) to ER:", h1)


# Scenario 2: Delivery Robot (Grid)

GRID = ["S..#....",
        ".#.#.##.",
        "##...#..",
        ".#.#.#.#",
        "..P.~~~.",
        "####.##.",
        "....~..D"]
# legend: # obstacle, . cost 1, ~ cost 3 (slippery floor), S/P/D cost 1
R, C = len(GRID), len(GRID[0])
find = lambda ch: next((r, c) for r in range(R) for c in range(C) if GRID[r][c] == ch)
cost_of = lambda r, c: 3 if GRID[r][c] == "~" else 1
def grid_graph():
    gr = {}
    for r in range(R):
        for c in range(C):
            if GRID[r][c] == "#": continue
            gr[(r, c)] = [((r+dr, c+dc), cost_of(r+dr, c+dc)) for dr, dc in ((1,0),(-1,0),(0,1),(0,-1))
                          if 0 <= r+dr < R and 0 <= c+dc < C and GRID[r+dr][c+dc] != "#"]
    return gr
gg = grid_graph(); S, P, D = find("S"), find("P"), find("D")
def leg(a, b, name):
    h = {n: abs(n[0]-b[0]) + abs(n[1]-b[1]) for n in gg}
    p, c, e = astar(gg, h, a, b)
    print(f"\nLeg {name}: start={a}, goal={b}")
    print("Manhattan heuristic grid (X = obstacle):")
    for r in range(R): print("  " + " ".join(f"{h[(r,cc)]:>2}" if (r,cc) in h else " X" for cc in range(C)))
    print(f"Path: {p}\nCost: {c}   Nodes expanded: {e}")
    return p, c
p1, c1 = leg(S, P, "S -> P"); p2, c2 = leg(P, D, "P -> D")
print("\nGrid with route (* = path):")
full = set(p1 + p2)
for r in range(R): print("  " + " ".join("*" if (r,c) in full and GRID[r][c] not in "SPD" else GRID[r][c] for c in range(C)))
print(f"\nTotal route cost S -> P -> D = {c1} + {c2} = {c1+c2}")

# Scenario 3: University Campus Navigation

cc = {"Main Gate":(0,0),"Library":(200,150),"Administration":(150,-120),"Cafeteria":(350,0),
      "CS Department":(450,200),"Lab":(600,100)}
cr = [("Main Gate","Library",1.1),("Main Gate","Administration",1.2),("Library","Cafeteria",1.3),
      ("Library","CS Department",1.2),("Administration","Cafeteria",1.1),("Cafeteria","CS Department",1.4),
      ("Cafeteria","Lab",1.2),("CS Department","Lab",1.1)]
cedges = [(u, v, math.ceil(euclid(cc[u], cc[v])*m)) for u, v, m in cr]; cgraph = build(cedges)
def navigate(a, b):
    h = {n: euclid(cc[n], cc[b]) for n in cc}
    p, c, e = astar(cgraph, h, a, b)
    print(f"{a} -> {b}: {' -> '.join(p)} | {c:.0f} m | expanded {e}")
print("Buildings:", list(cc)); print("Roads (m):", {f"{u}-{v}": w for u, v, w in cedges}); print()
for a, b in [("Main Gate","Lab"),("Administration","CS Department"),("Library","Cafeteria"),("Lab","Main Gate")]:
    navigate(a, b)

