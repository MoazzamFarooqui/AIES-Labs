from collections import deque

friends = {
    'Ali':    ['Bilal', 'Sara', 'Hina'],
    'Bilal':  ['Ali', 'Zain', 'Maria'],
    'Sara':   ['Ali', 'Maria', 'Omar'],
    'Hina':   ['Ali', 'Nida'],
    'Zain':   ['Bilal', 'Usman'],
    'Maria':  ['Bilal', 'Sara', 'Fatima'],
    'Omar':   ['Sara'],
    'Nida':   ['Hina', 'Kamran'],
    'Usman':  ['Zain', 'Ayesha'],
    'Fatima': ['Maria'],
    'Kamran': ['Nida', 'Rabia'],
    'Ayesha': ['Usman'],
    'Rabia':  ['Kamran', 'Imran'],
    'Imran':  ['Rabia'],
}

def bfs_levels(graph, start, max_level=3):
    level = {start: 0}              # user -> friendship level
    queue = deque([start])
    while queue:
        user = queue.popleft()
        if level[user] == max_level:    # do not go beyond the limit
            continue
        for friend in graph[user]:
            if friend not in level:     # not discovered yet
                level[friend] = level[user] + 1
                queue.append(friend)
    # group users by level
    result = {}
    for user, lvl in level.items():
        result.setdefault(lvl, []).append(user)
    return result

start = 'Ali'
levels = bfs_levels(friends, start, max_level=3)

print(f"Social network BFS starting from: {start}\n")
titles = {1: "Direct friends", 2: "Friends of friends", 3: "Friends of friends of friends"}
for lvl in range(1, 4):
    print(f"Level {lvl} - {titles[lvl]}: {levels.get(lvl, [])}")

within_3 = [u for lvl in range(1, 4) for u in levels.get(lvl, [])]
print(f"\nUsers within three friendship levels ({len(within_3)}): {within_3}")

outside = [u for u in friends if u != start and u not in within_3]
print(f"Users farther than three levels: {outside}")


