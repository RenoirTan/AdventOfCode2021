import sys
import typing as t


CORRECT_SEGMENTS = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9"
}


SEGMENTS_REQUIRED = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    n_one = 0
    n_four = 0
    n_seven = 0
    n_eight = 0
    for line in fobj:
        splat = line.strip().split(" ")
        #digits = splat[0:10]
        screen = splat[11:]
        for unit in screen:
            if len(unit) == 2:
                n_one += 1
            elif len(unit) == 4:
                n_four += 1
            elif len(unit) == 3:
                n_seven += 1
            elif len(unit) == 7:
                n_eight += 1
    print(n_one, n_four, n_seven, n_eight)
    return 0


main(sys.argv[1])
