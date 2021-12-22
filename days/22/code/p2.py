# DOES NOT WORK

from __future__ import annotations
import sys
import typing as t
from tqdm import tqdm


MinMaxAxis = t.Tuple[int, int]
MinMaxCoordinates = t.Tuple[MinMaxAxis, MinMaxAxis, MinMaxAxis]
Instruction = t.Tuple[bool, MinMaxCoordinates]
Coordinates = t.Tuple[int, int, int]


class Cuboid(object):
    def __init__(
        self,
        min_x: int,
        max_x: int,
        min_y: int,
        max_y: int,
        min_z: int,
        max_z: int
    ) -> None:
        assert min_x <= max_x
        assert min_y <= max_y
        assert min_z <= max_z
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z
    
    def __eq__(self, other: Cuboid) -> bool:
        return (
            self.min_x == other.min_x and
            self.max_x == other.max_x and
            self.min_y == other.min_y and
            self.max_y == other.max_y and
            self.min_z == other.min_z and
            self.max_z == other.max_z
        )
    
    def __and__(self, other: Cuboid) -> Cuboid:
        return self.intersect(other)
    
    def __int__(self) -> int:
        return self.volume()
    
    def __str__(self) -> str:
        return f"Cuboid(x={self.min_x}..{self.max_x},y={self.min_y}..{self.max_y},z={self.min_z}..{self.max_z})"
    
    def __repr__(self) -> str:
        return str(self)
    
    def copy(self) -> Cuboid:
        return Cuboid(self.min_x, self.max_x, self.min_y, self.max_y, self.min_z, self.max_z)
    
    def volume(self) -> int:
        return (self.max_x-self.min_x) * (self.max_y-self.min_y) * (self.max_z-self.min_z)
    
    @staticmethod
    def total_volume(cuboids: t.List[Cuboid]) -> int:
        total = sum(map(lambda c: c.volume(), cuboids))
        for i in range(len(cuboids)):
            for j in range(i+1, len(cuboids)):
                total -= cuboids[i].intersect(cuboids[j]).volume()
        return total
    
    def intersect(self, other: Cuboid) -> Cuboid:
        min_x = max(min(self.max_x, other.min_x), self.min_x)
        max_x = max(min(self.max_x, other.max_x), self.min_x)
        min_y = max(min(self.max_y, other.min_y), self.min_y)
        max_y = max(min(self.max_y, other.max_y), self.min_y)
        min_z = max(min(self.max_z, other.min_z), self.min_z)
        max_z = max(min(self.max_z, other.max_z), self.min_z)
        return Cuboid(min_x, max_x, min_y, max_y, min_z, max_z)
    
    def slice_off(self, other: Cuboid) -> t.List[Cuboid]:
        zone = self.intersect(other)
        # Base case
        if zone.volume() == 0:
            return [self.copy()]
        elif self == zone:
            return []
        result = []
        # Remaining contains the remainder of a cube after one shave (including the "zone")
        remaining: t.Optional[Cuboid] = None
        if zone.min_x > self.min_x:
            a = Cuboid(self.min_x, zone.min_x, self.min_y, self.max_y, self.min_z, self.max_z)
            remaining = Cuboid(zone.min_x, self.max_x, self.min_y, self.max_y, self.min_z, self.max_z)
            result.append(a)
        elif zone.max_x < self.max_x:
            a = Cuboid(zone.max_x, self.max_x, self.min_y, self.max_y, self.min_z, self.max_z)
            remaining = Cuboid(self.min_x, zone.max_x, self.min_y, self.max_y, self.min_z, self.max_z)
            result.append(a)
        elif zone.min_y > self.min_y:
            a = Cuboid(self.min_x, self.max_x, self.min_y, zone.min_y, self.min_z, self.max_z)
            remaining = Cuboid(self.min_x, self.max_x, zone.min_y, self.max_y, self.min_z, self.max_z)
            result.append(a)
        elif zone.max_y < self.max_y:
            a = Cuboid(self.min_x, self.max_x, zone.max_y, self.max_y, self.min_z, self.max_z)
            remaining = Cuboid(self.min_x, self.max_x, self.min_y, zone.max_y, self.min_z, self.max_z)
            result.append(a)
        elif zone.min_z > self.min_z:
            a = Cuboid(self.min_x, self.max_x, self.min_y, self.max_y, self.min_z, zone.min_z)
            remaining = Cuboid(self.min_x, self.max_x, self.min_y, self.max_y, zone.min_z, self.max_z)
            result.append(a)
        elif zone.max_z < self.max_z:
            a = Cuboid(self.min_x, self.max_x, self.min_y, self.max_y, zone.max_z, self.max_z)
            remaining = Cuboid(self.min_x, self.max_x, self.min_y, self.max_y, self.min_z, zone.max_z)
            result.append(a)
        # Recursion
        if remaining is not None:
            result.extend(remaining.slice_off(zone))
        return result


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
    grid: t.List[Cuboid] = []
    for index in iter(tqdm(range(len(instructions)), desc="Instruction")):
        turn_on, ((min_x, max_x), (min_y, max_y), (min_z, max_z)) = instructions[index]
        cuboid = Cuboid(min_x, max_x+1, min_y+1, max_y+1, min_z, max_z+1)
        if turn_on:
            grid.append(cuboid)
        else:
            new_grid = []
            while len(grid) > 0:
                existing = grid.pop()
                shaves = existing.slice_off(cuboid)
                #print(f"{existing} - {cuboid} = {shaves}")
                new_grid.extend(shaves)
            grid = new_grid
    print(Cuboid.total_volume(grid))
    return 0


main(sys.argv[1])
