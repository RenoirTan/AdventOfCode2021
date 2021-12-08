import sys
import typing as t


# Return histogram of fish timers
def elapse_lanternfish(
    lanternfish: t.List[int],
    cooldown: int,
    puberty: int,
    days: int
) -> t.List[int]:
    histogram = [0] * (max(cooldown, puberty) + 1)
    for fish in lanternfish:
        # Number of fish with the same age as this fish += 1
        histogram[fish] += 1
    for day in range(days):
        print(f"Day {day}/{days}")
        producers = histogram[0]
        histogram.pop(0)
        if puberty >= len(histogram):
            for _ in range(puberty - len(histogram)):
                histogram.append(0)
            histogram.insert(puberty, producers)
        else:
            histogram[puberty] += producers
        if cooldown >= len(histogram):
            for _ in range(cooldown - len(histogram)):
                histogram.append(0)
            histogram.insert(cooldown, producers)
        else:
            histogram[cooldown] += producers
    return histogram


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    lanternfish = list(map(int, fobj.readline().split(",")))
    result = elapse_lanternfish(lanternfish.copy(), 6, 8, 256)
    print(result, sum(result))
    return 0


main(sys.argv[1])
