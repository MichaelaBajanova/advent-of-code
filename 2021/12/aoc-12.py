def parse_input():
    lines = []
    nodes = []
    paths = {}
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_split = line.strip().split('-')
            node_1 = line_split[0]
            node_2 = line_split[1]

            if node_1 not in paths:
                paths[node_1] = []
            if node_2 not in paths:
                paths[node_2] = []

            paths[node_1].append(node_2)
            paths[node_2].append(node_1)

    return paths


def get_paths_from_node(connections, from_node, visited):
    if from_node == "end":
        return [["end"]]

    paths = []
    for node in connections[from_node]:
        visited_small_caves = [*visited]
        if node not in visited:
            if node.islower():
                visited_small_caves.append(node)
            paths_from_node = get_paths_from_node(
                connections, from_node=node, visited=visited_small_caves)
            for path_from_node in paths_from_node:
                paths.append([from_node, *path_from_node])

    return paths


def get_paths_from_node_2(connections, from_node, visited):
    if from_node == "end":
        return [["end"]]

    paths = []
    for node in connections[from_node]:
        visited_small_caves = visited.copy()
        has_visited_twice = False
        for visit in visited:
            if visited[visit] >= 2 and visit != "start":
                has_visited_twice = True
        if (node != 'start' and not has_visited_twice) or (has_visited_twice and visited[node] == 0):
            if node.islower():
                visited_small_caves[node] += 1
            paths_from_node = get_paths_from_node_2(
                connections, from_node=node, visited=visited_small_caves)
            for path_from_node in paths_from_node:
                paths.append([from_node, *path_from_node])

    return paths


if __name__ == "__main__":
    connections = parse_input()
    paths_1 = get_paths_from_node(
        connections, from_node="start", visited=["start"])
    print("Part 1: ", len(paths_1))

    visits = {}
    for node_key in connections:
        visits[node_key] = 0
    visits["start"] = 2
    paths_2 = get_paths_from_node_2(
        connections, from_node="start", visited=visits)
    print("Part 2: ", len(paths_2))
