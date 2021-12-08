import sys
import typing as t


CORRECT_SEGMENTS = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9"
}


COMMON_SEGMENTS = {
    "a": 8,
    "b": 6,
    "c": 8,
    "d": 7,
    "e": 4,
    "f": 9,
    "g": 7
}


SEGMENTS_REQUIRED = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]


def sort_segments_alphabetically(digit: str) -> str:
    segments = sorted(list(digit))
    return "".join(segments)


def a_is_subset_of_b(a: str, b: str) -> bool:
    return all(map(lambda segment: segment in b, a))


# The 6-segment digit that shares segments with 1 are 0,9.
# The remaining 6-segment digit is 6.
# The 5-segment digit that shares all of its segments with 6 is 5.
# If one of the remaining 5-segment digits shares all of its segments with one of the 2 unknown 6-segment digits,
#   the 5-segment digit is 3 and the 6-segment digit is 9.
# The remaining 6-segment digit is 0.
# The last 5-segment digit is 2.
def check_digits(digits: t.List[str]) -> t.List[str]:
    for index in range(len(digits)):
        digits[index] = sort_segments_alphabetically(digits[index])
    digits.sort(key=len)
    six_segment_digits = list(filter(lambda digit: len(digit) == 6, digits))
    five_segment_digits = list(filter(lambda digit: len(digit) == 5, digits))
    digit_one = digits[0]
    digit_four = digits[2]
    digit_seven = digits[1]
    digit_eight = digits[9]
    digit_six = None
    digit_six_index = None
    for segment in digit_one:
        for index, six_segment_digit in enumerate(six_segment_digits):
            if segment not in six_segment_digit:
                digit_six = six_segment_digit
                digit_six_index = index
    digit_zero_nine = []
    for possible_index in range(len(six_segment_digits)):
        if possible_index != digit_six_index:
            digit_zero_nine.append(six_segment_digits[possible_index])
    digit_five = None
    digit_five_index = None
    for index, five_segment_digit in enumerate(five_segment_digits):
        if a_is_subset_of_b(five_segment_digit, digit_six):
            digit_five = five_segment_digit
            digit_five_index = index
    digit_two_three = []
    for possible_index in range(len(five_segment_digits)):
        if possible_index != digit_five_index:
            digit_two_three.append(five_segment_digits[possible_index])
    digit_three = None
    digit_three_index = None
    digit_nine = None
    digit_nine_index = None
    for index5, five_segment_digit in enumerate(digit_two_three):
        for index6, six_segment_digit in enumerate(digit_zero_nine):
            if a_is_subset_of_b(five_segment_digit, six_segment_digit):
                digit_three = five_segment_digit
                digit_three_index = index5
                digit_nine = six_segment_digit
                digit_nine_index = index6
    digit_two = digit_two_three[int(not bool(digit_three_index))]
    digit_zero = digit_zero_nine[int(not bool(digit_nine_index))]
    return [
        digit_zero,
        digit_one,
        digit_two,
        digit_three,
        digit_four,
        digit_five,
        digit_six,
        digit_seven,
        digit_eight,
        digit_nine
    ]


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    total = 0
    for line in fobj:
        splat = line.strip().split(" ")
        digits = splat[0:10]
        screen = splat[11:]
        checked_digits = check_digits(digits)
        value = 0
        for unit in screen:
            value *= 10
            abc_unit = sort_segments_alphabetically(unit)
            value += checked_digits.index(abc_unit)
        total += value
    print(total)
    return 0


main(sys.argv[1])
