import sys
import typing as t


def debug_matrix(matrix: t.List[t.List[bool]]) -> None:
    for row in matrix:
        print("".join(map(lambda d: "#" if d else ".", row)))
        

def fold_at(current_magnitude: int, fold_magnitude: int) -> int:
    return fold_magnitude - (current_magnitude - fold_magnitude)


def fold_x(matrix: t.List[t.List[bool]], magnitude: int) -> t.List[t.List[bool]]:
    len_x = len(matrix[0])
    len_y = len(matrix)
    excess_ontop = max(len_x - 1 - magnitude * 2, 0)
    for _ in range(excess_ontop):
        for y in range(len_y):
            matrix[y].insert(0, False)
    actual_magnitude = magnitude + excess_ontop
    for x in range(magnitude + 1, len_x):
        actual_x = x + excess_ontop
        fold_location = fold_at(actual_x, actual_magnitude)
        for y in range(len_y):
            matrix[y][fold_location] |= matrix[y][actual_x]
    for y in range(len_y):
        matrix[y] = matrix[y][:actual_magnitude]
    return matrix
    


def fold_y(matrix: t.List[t.List[bool]], magnitude: int) -> t.List[t.List[bool]]:
    len_x = len(matrix[0])
    len_y = len(matrix)
    excess_ontop = max(len_y - 1 - magnitude * 2, 0)
    for _ in range(excess_ontop):
        matrix.insert(0, [False for _ in range(len_x)])
    actual_magnitude = magnitude + excess_ontop
    for y in range(magnitude + 1, len_y):
        actual_y = y + excess_ontop
        fold_location = fold_at(actual_y, actual_magnitude)
        for x in range(len_x):
            matrix[fold_location][x] |= matrix[actual_y][x]
    return matrix[:actual_magnitude]
    


def fold_paper(matrix: t.List[t.List[bool]], axis: str, magnitude: int) -> t.List[t.List[bool]]:
    if axis == "x":
        return fold_x(matrix.copy(), magnitude)
    elif axis == "y":
        return fold_y(matrix.copy(), magnitude)
    else:
        raise ValueError(f"Unrecognised axis: {axis}")


def count_dots(matrix: t.List[t.List[bool]]) -> int:
    dots = 0
    for row in matrix:
        dots += sum(map(int, row))
    return dots


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    coordinates: t.List[t.Tuple[int, int]] = []
    instructions: t.List[t.Tuple[str, int]] = []
    state: int = 0
    for line in fobj:
        if line.strip() == "":
            state = 1
            continue
        if state == 0:
            x, y = tuple(line.strip().split(","))
            coordinates.append((int(x), int(y)))
        elif state == 1:
            axis, magnitude = line[11], line[13:].strip()
            instructions.append((axis, int(magnitude)))
    len_x = max(map(lambda c: c[0], coordinates)) + 1
    len_y = max(map(lambda c: c[1], coordinates)) + 1
    matrix: t.List[t.List[bool]] = [[False for _ in range(len_x)] for _ in range(len_y)]
    for x, y in coordinates:
        matrix[y][x] = True
    for axis, magnitude in instructions:
        matrix = fold_paper(matrix, axis, magnitude)
    debug_matrix(matrix)
    return 0


main(sys.argv[1])
