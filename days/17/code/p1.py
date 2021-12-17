import sys
import typing as t
from tqdm import tqdm


SIMRES_OK: int = 0
SIMRES_XLEFT: int = 1
SIMRES_XRIGHT: int = 2
SIMRES_YUP: int = 3
SIMRES_YDOWN: int = 4


def simulate(
    usx: int, # Starting x-coordinate (u: start, s: displacement)
    usy: int, # Starting y-coordinate
    vx: int, # Starting x-velocity
    vy: int, # Starting y-velocity
    tx0: int, # 1st x-coordinate of the target area
    tx1: int, # 2nd x-coordinate of the target area
    ty0: int, # 1st y-coordinate of the target area
    ty1: int, # 2nd y-coordinate of the target area
    coord_out: t.Optional[t.List[t.Tuple[int, int]]] = None # List of coordinates
) -> int: # Whether the probe lands in the target
    
    # acceleration function
    def af(vx: int, vy: int) -> t.Tuple[int, int]:
        if vx < 0:
            vx += 1
        elif vx > 0:
            vx -= 1
        vy -= 1
        return vx, vy
    
    sx, sy = usx, usy
    if tx0 > tx1:
        tx0, tx1 = tx1, tx0
    if ty0 > ty1:
        ty0, ty1 = ty1, ty0
        
    if coord_out is not None:
        coord_out.append((sx, sy))
    
    while (not (tx0 <= sx <= tx1)) or (not (ty0 <= sy <= ty1)):
        if sy < ty0 and vy < 0:
            return SIMRES_YDOWN
        if sx < tx0 and vx < 0:
            return SIMRES_XLEFT
        if sx > tx1 and vx > 0:
            return SIMRES_XRIGHT
        
        sx += vx
        sy += vy
        vx, vy = af(vx, vy)
        if coord_out is not None:
            coord_out.append((sx, sy))
    return SIMRES_OK


def triangular(x: int) -> int:
    return x * (x+1) // 2


def guess(
    uvx0: int,
    uvx1: int,
    uvy0: int,
    uvy1: int,
    tx0: int,
    tx1: int,
    ty0: int,
    ty1: int
) -> int:
    pbar = iter(tqdm(range((uvx1-uvx0) * (uvy1-uvy0)), desc="Testing simulations"))
    possible: t.List[int] = []
    for vx in range(uvx0, uvx1):
        for vy in range(uvy0, uvy1):
            next(pbar)
            coord_out = []
            result = simulate(0, 0, vx, vy, tx0, tx1, ty0, ty1, coord_out)
            if result == 0:
                possible.append(max(map(lambda coord: coord[1], coord_out)))
    return max(possible)


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    line = fobj.readline().strip()[13:].split(", ")
    fobj.close()
    xline, yline = line[0][2:], line[1][2:]
    tx0, tx1 = tuple(map(int, xline.split("..")))
    ty0, ty1 = tuple(map(int, yline.split("..")))
    print(guess(0, 1000, 0, 1000, tx0, tx1, ty0, ty1))
    return 0


main(sys.argv[1])
