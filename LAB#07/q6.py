import random, itertools

random.seed(10)
ex = {"C1":("T1",{"G1","G2"},"R1"),"C2":("T2",{"G1"},"R2"),"C3":("T1",{"G3"},"R1"),"C4":("T3",{"G2","G3"},"R2"),
      "C5":("T2",{"G4"},"R1"),"C6":("T4",{"G1","G4"},"R3"),"C7":("T3",{"G4"},"R3"),"C8":("T4",{"G2"},"R2")}
cs = list(ex); SL = ["Mon 9am","Mon 2pm","Tue 9am","Tue 2pm"]; UN = {"T1":{3},"T3":{0}}
def tfit(ch):
    t = dict(zip(cs, ch)); v = 100
    for a, b in itertools.combinations(cs, 2):
        if t[a] == t[b]:
            v -= 10*bool(ex[a][1] & ex[b][1]) + 10*(ex[a][0] == ex[b][0]) + 10*(ex[a][2] == ex[b][2])
    v -= 5*sum(t[c] in UN.get(ex[c][0], set()) for c in cs)
    load = [ch.count(s) for s in range(4)]; v -= 2*(max(load)-min(load))     # balance term
    return v
def show(ch): return " | ".join(f"{SL[s]}: {[c for c in cs if ch[cs.index(c)]==s]}" for s in range(4))
pop = [[random.randrange(4) for _ in cs] for _ in range(30)]
for g in range(0, 16):
    b = max(pop, key=tfit)
    print(f"Gen {g:>2} best fitness={tfit(b):>4}  {show(b)}")
    new = [b[:]]
    while len(new) < 30:
        p1 = max(random.sample(pop, 3), key=tfit); p2 = max(random.sample(pop, 3), key=tfit)
        cp = random.randint(1, len(cs)-1); kids = [p1[:cp]+p2[cp:], p2[:cp]+p1[cp:]]
        for k in kids:
            for i in range(len(k)):
                if random.random() < 0.1: k[i] = random.randrange(4)
        new += kids
    pop = new[:30]

    