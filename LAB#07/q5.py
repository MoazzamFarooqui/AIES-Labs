import random, itertools

def team_ga(emps, budget, min_size, max_size, min_senior, pop_n, gens, seed, verbose=False, pm=0.05):
    random.seed(seed); n = len(emps)
    def info(c):
        sel = [emps[i] for i in range(n) if c[i] == "1"]
        return sel, sum(e[4] for e in sel)
    def tfit(c):
        sel, sal = info(c)
        v = sum(3*e[1] + e[2] + 10*e[3] for e in sel)
        v -= 2*max(0, sal-budget)                                # over-budget penalty
        v -= 20*max(0, min_size-len(sel)) + 20*max(0, len(sel)-max_size)
        v -= 25*max(0, min_senior - sum(e[1] >= 8 for e in sel))
        return round(v, 1)
    def tour(pop, k=3): return max(random.sample(pop, k), key=tfit)
    pop = ["".join(random.choice("01") for _ in range(n)) for _ in range(pop_n)]
    print("Initial population:")
    for c in pop: print(f"  {c}  fitness={tfit(c):>7}  salary={info(c)[1]}k  size={c.count('1')}")
    hist = []
    for g in range(1, gens+1):
        new = [max(pop, key=tfit)]; V = verbose and g <= 2
        if V: print(f"\n--- Generation {g} detail ---")
        while len(new) < pop_n:
            p1, p2 = tour(pop), tour(pop)
            if random.random() < 0.9:
                cp = random.randint(1, n-1); c1, c2 = p1[:cp]+p2[cp:], p2[:cp]+p1[cp:]
            else: cp, c1, c2 = None, p1, p2
            m1 = "".join(("1" if x == "0" else "0") if random.random() < pm else x for x in c1)
            m2 = "".join(("1" if x == "0" else "0") if random.random() < pm else x for x in c2)
            if V:
                print(f"  parents {p1} (f={tfit(p1)}) & {p2} (f={tfit(p2)})  crossover point={cp}")
                print(f"     crossover -> {c1}, {c2}   after mutation -> {m1}, {m2}")
            new += [m1, m2]
        pop = new[:pop_n]; b = max(pop, key=tfit); hist.append(tfit(b))
        print(f"Generation {g:>2}: best={b} fitness={tfit(b):>7}  avg={sum(map(tfit,pop))/len(pop):.1f}")

    b = max(pop, key=tfit); sel, sal = info(b)
    print(f"\nFinal team {b}: " + ", ".join(e[0] for e in sel))
    print(f"  size={len(sel)}, total salary={sal}k (budget {budget}k), seniors(skill>=8)={sum(e[1]>=8 for e in sel)}, fitness={tfit(b)}")
    return hist, tfit, n

e6 = [("E1",9,8,1.0,120),("E2",6,3,0.8,60),("E3",8,6,0.9,100),("E4",5,2,1.0,40),("E5",7,5,0.6,70),("E6",4,1,1.0,35)]
print("Employees (name, skill, experience, availability, salary k):"); [print("  ", e) for e in e6]
print("Budget=250k, team size 2-4, at least 1 senior (skill>=8). Fitness = sum(3*skill+exp+10*avail) - penalties")
hist, tf, n = team_ga(e6, 250, 2, 4, 1, 20, 30, 4, pm=0.1)
opt = max(("".join(map(str, b)) for b in itertools.product((0,1), repeat=n)), key=tf)
print(f"Exhaustive check over 64 teams: optimum {opt} fitness={tf(opt)}")

