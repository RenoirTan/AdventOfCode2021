#!/usr/bin/env python

from functools import reduce
from io import TextIOWrapper
import typing as t
import sys

def pair_depths(fobj: TextIOWrapper) -> t.Generator[t.Tuple[int, int], None, None]:
    prevline: t.Optional[str] = None
    currline: t.Optional[str] = None
    for line in fobj:
        prevline = currline
        currline = line
        if prevline is not None and currline is not None:
            yield int(prevline), int(currline)
        

def main(filepath: str) -> int:
    fobj: TextIOWrapper = open(filepath, "r")
    count: int = reduce(lambda c, p: c + int(p[1] > p[0]), pair_depths(fobj), 0)
    print(count)
    return 0


main(sys.argv[1])
    