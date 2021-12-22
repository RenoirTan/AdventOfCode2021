import sys
import typing as t
from tqdm import tqdm


MinMaxAxis = t.Tuple[int, int]
MinMaxCoordinates = t.Tuple[MinMaxAxis, MinMaxAxis, MinMaxAxis]
Instruction = t.Tuple[bool, MinMaxCoordinates]
Coordinates = t.Tuple[int, int, int]


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    instructions: t.List[Instruction] = []
    for line in fobj:
        state, mm_coordinates = line.split(" ")
        state = True if state == "on" else False
        mm_x, mm_y, mm_z = tuple(mm_coordinates.strip().split(","))
        min_x, max_x = tuple(mm_x[2:].split(".."))
        min_y, max_y = tuple(mm_y[2:].split(".."))
        min_z, max_z = tuple(mm_z[2:].split(".."))
        instruction = (
            state,
            (
                (int(min_x), int(max_x)),
                (int(min_y), int(max_y)),
                (int(min_z), int(max_z))
            )
        )
        instructions.append(instruction)
    initialization_grid: t.Set[Coordinates] = set()
    for index in iter(tqdm(range(len(instructions)), desc="Instruction")):
        turn_on, ((min_x, max_x), (min_y, max_y), (min_z, max_z)) = instructions[index]
        if max_x < -50 or min_x > 50 or max_y < -50 or min_y > 50 or max_z < -50 or min_z > 50:
            continue
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                for z in range(min_z, max_z+1):
                    if not (-50 <= x <= 50 and -50 <= y <= 50 and -50 <= z <= 50):
                        continue
                    if turn_on:
                        initialization_grid.add((x, y, z))
                    else:
                        if (x, y, z) in initialization_grid:
                            initialization_grid.remove((x, y, z))
    print(len(initialization_grid))
    return 0


main(sys.argv[1])
