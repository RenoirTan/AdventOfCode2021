import sys
import typing as t


Image = t.Set[t.Tuple[int, int]]
ImageBoundary = t.Tuple[t.Tuple[int, int], t.Tuple[int, int]]


def image_boundaries(image: Image) -> ImageBoundary:
    min_x = float("inf")
    max_x = -float("inf")
    min_y = float("inf")
    max_y = -float("inf")
    for x, y in image:
        if x < min_x: min_x = x
        if x > max_x: max_x = x
        if y < min_y: min_y = y
        if y > max_y: max_y = y
    return (min_x, max_x), (min_y, max_y)


def pixel_index(image: Image, x: int, y: int) -> int:
    NEIGHBOURS: t.List[t.Tuple[int, int]] = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (0, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1)
    ]
    index = 0
    for dx, dy in NEIGHBOURS:
        index <<= 1
        nx, ny = x + dx, y + dy
        index |= (nx, ny) in image
    return index


def enhance(algorithm: str, original: Image, boundary: ImageBoundary) -> Image:
    result = set()
    (min_x, max_x), (min_y, max_y) = boundary
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            algo_index = pixel_index(original, x, y)
            if algorithm[algo_index] == "#":
                result.add((x, y))
    return result


def image_to_string(image: Image) -> str:
    if not image:
        return ""
    (min_x, max_x), (min_y, max_y) = image_boundaries(image)
    len_x = max_x - min_x + 1
    len_y = max_y - min_y + 1
    result = [["." for _x in range(len_x)] for _y in range(len_y)]
    for x, y in image:
        result[y-min_y][x-min_y] = "#"
    return "\n".join(map(lambda row: "".join(row), result))


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    fiter = iter(fobj)
    algorithm = next(fiter).strip()
    next(fiter)
    image: Image = set()
    for y, line in enumerate(fiter):
        for x, pixel in enumerate(line.strip()):
            if pixel == "#":
                image.add((x, y))
    (min_x, max_x), (min_y, max_y) = image_boundaries(image)
    # Thanks womogenes for giving me a bunch of values that work
    min_x -= 200
    max_x += 200
    min_y -= 200
    max_y += 200
    for _ in range(2):
        image = enhance(algorithm, image, ((min_x, max_x), (min_y, max_y)))
        min_x += 3
        max_x -= 3
        min_y += 3
        max_y -= 3
    print(len(image))
    return 0


main(sys.argv[1])
