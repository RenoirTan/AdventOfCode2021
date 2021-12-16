import sys
import typing as t


def _versum_literal(bit_rep: str) -> t.Tuple[int, int]:
    vsum = int(bit_rep[:3], base=2)
    end = 0
    for index in range(6, len(bit_rep), 5):
        end = index + 5
        if bit_rep[index] == "0":
            break
    return vsum, end


def _versum_6_0_subpackets(bit_rep: str, length: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    while end < length:
        vsum, delta_end = _versum(bit_rep[end:])
        total += vsum
        end += delta_end
    return total, length


def _versum_6_0(bit_rep: str) -> t.Tuple[int, int]:
    total = int(bit_rep[:3], base=2)
    length = int(bit_rep[7:22], base=2) # Length data starts at index 7 and is 15 bits long
    vsum, end = _versum_6_0_subpackets(bit_rep[22:], length)
    return total + vsum, end + 22


def _versum_6_1_subpackets(bit_rep: str, n_subpackets: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    for _ in range(n_subpackets):
        vsum, delta_end = _versum(bit_rep[end:])
        total += vsum
        end += delta_end
    return total, end


def _versum_6_1(bit_rep: str) -> t.Tuple[int, int]:
    total = int(bit_rep[:3], base=2)
    n_subpackets = int(bit_rep[7:18], base=2) # Count data starts at index 7 and is 11 bits long
    vsum, end = _versum_6_1_subpackets(bit_rep[18:], n_subpackets)
    return total + vsum, end + 18


def _versum(bit_rep: str) -> t.Tuple[int, int]:
    type_id = int(bit_rep[3:6], base=2)
    if type_id == 4: # Normal integer
        result = _versum_literal(bit_rep)
    else: # Operator
        if bit_rep[6] == "0":
            result = _versum_6_0(bit_rep)
        else:
            result = _versum_6_1(bit_rep)
    return result


def version_sum(packet: str) -> int:
    bit_rep = packet_hex_to_bin(packet)
    return _versum(bit_rep)[0]


HEXBIN_TABLE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}


def packet_hex_to_bin(packet: str) -> str:
    return "".join(map(lambda h: HEXBIN_TABLE[h], packet))


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    for index, line in enumerate(fobj):
        print(f"{index}: {version_sum(line.strip())}")
    return 0


main(sys.argv[1])
