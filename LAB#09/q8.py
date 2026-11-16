prereq = {
    'Artificial Intelligence': ['Algorithms', 'Probability'],
    'Algorithms': ['Data Structures', 'Discrete Math'],
    'Data Structures': ['Programming'],
    'Probability': ['Calculus'],
    'Programming': [], 
    'Discrete Math': [], 
    'Calculus': []
}

seen, discovery, study_order = set(), [], []

def explore(course, depth=0):
    seen.add(course)
    discovery.append(course)
    print("  " * depth + ("-> " if depth else "") + course)
    for p in prereq[course]:
        if p not in seen: 
            explore(p, depth + 1)
    study_order.append(course)                     # post-order = safe study order

explore('Artificial Intelligence')

print("All prerequisites:", [c for c in discovery if c != 'Artificial Intelligence'])
print("A valid order to study them:", " -> ".join(study_order))

