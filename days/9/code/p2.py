import sys
import typing as t


def find_low_points(matrix: t.List[t.List[t.Tuple[int, bool]]]) -> t.Generator[t.Tuple[int, int], None, None]:
    len_x = len(matrix[0])
    max_x = len_x - 1
    len_y = len(matrix)
    max_y = len_y - 1
    for y in range(len_y):
        for x in range(len_x):
            height = matrix[y][x][0]
            # Check top
            if y >= 1 and height >= matrix[y-1][x][0]:
                continue
            # Check bottom
            if y < max_y and height >= matrix[y+1][x][0]:
                continue
            # Check left
            if x >= 1 and height >= matrix[y][x-1][0]:
                continue
            # Check right
            if x < max_x and height >= matrix[y][x+1][0]:
                continue
            yield x, y


def generate_basins(
    matrix: t.List[t.List[t.Tuple[int, bool]]],
    height_limit: int
) -> t.Generator[t.List[t.Tuple[int, int]], None, None]:
    len_x = len(matrix[0])
    max_x = len_x - 1
    len_y = len(matrix)
    max_y = len_y - 1
    for low_point in find_low_points(matrix):
        x, y = low_point
        if matrix[y][x][1]:
            continue
        basin: t.List[t.Tuple[int, int]] = []
        queue: t.List[t.Tuple[int, int]] = [low_point]
        while len(queue) > 0:
            x, y = queue.pop(0)
            height = matrix[y][x][0]
            if matrix[y][x][1] or height >= height_limit:
                continue
            matrix[y][x] = (height, True)
            basin.append((x, y))
            # Check top
            if y >= 1 and not matrix[y-1][x][1] and matrix[y-1][x][0] > height:
                queue.append((x, y-1))
            # Check bottom
            if y < max_y and not matrix[y+1][x][1] and matrix[y+1][x][0] > height:
                queue.append((x, y+1))
            # Check left
            if x >= 1 and not matrix[y][x-1][1] and matrix[y][x-1][0] > height:
                queue.append((x-1, y))
            # Check right
            if x < max_x and not matrix[y][x+1][1] and matrix[y][x+1][0] > height:
                queue.append((x+1, y))
        yield basin


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    matrix = []
    for line in fobj:
        shmap = list(line.strip())
        ihmap = list(map(int, shmap))
        iphmap = list(map(lambda h: (h, False), ihmap))
        matrix.append(iphmap)
    basins = list(generate_basins(matrix, 9))
    basins.sort(key=len)
    lbasins = list(map(len, basins))
    print(basins)
    print(lbasins)
    return 0


main(sys.argv[1])