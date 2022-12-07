import math
import heapq


class Node:
    def __init__(self, coords, risk, can_visit):
        self.coords = coords
        self.risk = risk
        self.can_visit = can_visit


def parse_input():
    cave = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            nodes = []
            for char in line.strip():
                nodes.append(int(char))
            cave.append(nodes)

    return cave


def get_nodes(cave):
    nodes = []
    cave_width = len(cave[0])
    cave_height = len(cave)

    for y in range(cave_height):
        row = []
        for x in range(cave_width):
            coords = (x, y)
            risk = cave[y][x]
            can_visit = []
            if y > 0:  # up
                can_visit.append(
                    Node(coords=(x, y-1), risk=cave[y-1][x], can_visit=[]))
            if x < cave_width - 1:  # right
                can_visit.append(
                    Node(coords=(x+1, y), risk=cave[y][x+1], can_visit=[]))
            if y < cave_height - 1:  # down
                can_visit.append(
                    Node(coords=(x, y+1), risk=cave[y+1][x], can_visit=[]))
            if x > 0:  # left
                can_visit.append(
                    Node(coords=(x-1, y), risk=cave[y][x-1], can_visit=[]))
            row.append(Node(coords, risk, can_visit))
        nodes.append(row)

    return nodes


def dijkstra(nodes, start_node):
    dijkstra_nodes = []
    height = len(nodes)
    width = len(nodes[0])

    # init
    for y in range(height):
        dijkstra_row = []
        for x in range(width):
            if x == 0 and y == 0:
                dijkstra_row.append(0)
                continue
            dijkstra_row.append(math.inf)
        dijkstra_nodes.append(dijkstra_row)

    visited = set()  # only coordinates
    queue = []  # whole Node objects
    heapq.heapify(queue)
    heapq.heappush(
        queue, (start_node.risk, start_node.coords, start_node.can_visit))

    # init flags of indices in queue
    is_in_queue = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(False)
        is_in_queue.append(row)
    is_in_queue[start_node.coords[1]][start_node.coords[0]] = True

    X = 0
    Y = 1
    COORDS = 1
    CAN_VISIT = 2
    while len(visited) < height*width:
        current_node = heapq.heappop(queue)
        curr_x = current_node[COORDS][X]
        curr_y = current_node[COORDS][Y]
        visited.add((curr_x, curr_y))
        is_in_queue[curr_y][curr_x] = False
        can_visit = current_node[CAN_VISIT]

        possible_paths = []
        heapq.heapify(possible_paths)
        for next_node in can_visit:
            # evaluate paths
            next_x = next_node.coords[X]
            next_y = next_node.coords[Y]
            old_risk = dijkstra_nodes[next_y][next_x]
            current_risk = dijkstra_nodes[curr_y][curr_x]
            new_risk = current_risk + next_node.risk
            if old_risk > new_risk:
                dijkstra_nodes[next_y][next_x] = new_risk
                node_to_push = nodes[next_y][next_x]
                heapq.heappush(
                    possible_paths, (new_risk, node_to_push.coords, node_to_push.can_visit))
                is_in_queue[next_y][next_x] = True

            # determine whether can move to next node and if yes then push next node to queue
            can_move = next_node.coords not in visited and not is_in_queue[next_y][next_x]
            if can_move:
                node_to_push = nodes[next_y][next_x]
                heapq.heappush(
                    possible_paths, (new_risk, node_to_push.coords, node_to_push.can_visit))
                is_in_queue[next_y][next_x] = True
        queue += possible_paths

    return dijkstra_nodes[height-1][width-1]


def increase_row(row, by):
    return [node+by if node <= 9 - by else 0-(9-node)+by for node in row]


def extend_row(row):
    new_row = []
    for i in range(5):
        new_row += increase_row(row, by=i)
    return new_row


def extend_cave(cave):
    size = len(cave)
    extended_cave = []
    for _ in range(size*5):
        extended_cave.append([])

    for i in range(5):
        for y in range(size):
            row = increase_row(cave[y], by=i)
            new_row = extend_row(row)
            extended_cave[i*size+y] = new_row

    return extended_cave


if __name__ == "__main__":
    cave = parse_input()
    nodes = get_nodes(cave)

    result_1 = dijkstra(nodes, nodes[0][0])
    print("Part 1: ", result_1)

    extended_cave = extend_cave(cave)
    extended_nodes = get_nodes(extended_cave)
    result_2 = dijkstra(extended_nodes, extended_nodes[0][0])
    print("Part 2: ", result_2)
