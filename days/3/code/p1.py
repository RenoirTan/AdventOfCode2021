from functools import reduce
import sys
import typing as t


def lm_bits(word_stream: t.Iterable[str], word_width_hint: int = -1) -> t.Tuple[t.List[int], t.List[int]]:
    word_width = word_width_hint
    n_one_word = [0] * max(word_width, 0)
    word_count = 0
    for word in word_stream:
        word = word.strip() # Get rid of trailing new line
        if word_width < 0:
            word_width = len(word)
            n_one_word = [0] * word_width
        for index, bit in enumerate(word):
            n_one_word[index] += int(bit == "1")
        word_count += 1
    
    def _ones_exceed_zeroes(n_one: int, word_count: int) -> int:
        n_zero = word_count - n_one
        if n_zero == n_one:
            raise ValueError("cannot resolve n_zero == n_one is true")
        return int(n_one > n_zero)

    def _l_from_m(m_bits: t.List[int]) -> t.List[int]:
        l_bits = []
        for bit in m_bits:
            l_bits.append(int(not bool(bit)))
        return l_bits
    
    m_bits = list(map(lambda n_one: _ones_exceed_zeroes(n_one, word_count) , n_one_word))
    return m_bits, _l_from_m(m_bits)


def bits_to_int(bits: t.Iterable[int]) -> int:
    return reduce(lambda result, bit: (result << 1) | bit, bits, 0)


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    m_bits, l_bits = lm_bits(fobj)
    print(m_bits, l_bits)
    gamma_rate = bits_to_int(m_bits)
    epsilon_rate = bits_to_int(l_bits)
    print(gamma_rate, epsilon_rate)
    print(gamma_rate * epsilon_rate)
    return 0


main(sys.argv[1])
