import random, itertools, math
 
random.seed(5)
L, POP, GENS, PC, PM = 4, 6, 8, 0.9, 0.08
x_of = lambda c: int(c, 2); fit = lambda c: x_of(c)**2 + 2*x_of(c)
def tournament(pop, k=2):
    return max(random.sample(pop, k), key=fit)
def crossover(a, b):
    if random.random() < PC:
        p = random.randint(1, L-1); return a[:p]+b[p:], b[:p]+a[p:], p
    return a, b, None
def mutate(c):
    return "".join(("1" if ch == "0" else "0") if random.random() < PM else ch for ch in c)
pop = ["".join(random.choice("01") for _ in range(L)) for _ in range(POP)]
def table(pop, g):
    print(f"\nGeneration {g}")
    print(f"  {'Chromosome':<12}{'x':<4}{'Fitness':<8}")
    for c in pop: print(f"  {c:<12}{x_of(c):<4}{fit(c):<8}")
    b = max(pop, key=fit); print(f"  Best: {b} (x={x_of(b)}, f={fit(b)})")
table(pop, 0); best_overall = max(pop, key=fit)
for g in range(1, GENS+1):
    new = [max(pop, key=fit)]                       
    while len(new) < POP:
        p1, p2 = tournament(pop), tournament(pop)
        c1, c2, _ = crossover(p1, p2); new += [mutate(c1), mutate(c2)]
    pop = new[:POP]; table(pop, g)
    best_overall = max(pop + [best_overall], key=fit)
print(f"\nBEST SOLUTION FOUND: chromosome={best_overall}, x={x_of(best_overall)}, f(x)={fit(best_overall)}  (true optimum: x=15, f=255)")

