import sys
import typing as t


def main(filepath: str) -> int:
    with open(filepath, "r") as fobj:
        raw_config = fobj.readlines()
    return 0


main(sys.argv[1])
