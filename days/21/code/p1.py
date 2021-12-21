import sys
import typing as t


DIE_VALUES = [i+1 for i in range(100)]
SPACE_VALUES = [i+1 for i in range(10)]


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    players: t.List[int] = []
    scores: t.List[int] = []
    for line in fobj:
        space_index = line.find(":") + 1
        players.append(int(line.strip()[space_index:]) - 1)
        scores.append(0)
    die = 0
    rolls = 0
    player = 0
    while True:
        forwards = 0
        die %= 100
        forwards += DIE_VALUES[die]
        die += 1
        die %= 100
        forwards += DIE_VALUES[die]
        die += 1
        die %= 100
        forwards += DIE_VALUES[die]
        die += 1
        rolls += 3
        players[player] += forwards
        players[player] %= 10
        scores[player] += SPACE_VALUES[players[player]]
        if scores[player] >= 1000:
            break
        player += 1
        player %= len(players)
    print(rolls, min(scores), rolls * min(scores))
    return 0


main(sys.argv[1])
