from __future__ import annotations
from io import TextIOWrapper
import sys
import typing as t


class BingoCell(object):
    def __init__(self, value: int, marked: bool = False) -> None:
        self.value: int = value
        self.marked: bool = marked
    
    def __str__(self) -> str:
        return str(self.value) + ("+" if self.marked else "-")

    def __repr__(self) -> str:
        return str(self.value) + ("+" if self.marked else "-")
    
    def mark(self) -> BingoCell:
        self.marked = True
        return self


class BingoBoard(object):
    def __init__(self, board: t.Optional[t.List[t.List[int]]] = None) -> None:
        if board is None:
            _board: t.List[t.List[int]] = [[0] * 5] * 5
        else:
            _board = board
        self.board: t.List[t.List[BingoCell]] = []
        for y in range(5):
            self.board.append([])
            for x in range(5):
                self.board[y].append(BingoCell(_board[y][x], False))
        
    def __str__(self) -> str:
        return str(self.board)
                
    def get_cell(self, x: int, y: int) -> BingoCell:
        return self.board[y][x]

    def mark_cell_with_value(self, value: int) -> t.Optinal[BingoCell]:
        for y in range(5):
            for x in range(5):
                cell = self.get_cell(x, y)
                if cell.value == value:
                    return cell.mark()
        return None

    def check_for_bingo(self) -> t.Tuple[t.Optional[int], t.Optional[int]]:
        # scan horizontally first
        for y in range(5):
            if all(map(lambda cell: cell.marked, self.board[y])):
                return None, y
        # scan vertically
        for x in range(5):
            bingo: bool = True
            for y in range(5):
                if not self.get_cell(x, y).marked:
                    bingo = False
                    break
            if bingo:
                return x, None
        return None, None
    
    def calculate_score(self) -> int:
        score: int = 0
        for y in range(5):
            for x in range(5):
                cell = self.get_cell(x, y)
                if not cell.marked:
                    score += cell.value
        return score


def get_one_board(fobj: TextIOWrapper) -> BingoBoard:
    board = []
    for lines, line in enumerate(fobj):
        if line.strip() == "":
            if lines == 0:
                continue
            else:
                break
        row = list(map(int, filter(lambda raw: not raw.strip() == "", line.split(" "))))
        board.append(row)
    return BingoBoard(board)


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    calls: t.List[str] = fobj.readline().strip().split(",")
    print(calls)
    boards: t.List[t.Tuple[BingoBoard, bool]] = []
    while True:
        try:
            board = get_one_board(fobj)
        except:
            break
        else:
            boards.append((board, False))
    winners: t.List[int] = []
    winning_calls: t.List[int] = []
    for call in calls:
        call = int(call)
        for index, (board, bingoed) in enumerate(boards):
            if bingoed:
                continue
            board.mark_cell_with_value(call)
            bingo_check = board.check_for_bingo()
            if bingo_check != (None, None):
                boards[index] = (board, True)
                winners.append(index)
                winning_calls.append(call)
    last_winner = boards[winners[-1]][0]
    score = last_winner.calculate_score()
    call = winning_calls[-1]
    print(str(last_winner), score, call, score * call)
    return 0


main(sys.argv[1])
