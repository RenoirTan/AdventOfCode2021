import sys
import typing as t


def find_low_points(matrix: t.List[t.List[int]]) -> t.Generator[int, None, None]:
    len_x = len(matrix[0])
    max_x = len_x - 1
    len_y = len(matrix)
    max_y = len_y - 1
    for y in range(len_y):
        for x in range(len_x):
            height = matrix[y][x]
            # Check top
            if y >= 1 and height >= matrix[y-1][x]:
                continue
            # Check bottom
            if y < max_y and height >= matrix[y+1][x]:
                continue
            # Check left
            if x >= 1 and height >= matrix[y][x-1]:
                continue
            # Check right
            if x < max_x and height >= matrix[y][x+1]:
                continue
            yield height


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    matrix = []
    for line in fobj:
        shmap = list(line.strip())
        ihmap = list(map(int, shmap))
        matrix.append(ihmap)
    print(sum(map(lambda lp: lp+1, find_low_points(matrix))))
    return 0


main(sys.argv[1])
