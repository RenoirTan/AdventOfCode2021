import sys
import typing as t


RIGHT_BRACKETS = {")", "]", "}", ">"}


RMATCHES = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}


LMATCHES = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}


SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

ASCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
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


def autocomplete(line: str) -> t.Optional[str]:
    stack: t.List[str] = []
    complete: t.List[str] = []
    for character in line:
        if character in {"(", "[", "{", "<"}:
            stack.append(character)
        elif character in RIGHT_BRACKETS:
            if stack[-1] != RMATCHES[character]:
                return None
            else:
                stack.pop(-1)
    for character in stack[::-1]:
        complete.append(LMATCHES[character])
    return "".join(complete)


def autocomplete_score(suggestion: str) -> int:
    score: int = 0
    for character in suggestion:
        score *= 5
        score += ASCORES[character]
    return score


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    incomplete = map(
        lambda line: line.strip(),
        filter(lambda line: find_corrupt_bracket(line) is None, fobj)
    )
    scores = []
    for l in incomplete:
        suggestion = autocomplete(l)
        score = autocomplete_score(suggestion)
        scores.append(score)
    scores.sort()
    print(scores[len(scores)//2])
    return 0


main(sys.argv[1])
