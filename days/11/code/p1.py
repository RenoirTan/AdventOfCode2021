from __future__ import annotations
from functools import reduce
import sys
import typing as t


T = t.TypeVar("T")


NEIGHBOURS: t.List[t.Tuple[int, int]] = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]


def debug_matrix(thing: t.List[t.List[T]]) -> None:
    for row in thing:
        print(row)


def add_one(octopi: t.List[t.List[int]]) -> None:
    for y in range(len(octopi)):
        for x in range(len(octopi[y])):
            octopi[y][x] += 1
    return None


def reset_flashed(flashed: t.List[t.List[bool]]) -> None:
    for y in range(len(flashed)):
        for x in range(len(flashed[y])):
            flashed[y][x] = False
    return None


def must_repeat(octopi: t.List[t.List[int]], flashed: t.List[t.List[bool]], threshold: int) -> True:
    must = False
    for y in range(len(octopi)):
        for x in range(len(octopi[y])):
            if octopi[y][x] > threshold and not flashed[y][x]:
                must = True
    return must


def step(octopi: t.List[t.List[int]], flashed: t.List[t.List[bool]], threshold: int) -> int:
    reset_flashed(flashed)
    add_one(octopi)
    flashes = 0
    while must_repeat(octopi, flashed, threshold):
        for y in range(len(octopi)):
            for x in range(len(octopi[y])):
                if octopi[y][x] > threshold and not flashed[y][x]:
                    flashed[y][x] = True
                    for dx, dy in NEIGHBOURS:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < len(octopi[y]) and 0 <= ny < len(octopi):
                            octopi[ny][nx] += 1
    for y in range(len(octopi)):
        for x in range(len(octopi[y])):
            if flashed[y][x]:
                flashes += 1
                octopi[y][x] = 0
    return flashes


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    octopi: t.List[t.List[int]] = []
    flashed: t.List[t.List[bool]] = []
    for line in fobj:
        octopi.append(list(map(int, list(line.strip()))))
        flashed.append([False for _ in range(len(octopi[-1]))])
    total_flashes = 0
    for i in range(100):
        flashes = step(octopi, flashed, 9)
        print(i, flashes)
        total_flashes += flashes
    print(total_flashes)
    return 0


main(sys.argv[1])
