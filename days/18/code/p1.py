from __future__ import annotations
import sys
import typing as t


# I hate Python's typing system
class Pair(object):
    def __init__(
        self,
        left: t.Union[Pair, int],
        right: t.Union[Pair, int],
        parent: t.Optional[Pair] = None
    ) -> None:
        self.parent = parent
        self.left = left
        self.right = right
        if type(self.left) == Pair:
            self.left.parent = self
        if type(self.right) == Pair:
            self.right.parent = self
        
    def __str__(self) -> str:
        return f"[{str(self.left)},{str(self.right)}]"
    
    def __repr__(self) -> str:
        return str(self)
    
    def __add__(self, other: Pair) -> Pair:
        if other is None:
            return self
        else:
            return Pair(self, other)
    
    def __iadd__(self, other: t.Union[Pair, int]) -> None:
        left = Pair(self.left, self.right, self)
        if type(other) == Pair:
            other.parent = self
        return Pair(left, other, self.parent)
    
    def __contains__(self, pair: Pair) -> bool:
        if self == pair:
            return True
        ancestor = pair.parent
        while ancestor is not None:
            if ancestor == self:
                return True
            ancestor = ancestor.parent
        return False
    
    @classmethod
    def split(cls, number: int, parent: Pair = None) -> Pair:
        left = number // 2
        right = number - left
        return cls(left, right, parent)
    
    def depth(self) -> int:
        parent = self.parent
        depth = 0
        while parent is not None:
            depth += 1
            parent = parent.parent
        return depth
    
    def magnitude(self) -> int:
        left_value = self.left if type(self.left) == int else self.left.magnitude()
        right_value = self.right if type(self.right) == int else self.right.magnitude()
        return left_value*3 + right_value*2
    
    def get_root(self) -> Pair:
        ancestor = self
        while ancestor.parent is not None:
            ancestor = ancestor.parent
        return ancestor
    
    def get_leftmost_pair(self) -> Pair:
        left = self
        while type(left.left) == Pair:
            left = left.left
        #print(f"Leftmost Pair: {left}")
        return left
    
    def get_rightmost_pair(self) -> Pair:
        right = self
        while type(right.right) == Pair:
            right = right.right
        #print(f"Rightmost Pair: {right}")
        return right
    
    def is_leftmost(self) -> bool:
        parent = self.get_root()
        while type(parent.left) == Pair:
            parent = parent.left
        return self == parent
        
    def is_rightmost(self) -> bool:
        parent = self.get_root()
        while type(parent.right) == Pair:
            parent = parent.right
        return self == parent
    
    # Find the most recent ancestor from which the current pair descended leftward
    def find_mra_descend_left(self) -> t.Optional[Pair]:
        ancestor = self.parent
        current = self
        while ancestor is not None:
            if current == ancestor.left:
                return ancestor
            current = ancestor
            ancestor = ancestor.parent
        return None
    
    def find_mra_descend_right(self) -> t.Optional[Pair]:
        ancestor = self.parent
        current = self
        while ancestor is not None:
            if current == ancestor.right:
                return ancestor
            current = ancestor
            ancestor = ancestor.parent
        return None
    
    def reduce(self) -> Pair:
        reductions = -1
        count = 0
        print(f"Before reduction: {self}")
        while reductions != 0:
            reductions = self._reduce_me()
            count += 1
            print(f"Step {count}: {self}")
        return self
    
    def _reduce_me(self) -> int:
        depth = self.depth()
        print(f"Subpair: {self} @ Depth: {depth}")
        if depth >= 4 and type(self.left) == int and type(self.right) == int and self.left < 10 and self.right < 10:
            self._explode()
            return 1
        left_reduce, right_reduce = 0, 0
        if type(self.left) == Pair:
            left_reduce = self.left._reduce_me()
        else:
            if self.left >= 10:
                self.left = Pair.split(self.left, self)
                left_reduce += 1
        if left_reduce > 0:
            return left_reduce
        if type(self.right) == Pair:
            right_reduce = self.right._reduce_me()
        else:
            if self.right >= 10:
                self.right = Pair.split(self.right, self)
                right_reduce += 1
        if right_reduce > 0:
            return right_reduce
        return 0
    
    def _explode(self) -> None:
        #print(f"{self.parent=} {id(self.parent)=} {self.parent.depth()=}")
        mra_leftward = self.find_mra_descend_left()
        mra_rightward = self.find_mra_descend_right()
        if mra_leftward is not None:
            #print(f"{mra_leftward=} {id(mra_leftward)=} {mra_leftward.depth()=}")
            if type(mra_leftward.right) == int:
                #print("3")
                mra_leftward.right += self.right
            else:
                #print("4")
                leftmost_right = mra_leftward.right.get_leftmost_pair()
                leftmost_right.left += self.right
        if mra_rightward is not None:
            #print(f"{mra_rightward=} {id(mra_rightward)=} {mra_rightward.depth()=}")
            if type(mra_rightward.left) == int:
                #print("1")
                mra_rightward.left += self.left
            else:
                #print("2")
                rightmost_left = mra_rightward.left.get_rightmost_pair()
                rightmost_left.right += self.left
        #print(f"{self.parent=} {id(self.parent)=} {self.parent.depth()=}")
        if self == self.parent.left:
            self.parent.left = 0
        else:
            self.parent.right = 0


def make_snailfish_from_pseudo(pseudo: t.Any, parent: t.Optional[Pair]) -> Pair:
    pair = Pair(None, None, parent)
    left = pseudo[0] if type(pseudo[0]) == int else make_snailfish_from_pseudo(pseudo[0], pair)
    right = pseudo[1] if type(pseudo[1]) == int else make_snailfish_from_pseudo(pseudo[1], pair)
    pair.left = left
    pair.right = right
    return pair


def make_snailfish_from_raw(raw: str) -> Pair:    
    pseudo = eval(raw)
    return make_snailfish_from_pseudo(pseudo, None)


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    fiter = iter(fobj)
    snailfish = make_snailfish_from_raw(next(fiter).strip())
    for following in fiter:
        snailfish = snailfish + make_snailfish_from_raw(following.strip())
        snailfish.reduce()
    print(f"Final snailfish: {snailfish}\nFinal magnitude: {snailfish.magnitude()}")
    return 0


main(sys.argv[1])
