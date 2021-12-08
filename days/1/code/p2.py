from functools import reduce
from io import TextIOWrapper
import typing as t
import sys


def sliding_window(
    depths: t.Iterable[int],
    window_length: int
) -> t.Generator[t.List[int], None, None]:
    window: t.List[int] = []
    for depth in depths:
        if len(window) == window_length:
            window.pop(0)
        window.append(depth)
        if len(window) == window_length:
            yield window.copy()


def pair_window_sums(
    window_sums: t.Iterable[int]
) -> t.Generator[t.Tuple[int, int], None, None]:
    prevsum: t.Optional[int] = None
    currsum: t.Optional[int] = None
    for window_sum in window_sums:
        prevsum = currsum
        currsum = window_sum
        if prevsum is not None and currsum is not None:
            yield prevsum, currsum


def main(filepath: str) -> int:
    fobj: TextIOWrapper = open(filepath, "r")
    window_sums = map(sum, sliding_window(map(int, fobj), 3))
    count: int = reduce(lambda c, p: c + int(p[1] > p[0]), pair_window_sums(window_sums), 0)
    print(count)
    return 0


main(sys.argv[1])
