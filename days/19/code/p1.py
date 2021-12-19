from __future__ import annotations
from collections import Counter
import sys
import typing as t
from tqdm import tqdm


# I could have used quarternions but I'm not smart enough to understand 3b1b
CUBE_ROTATIONS: t.List[str] = [
    "",
    "y1",
    "y2",
    "y3",
    "z2",
    "x2y1",
    "x2",
    "y1x2",
    "z3",
    "x1y3",
    "x2z1",
    "z3x3",
    "z1",
    "z1x1",
    "z1x2",
    "z1x3",
    "x1",
    "x1z1",
    "y2x1",
    "x1z3",
    "x3z3",
    "x1y2",
    "x3z1",
    "x3"
]


class Coordinates3D(object):
    def __init__(self, x: int = 0, y: int = 0, z: int = 0) -> None:
        self.x, self.y, self.z = x, y, z
        
    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"
    
    def __repr__(self) -> str:
        return f"Coordinates3D({str(self)})"
    
    def __eq__(self, other: Coordinates3D) -> bool:
        return all([
            self.x == other.x,
            self.y == other.y,
            self.z == other.z
        ])
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
        
    def copy(self) -> Coordinates3D:
        return Coordinates3D(self.x, self.y, self.z)
    
    def add(self, other: Coordinates3D) -> Coordinates3D:
        return Coordinates3D(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def negative(self) -> Coordinates3D:
        return Coordinates3D(-self.x, -self.y, -self.z)
    
    def subtract(self, other: Coordinates3D) -> Coordinates3D:
        return self.add(other.negative())
    
    def rotate(self, axis: str, right_angles: int) -> Coordinates3D:
        quarter_rotations: int = right_angles % 4
        if quarter_rotations == 0:
            return self.copy()
        if axis == "x":
            if quarter_rotations == 1:
                return Coordinates3D(self.x, -self.z, self.y)
            elif quarter_rotations == 2:
                return Coordinates3D(self.x, -self.y, -self.z)
            elif quarter_rotations == 3:
                return Coordinates3D(self.x, self.z, -self.y)
        elif axis == "y":
            if quarter_rotations == 1:
                return Coordinates3D(self.z, self.y, -self.x)
            elif quarter_rotations == 2:
                return Coordinates3D(-self.x, self.y, -self.z)
            elif quarter_rotations == 3:
                return Coordinates3D(-self.z, self.y, self.x)
        elif axis == "z":
            if quarter_rotations == 1:
                return Coordinates3D(-self.y, self.x, self.z)
            elif quarter_rotations == 2:
                return Coordinates3D(-self.x, -self.y, self.z)
            elif quarter_rotations == 3:
                return Coordinates3D(self.y, -self.x, self.z)
        else:
            raise ValueError(f"Invalid axis: {axis}")
    
    def rotate_by_str(self, transformations: str) -> Coordinates3D:
        result = self.copy()
        if len(transformations) > 0:
            for axis, right_angles in zip(transformations[:-1:2], transformations[1::2]):
                result = result.rotate(axis, int(right_angles))
        return result


class Scanner(object):
    def __init__(self, beacons: t.List[Coordinates3D]) -> None:
        self.beacons = beacons
        
    def __str__(self) -> str:
        return "Scanner(\n\t" + "\n\t".join(map(str, self.beacons)) + "\n)"

    def __repr__(self) -> str:
        return str(self)
    
    def n_beacons(self) -> int:
        return len(self.beacons)
        
    @classmethod
    def from_tuples(cls, tuples: t.Iterable[t.Tuple[int, int, int]]) -> Scanner:
        beacons = list(map(lambda coords: Coordinates3D(*coords), tuples))
        return cls(beacons)
    
    def rotate(self, axis: str, right_angles: int) -> Scanner:
        new_beacons = list(map(lambda coords: coords.rotate(axis, right_angles), self.beacons))
        return Scanner(new_beacons)
    
    def rotate_by_str(self, transformations: str) -> Scanner:
        new_beacons = list(map(lambda coords: coords.rotate_by_str(transformations), self.beacons))
        return Scanner(new_beacons)
    
    def rotate_by_24_axes(self) -> t.Generator[Scanner, None, None]:
        for transformation in CUBE_ROTATIONS:
            yield self.rotate_by_str(transformation)
    
    def find_overlapping(self, other: Scanner) -> t.Tuple[str, Coordinates3D, int]:
        rotation = ""
        offset = None
        encounters = 0
        for rotation_index, transformed_other in enumerate(other.rotate_by_24_axes()):
            offsets: Counter[Coordinates3D] = Counter()
            for this_beacon_index, this_beacon in enumerate(self.beacons):
                for other_beacon_index, other_beacon in enumerate(transformed_other.beacons):
                    offsets[this_beacon.subtract(other_beacon)] += 1
            current_rotation_most_common_offset = offsets.most_common(1)[0]
            if current_rotation_most_common_offset[1] > encounters:
                offset = current_rotation_most_common_offset[0].copy()
                encounters = current_rotation_most_common_offset[1]
                rotation = CUBE_ROTATIONS[rotation_index]
        return rotation, offset, encounters


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    scanners: t.List[t.Tuple[int, int, int]] = []
    for line in fobj:
        if line.strip() == "":
            continue
        elif line[:3] == "---":
            scanners.append([])
        else:
            coord = tuple(map(int, line.strip().split(",")))
            scanners[-1].append(coord)
    scanners: t.List[Scanner] = list(map(Scanner.from_tuples, scanners))
    progress_bar = iter(tqdm(range(len(scanners)**2)))
    contiguous: t.List[t.Tuple[int, int, int]] = []
    for a in range(len(scanners)):
        for b in range(len(scanners)):
            next(progress_bar)
            if a == b:
                continue
            rotation, offset, encounters = scanners[a].find_overlapping(scanners[b])
            if encounters >= 12:
                #print(a, b, rotation, repr(offset), encounters)
                contiguous.append((a, b, encounters))
    double_counted: t.Set[t.Tuple[int, int]] = set()
    total = sum(map(lambda s: s.n_beacons(), scanners))
    double_counts: int = 0
    for a, b, encounters in contiguous:
        if (a,b) in double_counted:
            continue
        else:
            double_counts += encounters
            double_counted.add((a,b))
            double_counted.add((b,a))
    print(total - double_counts)
    return 0


main(sys.argv[1])
