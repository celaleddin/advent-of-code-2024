import re

def read_program_lines() -> list[str]:
    with open('./inputs/day_3.txt') as f:
        return f.readlines()

def find_instructions(program: list[str]):
    pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)|don't|do")
    instructions = []
    for line in program:
        for result in re.findall(pattern, line):
            instructions.append(result)
    return instructions

def is_mul_instruction(instruction: str): return instruction.startswith('mul')
def is_do_instruction(instruction: str): return instruction == "do"
def is_dont_instruction(instruction: str): return instruction == "don't"

def execute_mul_instruction(instruction: str):
    numbers = instruction.split('(')[1].split(')')[0].split(',')
    return int(numbers[0]) * int(numbers[1])

def solve_part_1(instructions: list[str]) -> int:
    return sum(
        execute_mul_instruction(instruction)
        if is_mul_instruction(instruction)
        else 0
        for instruction in instructions
    )

def solve_part_2(instructions: list[str]) -> int:
    mul_enabled = True

    def handle_instruction(i):
        nonlocal mul_enabled
        if is_do_instruction(i):
            mul_enabled = True
        elif is_dont_instruction(i):
            mul_enabled = False
        elif is_mul_instruction(i) and mul_enabled:
            return execute_mul_instruction(i)
        return 0

    return sum(
        handle_instruction(instruction)
        for instruction in instructions
    )

if __name__ == '__main__':
    program = read_program_lines()
    instructions = find_instructions(program)
    print(f"Answer for part 1: {solve_part_1(instructions)}")
    print(f"Answer for part 2: {solve_part_2(instructions)}")
