import random, itertools

EXAMS = {
    "E1": ("T1", {"G1", "G2"}, "R1"),
    "E2": ("T2", {"G1"},       "R2"),
    "E3": ("T1", {"G3"},       "R1"),
    "E4": ("T3", {"G2", "G3"}, "R2"),
    "E5": ("T2", {"G4"},       "R1"),
    "E6": ("T3", {"G4", "G1"}, "R3"),
}
SLOTS = ["Mon 9am", "Mon 2pm", "Tue 9am", "Tue 2pm"]
TEACHER_UNAVAILABLE = {"T1": {3}, "T3": {0}}      # slot indices a teacher cannot attend
ROOM_UNAVAILABLE    = {"R2": {1}, "R3": {2}}      # slot indices a room is not free

REWARD_FREE, REWARD_TEACHER_OK, REWARD_ROOM_OK = 10, 5, 5
PEN_STUDENT, PEN_ROOM, PEN_TEACHER = 20, 15, 15
MAX_FITNESS = len(EXAMS) * (REWARD_FREE + REWARD_TEACHER_OK + REWARD_ROOM_OK)   # 120

def evaluate(t):
    """t = timetable: dict exam -> slot index. Returns (fitness, details)."""
    stu = rm = tea = 0
    in_conflict = set()
    for a, b in itertools.combinations(EXAMS, 2):
        if t[a] == t[b]:
            if EXAMS[a][1] & EXAMS[b][1]: stu += 1; in_conflict |= {a, b}
            if EXAMS[a][2] == EXAMS[b][2]: rm += 1;  in_conflict |= {a, b}
            if EXAMS[a][0] == EXAMS[b][0]: tea += 1; in_conflict |= {a, b}
    free   = len(EXAMS) - len(in_conflict)                                   # conflict-free exams
    t_ok   = sum(t[e] not in TEACHER_UNAVAILABLE.get(EXAMS[e][0], set()) for e in EXAMS)
    r_ok   = sum(t[e] not in ROOM_UNAVAILABLE.get(EXAMS[e][2], set()) for e in EXAMS)
    fit = (REWARD_FREE*free + REWARD_TEACHER_OK*t_ok + REWARD_ROOM_OK*r_ok
           - PEN_STUDENT*stu - PEN_ROOM*rm - PEN_TEACHER*tea)
    return fit, dict(free=free, teacher_ok=t_ok, room_ok=r_ok, student=stu, room=rm, teacher=tea)

def fitness(t): return evaluate(t)[0]

def neighbours(t):
    """Every timetable obtained by changing ONE exam's time slot."""
    for e in EXAMS:
        for s in range(len(SLOTS)):
            if s != t[e]:
                n = dict(t); n[e] = s
                yield (e, s), n

def show(t):
    for i, name in enumerate(SLOTS):
        items = [f"{e}({EXAMS[e][0]},{EXAMS[e][2]})" for e in EXAMS if t[e] == i]
        print(f"   {name:<8}: {', '.join(items) if items else '-'}")
    f, d = evaluate(t)
    print(f"   fitness={f}/{MAX_FITNESS} | conflict-free exams={d['free']}, teacher-available={d['teacher_ok']}, "
          f"room-available={d['room_ok']} | student conflicts={d['student']}, room conflicts={d['room']}, "
          f"teacher conflicts={d['teacher']}")

def hill_climb(start, verbose=True):
    t, it = dict(start), 0
    while True:
        nb = list(neighbours(t))
        if verbose and it == 0:
            print(f"\n   Iteration 1 considers {len(nb)} neighbours, e.g.:")
            for (e, s), n in nb[:6]:
                print(f"     change {e} to {SLOTS[s]:<8} -> fitness {fitness(n)}")
        (move, best) = max(nb, key=lambda x: fitness(x[1]))
        if fitness(best) <= fitness(t):
            if verbose: print(f"Iteration {it+1}: best neighbour fitness {fitness(best)} <= current {fitness(t)} -> STOP (local/global maximum)")
            return t, it
        it += 1
        if verbose: print(f"Iteration {it}: move {move[0]} {SLOTS[t[move[0]]]} -> {SLOTS[move[1]]}   fitness {fitness(t)} -> {fitness(best)}")
        t = best

print("Solution representation : dictionary  exam -> time-slot index")
print("Neighbour               : same timetable with ONE exam moved to a different slot")
print(f"Fitness (max {MAX_FITNESS})        : +{REWARD_FREE} per conflict-free exam, +{REWARD_TEACHER_OK} per exam in a teacher-available slot,"
      f" +{REWARD_ROOM_OK} per exam in a room-available slot,")
print(f"                          -{PEN_STUDENT} per student conflict, -{PEN_ROOM} per room conflict, -{PEN_TEACHER} per teacher conflict")
print("Teacher unavailable     :", {k: [SLOTS[i] for i in v] for k, v in TEACHER_UNAVAILABLE.items()})
print("Room unavailable        :", {k: [SLOTS[i] for i in v] for k, v in ROOM_UNAVAILABLE.items()})

random.seed(4)
start = {e: random.randrange(len(SLOTS)) for e in EXAMS}
print("\nINITIAL TIMETABLE"); show(start)
final, its = hill_climb(start)
print(f"\nFINAL TIMETABLE after {its} moves"); show(final)

best, bestf, results = None, -10**9, []
for seed in range(20):
    random.seed(seed); s0 = {e: random.randrange(len(SLOTS)) for e in EXAMS}
    r, _ = hill_climb(s0, verbose=False); results.append(fitness(r))
    if fitness(r) > bestf: best, bestf = r, fitness(r)
print(f"\nRandom restarts (20 runs): final fitness values = {sorted(results)}")
print(f"Runs reaching the maximum {max(results)}: {results.count(max(results))}/20")
print("\nBEST TIMETABLE OVER ALL RESTARTS"); show(best)