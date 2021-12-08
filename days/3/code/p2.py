from functools import reduce
import sys
import typing as t

# bit_index is counted from right to left (so the zeroeth bit is the smallest digit)


def bit_at(number: int, bit_index: int) -> int:
    return (number >> bit_index) & 1


def most_common_bit(numbers: t.List[int], bit_index: int) -> int:
    ones = sum(map(lambda number: bit_at(number, bit_index), numbers))
    n_nums = len(numbers)
    zeroes = n_nums - ones
    return int(ones >= zeroes)


def split_numbers(numbers: t.List[int], bit_index: int) -> t.Tuple[t.List[int], t.List[int]]:
    mcbit = most_common_bit(numbers, bit_index)
    # numbers with most common bit
    most = []
    least = []
    for number in numbers:
        if bit_at(number, bit_index) == mcbit:
            most.append(number)
        else:
            least.append(number)
    return most, least


def search_numbers(numbers: t.List[int]) -> t.Tuple[int, int]:
    word_width = len(bin(numbers[0])) - 2
    bit_index = word_width - 1
    most: t.List[int] = []
    least: t.List[int] = []
    while bit_index >= 0:
        if bit_index == word_width - 1:
            most, least = split_numbers(numbers, bit_index)
        else:
            if len(most) > 1:
                most = split_numbers(most, bit_index)[0]
            if len(least) > 1:
                least = split_numbers(least, bit_index)[1]
        bit_index -= 1
    return most[0], least[0]


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    core_dump = list(map(lambda v: int(v, base=2), fobj)) # List of numbers
    o2, co2 = search_numbers(core_dump)
    print(o2, co2)
    print(o2 * co2)
    return 0


main(sys.argv[1])
