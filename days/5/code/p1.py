import sys
import typing as t

def create_matrix(x: int, y: int) -> t.List[t.List[int]]:
    return [[0 for _ in range(x)] for _ in range(y)]


def slap_line_onto_matrix(
    matrix: t.List[t.List[int]],
    a: t.Tuple[int, int],
    b: t.Tuple[int, int]
) -> bool:
    if a[0] == b[0]:
        x = a[0]
        min_y = min(a[1], b[1]+1)
        max_y = max(a[1], b[1]+1)
        for y in range(min_y, max_y):
            matrix[y][x] += 1
        return True
    elif a[1] == b[1]:
        y = a[1]
        min_x = min(a[0], b[0]+1)
        max_x = max(a[0], b[0]+1)
        for x in range(min_x, max_x):
            matrix[y][x] += 1
        return True
    return False


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    inputs: t.List[t.Tuple[t.Tuple[int, int], t.Tuple[int, int]]] = []
    for rawline in fobj:
        a, b = tuple(rawline.split(" -> "))
        a = a.split(",")
        b = b.split(",")
        a = int(a[0]), int(a[1])
        b = int(b[0]), int(b[1])
        inputs.append((a, b))
    matrix_size = [0, 0]
    for (ax, ay), (bx, by) in inputs:
        matrix_size[0] = max(matrix_size[0], ax, bx)
        matrix_size[1] = max(matrix_size[1], ay, by)
    matrix = create_matrix(matrix_size[0]+1, matrix_size[1]+1)
    for a, b in inputs:
        slap_line_onto_matrix(matrix, a, b)
    dangerous = 0
    for row in matrix:
        for grid in row:
            if grid >= 2:
                dangerous += 1
    print(dangerous)
    return 0


main(sys.argv[1])
