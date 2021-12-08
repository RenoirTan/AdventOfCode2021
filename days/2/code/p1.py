import sys


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    x, y = 0, 0
    for instruction in fobj:
        direction, magnitude = tuple(instruction.split(" "))
        magnitude = int(magnitude)
        if direction == "forward":
            x += magnitude
        elif direction == "up":
            y -= magnitude
        else:
            y += magnitude
    print(x, y)
    print(x*y)
    return 0


main(sys.argv[1])
