import sys
import typing as t


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    crabs = list(map(int, fobj.readline().split(",")))
    cost_to_dests = [0] * (max(crabs) + 1)
    for dest in range(len(cost_to_dests)):
        for crab in crabs:
            cost_to_dests[dest] += abs(dest - crab)
    print(min(cost_to_dests))
    return 0


main(sys.argv[1])
