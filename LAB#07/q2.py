import random, itertools, math
 
f = lambda x: x*x + 2*x
def neighbors(x): return [n for n in (x-1, x+1) if 0 <= n <= 15]
 
def steepest(x):
    it = 0
    while True:
        nb = {n: f(n) for n in neighbors(x)}
        best = max(nb, key=nb.get)
        print(f"Iter {it}: x={x:<2} f={f(x):<4} neighbors={nb} -> best neighbor x={best} (f={nb[best]})", end="")
        if nb[best] <= f(x):
            print("  => no better neighbor, STOP"); return x
        print("  => MOVE"); x = best; it += 1
 
def simple(x):
    it = 0
    while True:
        moved = False
        for n in neighbors(x):                     
            if f(n) > f(x):
                print(f"Iter {it}: x={x:<2} f={f(x):<4} first better neighbor x={n} (f={f(n)}) => MOVE")
                x = n; moved = True; it += 1; break
        if not moved:
            print(f"Iter {it}: x={x} f={f(x)} no better neighbor => STOP"); return x
 
print("\n-- Steepest-ascent, initial x = 3 --"); x = steepest(3)
print(f"FINAL: x={x}, f(x)={f(x)}")
print("\n-- Simple hill climbing, initial x = 9 --"); x = simple(9)
print(f"FINAL: x={x}, f(x)={f(x)}")

#  Scenario 1: Employee Shift Scheduling

random.seed(11)
SH = ["Morning","Evening","Night","OFF"]; DAYS = 3
EMP = {"Dr.Ali":("doctor",{(0,2)}),"Dr.Sara":("doctor",{(1,0)}),"Dr.Omar":("doctor",set()),
       "N.Hina":("nurse",set()),"N.Zain":("nurse",{(2,1)}),"N.Ayesha":("nurse",set()),
       "N.Bilal":("nurse",{(0,0)}),"N.Fatima":("nurse",set())}
names = list(EMP)
def sfit(s):
    t = 0
    for d in range(DAYS):
        for sh in range(3):
            who = [e for e in names if s[e][d] == sh]
            dc = sum(EMP[e][0] == "doctor" for e in who)
            t += 10*min(len(who), 2) + (15 if dc >= 1 else 0) - 5*max(0, len(who)-2)   # coverage rewards
    for e in names:
        t -= 25*sum((d, s[e][d]) in EMP[e][1] for d in range(DAYS))                     # unavailable shift
        t -= 12*max(0, sum(s[e][d] != 3 for d in range(DAYS)) - 2)                      # overtime (>2 shifts)
    return t
def show(s):
    print(f"{'Employee':<10}" + "".join(f"Day{d+1:<9}" for d in range(DAYS)))
    for e in names: print(f"{e:<10}" + "".join(f"{SH[s[e][d]]:<12}" for d in range(DAYS)))
sched = {e: [random.randrange(4) for _ in range(DAYS)] for e in names}
print("Max possible coverage score = 9 slots x 35 = 315\nInitial schedule, fitness =", sfit(sched)); show(sched)
it = 0
while True:
    best, bf = None, sfit(sched)
    for e in names:
        for d in range(DAYS):
            for sh in range(4):
                if sh != sched[e][d]:
                    old = sched[e][d]; sched[e][d] = sh; v = sfit(sched); sched[e][d] = old
                    if v > bf: bf, best = v, (e, d, sh)
    if best is None: break
    e, d, sh = best; it += 1
    print(f"Iter {it}: change {e} on Day{d+1}: {SH[sched[e][d]]} -> {SH[sh]}  fitness -> {bf}")
    sched[e][d] = sh
print(f"No neighbour has higher fitness. FINAL fitness = {sfit(sched)}"); show(sched)

# Scenario 2: Delivery Route Optimization

random.seed(3)
pts = {"Depot":(25,25), **{f"L{i}":(random.randint(0,50), random.randint(0,50)) for i in range(1,8)}}
dist = lambda a, b: math.dist(pts[a], pts[b])
def tour(r): p = ["Depot"]+list(r)+["Depot"]; return sum(dist(p[i], p[i+1]) for i in range(len(p)-1))
fit = lambda r: 1/tour(r)
route = [f"L{i}" for i in range(1, 8)]; random.shuffle(route)
print("Locations:", pts); print(f"Initial route : {route}\nInitial distance={tour(route):.2f}  fitness={fit(route):.6f}")
it = 0
while True:
    nbrs = []
    for i, j in itertools.combinations(range(7), 2):
        n = route[:]; n[i], n[j] = n[j], n[i]; nbrs.append((fit(n), n, (i, j)))
    best = max(nbrs)
    if it == 0:
        print("\nNeighbour routes of iteration 1 (swap positions i,j):")
        for fv, n, ij in nbrs: print(f"  swap{ij}: {n}  dist={1/fv:.2f}  fitness={fv:.6f}")
    if best[0] <= fit(route): print(f"Iter {it+1}: no better neighbour -> STOP"); break
    it += 1; route = best[1]
    print(f"Iter {it}: selected swap{best[2]} -> {route}  dist={tour(route):.2f}  fitness={fit(route):.6f}")
print(f"\nFinal route: Depot -> {' -> '.join(route)} -> Depot\nFinal distance={tour(route):.2f}  fitness={fit(route):.6f}")
opt = min(itertools.permutations(route), key=tour); print(f"(Brute-force optimum = {tour(opt):.2f})")


