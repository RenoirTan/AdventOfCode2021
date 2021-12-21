import sys
import typing as t

sys.setrecursionlimit(10**7)

# Sum of rolls: How many times you will get that sum in a round
DIE_ROLLS = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}


# Keys: Arguments to `play`
# Values: How many times player 0 or 1 won
GAME_WIN: t.Dict[t.Tuple[int, int, int, int, int], t.Tuple[int, int]] = {}


# Recursive function to add up all of the wins in this particular universe
def play(p0: int, p1: int, s0: int, s1: int, turn: int) -> t.Tuple[int, int]:
    game = p0, p1, s0, s1, turn
    # Check for any winners
    win_list = (0, 0)
    if s0 >= 21:
        return (1, 0)
    elif s1 >= 21:
        return (0, 1)
    # If you have seen this scenario before, return that value
    if game in GAME_WIN:
        return GAME_WIN[game]
    for first in range(1, 4):
        for second in range(1, 4):
            for third in range(1, 4):
                if turn == 0:
                    new_p0 = p0 + first + second + third
                    if new_p0 > 10:
                        new_p0 %= 10
                    new_s0 = s0 + new_p0
                    # Next player's turn
                    nr_w0, nr_w1 = play(new_p0, p1, new_s0, s1, 1)
                    win_list = win_list[0] + nr_w0, win_list[1] + nr_w1
                else:
                    new_p1 = p1 + first + second + third
                    if new_p1 > 10:
                        new_p1 %= 10
                    new_s1 = s1 + new_p1
                    nr_w0, nr_w1 = play(p0, new_p1, s0, new_s1, 0)
                    win_list = win_list[0] + nr_w0, win_list[1] + nr_w1
    GAME_WIN[game] = win_list
    return win_list


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    players: t.List[int] = []
    scores: t.List[int] = []
    for line in fobj:
        space_index = line.find(":") + 1
        players.append(int(line.strip()[space_index:]) - 1)
        scores.append(0)
    result = play(players[0], players[1], scores[0], scores[1], 0)
    print(result)
    return 0


main(sys.argv[1])
