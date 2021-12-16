import sys
import typing as t


DEPTH: int = 0


def _eval_0_0(bit_rep: str, length: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    while end < length:
        vsum, dend = _eval_packet(bit_rep[end:])
        total += vsum
        end += dend
    return total, length


def _eval_0_1(bit_rep: str, n_subpackets: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    for _ in range(n_subpackets):
        vsum, dend = _eval_packet(bit_rep[end:])
        total += vsum
        end += dend
    return total, end


# Sum
def _eval_0(bit_rep: str, len_id: int, count: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    if len_id == 0:
        total, end = _eval_0_0(bit_rep[22:], count)
        end += 22
    else:
        total, end = _eval_0_1(bit_rep[18:], count)
        end += 18
    return total, end


def _eval_1_0(bit_rep: str, length: int) -> t.Tuple[int, int]:
    total = 1
    end = 0
    while end < length:
        vsum, dend = _eval_packet(bit_rep[end:])
        total *= vsum
        end += dend
    return total, length


def _eval_1_1(bit_rep: str, n_subpackets: int) -> t.Tuple[int, int]:
    total = 1
    end = 0
    for _ in range(n_subpackets):
        vsum, dend = _eval_packet(bit_rep[end:])
        total *= vsum
        end += dend
    return total, end


# Product
def _eval_1(bit_rep: str, len_id: int, count: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    if len_id == 0:
        total, end = _eval_1_0(bit_rep[22:], count)
        end += 22
    else:
        total, end = _eval_1_1(bit_rep[18:], count)
        end += 18
    return total, end


def _eval_2_0(bit_rep: str, length: int) -> t.Tuple[int, int]:
    total = None
    end = 0
    while end < length:
        vsum, dend = _eval_packet(bit_rep[end:])
        if total is None or vsum < total:
            total = vsum
        end += dend
    return total, length


def _eval_2_1(bit_rep: str, n_subpackets: int) -> t.Tuple[int, int]:
    total = None
    end = 0
    for _ in range(n_subpackets):
        vsum, dend = _eval_packet(bit_rep[end:])
        if total is None or vsum < total:
            total = vsum
        end += dend
    return total, end


# Minimum
def _eval_2(bit_rep: str, len_id: int, count: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    if len_id == 0:
        total, end = _eval_2_0(bit_rep[22:], count)
        end += 22
    else:
        total, end = _eval_2_1(bit_rep[18:], count)
        end += 18
    return total, end


def _eval_3_0(bit_rep: str, length: int) -> t.Tuple[int, int]:
    total = None
    end = 0
    while end < length:
        vsum, dend = _eval_packet(bit_rep[end:])
        if total is None or vsum > total:
            total = vsum
        end += dend
    return total, length


def _eval_3_1(bit_rep: str, n_subpackets: int) -> t.Tuple[int, int]:
    total = None
    end = 0
    for _ in range(n_subpackets):
        vsum, dend = _eval_packet(bit_rep[end:])
        if total is None or vsum > total:
            total = vsum
        end += dend
    return total, end


# Maximum
def _eval_3(bit_rep: str, len_id: int, count: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    if len_id == 0:
        total, end = _eval_3_0(bit_rep[22:], count)
        end += 22
    else:
        total, end = _eval_3_1(bit_rep[18:], count)
        end += 18
    return total, end


# Literal Value
def _eval_4(bit_rep: str) -> t.Tuple[int, int]:
    value = 0
    end = 0
    for index in range(6, len(bit_rep), 5):
        end = index + 5
        value += int(bit_rep[index+1:index+5], base=2)
        if bit_rep[index] == "0":
            break
    return value, end


def _eval_5_0(bit_rep: str, length: int) -> t.Tuple[int, int]:
    values = []
    end = 0
    while end < length:
        vsum, dend = _eval_packet(bit_rep[end:])
        values.append(vsum)
        end += dend
    if len(values) != 2:
        raise ValueError(f"Fuck {len(values)=}")
    return values[0] > values[1], length


def _eval_5_1(bit_rep: str, n_subpackets: int) -> t.Tuple[int, int]:
    values = []
    end = 0
    if n_subpackets != 2:
        raise ValueError(f"Fuck: {n_subpackets=}")
    for _ in range(n_subpackets):
        vsum, dend = _eval_packet(bit_rep[end:])
        values.append(vsum)
        end += dend
    return values[0] > values[1], end


# Greater Than
def _eval_5(bit_rep: str, len_id: int, count: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    if len_id == 0:
        total, end = _eval_5_0(bit_rep[22:], count)
        end += 22
    else:
        total, end = _eval_5_1(bit_rep[18:], count)
        end += 18
    return int(total), end


def _eval_6_0(bit_rep: str, length: int) -> t.Tuple[int, int]:
    values = []
    end = 0
    while end < length:
        vsum, dend = _eval_packet(bit_rep[end:])
        values.append(vsum)
        end += dend
    if len(values) != 2:
        raise ValueError(f"Fuck {len(values)=}")
    return values[0] < values[1], length


def _eval_6_1(bit_rep: str, n_subpackets: int) -> t.Tuple[int, int]:
    values = []
    end = 0
    if n_subpackets != 2:
        raise ValueError(f"Fuck: {n_subpackets=}")
    for _ in range(n_subpackets):
        vsum, dend = _eval_packet(bit_rep[end:])
        values.append(vsum)
        end += dend
    return values[0] < values[1], end


# Less Than
def _eval_6(bit_rep: str, len_id: int, count: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    if len_id == 0:
        total, end = _eval_6_0(bit_rep[22:], count)
        end += 22
    else:
        total, end = _eval_6_1(bit_rep[18:], count)
        end += 18
    return int(total), end


def _eval_7_0(bit_rep: str, length: int) -> t.Tuple[int, int]:
    values = []
    end = 0
    while end < length:
        vsum, dend = _eval_packet(bit_rep[end:])
        values.append(vsum)
        end += dend
    if len(values) != 2:
        raise ValueError(f"Fuck {len(values)=}")
    return values[0] == values[1], length


def _eval_7_1(bit_rep: str, n_subpackets: int) -> t.Tuple[int, int]:
    values = []
    end = 0
    if n_subpackets != 2:
        raise ValueError(f"Fuck: {n_subpackets=}")
    for _ in range(n_subpackets):
        vsum, dend = _eval_packet(bit_rep[end:])
        values.append(vsum)
        end += dend
    return values[0] == values[1], end


# Equal to
def _eval_7(bit_rep: str, len_id: int, count: int) -> t.Tuple[int, int]:
    total = 0
    end = 0
    if len_id == 0:
        total, end = _eval_7_0(bit_rep[22:], count)
        end += 22
    else:
        total, end = _eval_7_1(bit_rep[18:], count)
        end += 18
    return int(total), end


PACKETTYPE_OPERATIONS: t.Dict[int, t.Callable[[str, int, int], t.Tuple[int, int]]] = {
    0: _eval_0,
    1: _eval_1,
    2: _eval_2,
    3: _eval_3,
    5: _eval_5,
    6: _eval_6,
    7: _eval_7
}


def _eval_packet(bit_rep: str) -> t.Tuple[int, int]:
    global DEPTH
    DEPTH += 1
    type_id = int(bit_rep[3:6], base=2)
    if type_id == 4:
        result = _eval_4(bit_rep)
    else:
        len_id = int(bit_rep[6], base=2)
        count = 0
        if len_id == 0:
            count = int(bit_rep[7:22], base=2)
        else:
            count = int(bit_rep[7:18], base=2)
        result = PACKETTYPE_OPERATIONS[type_id](bit_rep, len_id, count)
    DEPTH -= 1
    return result


def evaluate_packet(packet: str) -> int:
    return _eval_packet(packet_hex_to_bin(packet))[0]


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
        print(f"{index}: {evaluate_packet(line.strip())}")
    return 0


main(sys.argv[1])
