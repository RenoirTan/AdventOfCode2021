from __future__ import annotations
from collections import Counter
import sys
import typing as t


def generate_pairs(template: str) -> Counter[str]:
    pairs: Counter[str] = Counter()
    for first, second in zip(template[:-1], template[1:]):
        pair = first + second
        pairs[pair] += 1
    return pairs


class Polymer(object):
    def __init__(self, template: str) -> None:
        polymer = list(template.strip())
        self.elements = Counter(polymer)
        self.pairs = generate_pairs(template)
    
    def __str__(self) -> str:
        return f"Polymer Elements: {self.elements.most_common()}\nPolymer Pairs: {self.pairs.most_common()}"
    
    def step(self, rules: t.Dict[str, str]) -> Polymer:
        pairs_delta = Counter()
        elements_delta = Counter()
        for pair, count in self.pairs.most_common():
            first = pair[0]
            last = pair[-1]
            middle = rules[pair]
            pairs_delta[first+middle] += count
            pairs_delta[middle+last] += count
            pairs_delta[first+last] -= count
            elements_delta[middle] += count
        self.pairs += pairs_delta
        self.elements += elements_delta
        return self


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    fiter = iter(fobj)
    template = next(fiter).strip()
    polymer = Polymer(template)
    next(fiter)
    rules: t.Dict[str, str] = {}
    for line in fiter:
        pair, inserted = tuple(line.strip().split(" -> "))
        rules[pair] = inserted
    for _ in range(40):
        polymer.step(rules)
    histogram = polymer.elements.most_common()
    print(histogram[0][1] - histogram[-1][1])
    return 0


main(sys.argv[1])
