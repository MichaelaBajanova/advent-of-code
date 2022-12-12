import math
import heapq


class Node:
    def __init__(self, coords, cost, can_visit):
        self.coords = coords
        self.cost = cost
        self.can_visit = can_visit


def parse_input():
    heightmap = []
    start = (0, 0)
    end = (0, 0)
    y = 0
    with (open("./input.txt")) as input_file:
        for line in input_file:
            row = []
            x = 0
            for char in list(line.strip()):
                if char == 'S':
                    start = (x, y)
                    row.append(ord('a'))
                elif char == 'E':
                    end = (x, y)
                    row.append(ord('z'))
                else:
                    row.append(ord(char))
                x += 1
            heightmap.append(row)
            y += 1

    return {"start": start, "end": end, "heightmap": heightmap}


def can_go_to(heightmap, coords, this_height):
    X = 0
    Y = 1
    x = coords[X]
    y = coords[Y]
    next_height = heightmap[y][x]

    return next_height < this_height or (next_height >= this_height and next_height - this_height <= 1)


def get_nodes(heightmap):
    nodes = []
    width = len(heightmap[0])
    height = len(heightmap)

    for y in range(1, height-1):
        row = []
        for x in range(1, width-1):
            coords = (x-1, y-1)
            cost = heightmap[y][x]
            can_visit = []
            if can_go_to(heightmap, (x, y-1), cost):  # up
                can_visit.append(
                    Node(coords=(x-1, y-2), cost=heightmap[y-1][x], can_visit=[]))
            if can_go_to(heightmap, (x+1, y), cost):  # right
                can_visit.append(
                    Node(coords=(x, y-1), cost=heightmap[y][x+1], can_visit=[]))
            if can_go_to(heightmap, (x, y+1), cost):  # down
                can_visit.append(
                    Node(coords=(x-1, y), cost=heightmap[y+1][x], can_visit=[]))
            if can_go_to(heightmap, (x-1, y), cost):  # left
                can_visit.append(
                    Node(coords=(x-2, y-1), cost=heightmap[y][x-1], can_visit=[]))
            row.append(Node(coords, cost, can_visit))
        nodes.append(row)

    return nodes


def print_dijkstra(dijkstra_nodes):
    for i in range(len(dijkstra_nodes[0])+1):
        if i == 0:
            print("   ", end=" ")
        else:
            if len(str(i-1)) == 1:
                print(" ", end="")
                print(i-1, end="")
                print(" ", end=" ")
            elif len(str(i-1)) == 2:
                print(i-1, end="")
                print(" ", end=" ")
            else:
                print(i-1, end=" ")
    print()
    for i in range(len(dijkstra_nodes)):
        print(i, end="   ")
        for node in dijkstra_nodes[i]:
            if len(str(node)) == 1:
                print(" ", end="")
                print(node, end="")
                print(" ", end=" ")
            elif len(str(node)) == 2:
                print(node, end="")
                print(" ", end=" ")
            else:
                print(node, end=" ")
        print()
    print()


def dijkstra(nodes, start_node, end_coords):
    dijkstra_nodes = []
    height = len(nodes)
    width = len(nodes[0])

    # init
    for y in range(height):
        dijkstra_row = []
        for x in range(width):
            if x == start_node.coords[0] and y == start_node.coords[1]:
                dijkstra_row.append(0)
                continue
            dijkstra_row.append(math.inf)
        dijkstra_nodes.append(dijkstra_row)

    visited = set()  # only coordinates
    queue = []  # whole Node objects
    heapq.heapify(queue)
    heapq.heappush(
        queue, (0, start_node.coords, start_node.can_visit))

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
    while len(queue) > 0:
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
            old_cost = dijkstra_nodes[next_y][next_x]
            current_cost = dijkstra_nodes[curr_y][curr_x]
            new_cost = current_cost + 1
            if old_cost > new_cost:
                dijkstra_nodes[next_y][next_x] = new_cost
                node_to_push = nodes[next_y][next_x]
                heapq.heappush(
                    possible_paths, (new_cost, node_to_push.coords, node_to_push.can_visit))
                is_in_queue[next_y][next_x] = True

            # determine whether can move to next node and if yes then push next node to queue
            can_move = next_node.coords not in visited and not is_in_queue[next_y][next_x]
            if can_move:
                node_to_push = nodes[next_y][next_x]
                heapq.heappush(
                    possible_paths, (new_cost, node_to_push.coords, node_to_push.can_visit))
                is_in_queue[next_y][next_x] = True
        queue += possible_paths

    return dijkstra_nodes[end_coords[1]][end_coords[0]]


def part_2(heightmap, nodes, end_coords):
    height = len(nodes)
    width = len(nodes[0])

    a_coords = []
    for y in range(height):
        for x in range(width):
            if heightmap[y+1][x+1] == 97:
                a_coords.append((x, y))

    shortest_lengths = []
    for coords in a_coords:
        start_node = nodes[coords[1]][coords[0]]
        shortest_lengths.append(dijkstra(nodes, start_node, end_coords))

    return min(shortest_lengths)


if __name__ == "__main__":
    parsed = parse_input()
    start = parsed["start"]
    end = parsed["end"]
    heightmap = parsed["heightmap"]

    width = len(heightmap[0])
    border_row = []
    BORDER_VALUE = 130  # random number that is > 123 (z = 122)
    for i in range(width + 2):
        border_row.append(BORDER_VALUE)
    # add border row at the top and bottom
    heightmap.insert(0, border_row)
    heightmap.append(border_row)
    # add border left and right
    for i in range(len(heightmap)):
        if i == 0 or i == len(heightmap) - 1:
            continue
        heightmap[i].insert(0, BORDER_VALUE)
        heightmap[i].append(BORDER_VALUE)

    nodes = get_nodes(heightmap)
    start_node = nodes[start[1]][start[0]]

    result_1 = dijkstra(nodes, start_node, end_coords=end)
    print("Part 1: ", result_1)

    result_2 = part_2(heightmap, nodes, end_coords=end)
    print("Part 2: ", result_2)
