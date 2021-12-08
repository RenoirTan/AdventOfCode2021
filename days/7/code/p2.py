import sys
import typing as t


def required_fuel(distance: int) -> int:
    return (distance * distance + distance) // 2


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    crabs = list(map(int, fobj.readline().split(",")))
    cost_to_dests = [0] * (max(crabs) + 1)
    for dest in range(len(cost_to_dests)):
        for crab in crabs:
            cost_to_dests[dest] += required_fuel(abs(dest - crab))
    print(min(cost_to_dests))
    print(cost_to_dests.index(89647695))
    return 0


main(sys.argv[1])
