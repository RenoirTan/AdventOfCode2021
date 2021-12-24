from collections import Counter
import operator
import sys
import typing as t
from tqdm import tqdm


AssemblyValue = t.Union[str, int]


INS_INP = 0
INS_ADD = 1
INS_MUL = 2
INS_DIV = 3
INS_MOD = 4
INS_EQL = 5


def instruction_atoi(instruction: str) -> int:
    CONVERSION = {
        "inp": INS_INP,
        "add": INS_ADD,
        "mul": INS_MUL,
        "div": INS_DIV,
        "mod": INS_MOD,
        "eql": INS_EQL
    }
    return CONVERSION[instruction]


def atoav(raw: str) -> AssemblyValue:
    try:
        return int(raw)
    except:
        return raw


def generate_nonnegative_integers(start: int = 0) -> t.Generator[int, None, None]:
    number = start
    while True:
        yield number
        number += 1


def generate_model_numbers(length: int) -> t.Generator[str, None, None]:
    for number in generate_nonnegative_integers(int("1" * length)):
        result = str(number).zfill(length)
        if len(result) > length:
            break
        valid: bool = True
        for digit in result:
            if digit == "0":
                valid = False
                break
        if valid:
            yield result
        else:
            continue


class Alu(object):
    def __init__(self, registers: t.Iterable[str]) -> None:
        self.registers: t.Dict[str, int] = {}
        for register in registers:
            self.registers[register] = 0
    
    def __str__(self) -> str:
        return str(self.registers)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def instruction(self, instruction: int, register: str, value: AssemblyValue) -> None:
        NON_INP_INS_TO_OP = {
            INS_ADD: operator.add,
            INS_MUL: operator.mul,
            INS_DIV: operator.floordiv,
            INS_MOD: operator.mod,
            INS_EQL: operator.eq
        }
        if instruction == INS_INP:
            if type(value) == int:
                self.registers[register] = value
            else:
                raise TypeError(f"value must be type int, got {type(value)} instead")
        else:
            if type(value) == int:
                self.registers[register] = int(
                    NON_INP_INS_TO_OP[instruction](self.registers[register], value)
                )
            else:
                self.registers[register] = int(
                    NON_INP_INS_TO_OP[instruction](
                        self.registers[register],
                        self.registers[value]
                    )
                )
    
    def value(self, register: str) -> int:
        return self.registers[register]


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    program: t.List[t.Tuple[int, str, t.Optional[AssemblyValue]]] = []
    for line in fobj:
        raw = tuple(line.strip().split(" "))
        instruction = instruction_atoi(raw[0])
        register = raw[1]
        if len(raw) == 3:
            value = atoav(raw[2])
        else:
            value = None
        program.append((instruction, register, value))
    n_valid = 0
    miter = iter(tqdm(generate_model_numbers(14), desc="Model Numbers Tested"))
    for model in miter:
        digits = iter(model)
        alu = Alu("wxyz")
        for line in program:
            if line[0] == INS_INP:
                value = int(next(digits))
            else:
                value = line[2]
            alu.instruction(line[0], line[1], value)
        n_valid += int(alu.value("z") == 0)
    print(n_valid)
    return 0


main(sys.argv[1])
