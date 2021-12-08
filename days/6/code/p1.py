import sys
import typing as t


# Return list of lanternfish
def elapse_lanternfish(
    lanternfish: t.List[int],
    cooldown: int,
    puberty: int,
    days: int
) -> t.List[int]:
    for day in range(days):
        print(f"Day {day}/{days}")
        n_fish = len(lanternfish)
        for index in range(n_fish):
            if lanternfish[index] <= 0:
                lanternfish.append(puberty)
                lanternfish[index] += cooldown
            else:
                lanternfish[index] -= 1
    return lanternfish


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    lanternfish = list(map(int, fobj.readline().split(",")))
    result = elapse_lanternfish(lanternfish.copy(), 6, 8, 80)
    print(len(result))
    return 0


main(sys.argv[1])
