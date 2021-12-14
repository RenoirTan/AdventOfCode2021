from collections import Counter
import sys
import typing as t


def step(polymer: t.List[str], rules: t.Dict[str, str]) -> t.List[str]:
    inserts: t.List[str] = []
    for index in range(len(polymer) - 1):
        pair = "".join(polymer[index:index+2])
        inserts.append(rules[pair])
    for index, inserted in zip(range(1, 2*len(polymer) - 1, 2), inserts):
        polymer.insert(index, inserted)
    return polymer


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    fiter = iter(fobj)
    polymer: t.List[str] = list(next(fiter).strip())
    next(fiter)
    rules: t.Dict[str, str] = {}
    for line in fiter:
        pair, inserted = tuple(line.strip().split(" -> "))
        rules[pair] = inserted
    for _ in range(10):
        polymer = step(polymer, rules)
    counter = Counter(polymer)
    histogram = counter.most_common()
    print(histogram[0][1] - histogram[-1][1])
    return 0


main(sys.argv[1])
