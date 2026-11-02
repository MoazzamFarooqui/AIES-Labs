import random, math, itertools

random.seed(10)
P = {"W":(0,0),"A":(2,6),"B":(8,3),"C":(5,9),"D":(9,8),"E":(1,2)}
cust = list("ABCDE"); d = lambda a, b: math.dist(P[a], P[b])
def td(r): p = ["W"]+r+["W"]; return sum(d(p[i], p[i+1]) for i in range(len(p)-1))
ft = lambda r: 1/td(r)
def ox(p1, p2):
    a, b = sorted(random.sample(range(len(p1)), 2)); ch = [None]*len(p1); ch[a:b+1] = p1[a:b+1]
    rest = [g for g in p2 if g not in ch]; return [g if g else rest.pop(0) for g in ch]
pop = [random.sample(cust, 5) for _ in range(12)]
print("Warehouse W + customers", {k: v for k, v in P.items() if k != "W"})
for g in range(0, 13):
    b = max(pop, key=ft)
    print(f"Gen {g:>2}: best route W->{'->'.join(b)}->W  distance={td(b):.3f}  fitness={ft(b):.5f}")
    new = [b[:]]                                              # elitism
    while len(new) < 12:
        p1 = max(random.sample(pop, 3), key=ft); p2 = max(random.sample(pop, 3), key=ft)
        c = ox(p1, p2)
        if random.random() < 0.3: i, j = random.sample(range(5), 2); c[i], c[j] = c[j], c[i]
        new.append(c)
    pop = new
opt = min(itertools.permutations(cust), key=lambda r: td(list(r)))
print(f"\nFinal best: W->{'->'.join(max(pop,key=ft))}->W distance={td(max(pop,key=ft)):.3f}")
print(f"Brute-force optimum (120 routes): W->{'->'.join(opt)}->W distance={td(list(opt)):.3f}")

