import sys
import typing as t


RIGHT_BRACKETS = {")", "]", "}", ">"}


RMATCHES = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}


SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}


def find_corrupt_bracket(line: str) -> t.Optional[str]:
    stack: t.List[str] = []
    for character in line:
        if character in {"(", "[", "{", "<"}:
            stack.append(character)
        elif character in RIGHT_BRACKETS:
            if stack[-1] != RMATCHES[character]:
                return character
            else:
                stack.pop(-1)
    return None


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    offenders = []
    for line in fobj:
        offending = find_corrupt_bracket(line)
        if offending is not None:
            offenders.append(offending)
    print(offenders)
    print(sum(map(lambda c: SCORES[c], offenders)))
    return 0


main(sys.argv[1])
