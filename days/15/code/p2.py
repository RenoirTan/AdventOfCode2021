from __future__ import annotations
import sys
import typing as t


def debug_matrix(matrix: t.List[t.List[int]]) -> None:
    for row in matrix:
        print("".join(map(str, row)))


class NodeCost(object):
    def __init__(self, x: int, y: int, cost: int) -> None:
        self.node = x, y
        self.cost = cost

    def __lt__(self, other: NodeCost) -> bool:
        return self.cost < other.cost
    
    def __le__(self, other: NodeCost) -> bool:
        return self.cost <= other.cost
    
    def __eq__(self, other: NodeCost) -> bool:
        return self.cost == other.cost
    
    def __gt__(self, other: NodeCost) -> bool:
        return self.cost > other.cost
    
    def __ge__(self, other: NodeCost) -> bool:
        return self.cost >= other.cost
    

NEIGHBOURS = [
    (0, -1),
    (-1, 0),
    (1, 0),
    (0, 1)
]


def dijkstra(matrix: t.List[t.List[int]], x: int, y: int) -> t.List[t.List[t.Optional[int]]]:
    len_y = len(matrix)
    len_x = len(matrix[0])
    priority_queue: t.List[NodeCost] = [NodeCost(x, y, 0)]
    distances: t.List[t.List[t.Optional[int]]] = []
    for y in range(len_y):
        distances.append([None] * len_x)
    distances[y][x] = 0
    while len(priority_queue) > 0:
        current_node_cost = priority_queue.pop(0)
        cx, cy = current_node_cost.node
        ccost = current_node_cost.cost
        for dx, dy in NEIGHBOURS:
            ax, ay = cx + dx, cy + dy
            if not (0 <= ax < len_x and 0 <= ay < len_y):
                continue
            if distances[ay][ax] is None or distances[ay][ax] > ccost + matrix[ay][ax]:
                distances[ay][ax] = ccost + matrix[ay][ax]
                priority_queue.append(NodeCost(ax, ay, distances[ay][ax]))
                priority_queue.sort()
    return distances


def wrap(value: int, limit: int, lowest: int) -> int:
    return lowest + (value % limit) - 1 if value > limit else value


def clone_2d(original: t.List[t.List[int]]) -> t.List[t.List[int]]:
    result = []
    for row in original:
        result.append(row.copy())
    return result


def extend_matrix(original: t.List[t.List[int]], nx: int, ny: int, limit: int, lowest: int) -> t.List[t.List[int]]:
    olen_y = len(original)
    olen_x = len(original[0])
    result = clone_2d(original)
    for mx in range(nx):
        for my in range(ny):
            if my + mx == 0:
                continue
            clone = clone_2d(original)
            for y in range(olen_y):
                for x in range(olen_x):
                    clone[y][x] = wrap(clone[y][x]+my+mx, limit, lowest)
            if mx == 0:
                for _ in range(olen_y):
                    result.append([])
            for y in range(olen_y):
                sy = y + my*olen_y
                result[sy].extend(clone[y])
    return result


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    matrix: t.List[t.List[int]] = []
    for line in fobj:
        matrix.append(list(map(int, line.strip())))
    matrix = extend_matrix(matrix, 5, 5, 9, 1)
    distances = dijkstra(matrix, 0, 0)
    print(distances[-1][-1])
    return 0


main(sys.argv[1])
