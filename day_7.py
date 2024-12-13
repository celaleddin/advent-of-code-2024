from typing import NamedTuple
from operator import add, mul
from itertools import product
from collections.abc import Callable

Equation = NamedTuple('Equation', [
    ('value', int),
    ('numbers', list[int])
])
type Operator = Callable[[int, int], int]

def read_equations() -> list[Equation]:
    equations = []
    with open('./inputs/day_7.txt') as f:
        for line in f:
            value_str, numbers_str = line.split(':')
            numbers = [int(n) for n in numbers_str.strip().split(' ')]
            equations.append(Equation(int(value_str), numbers))
    return equations

def can_satisfy_equation(equation: Equation, operators: list[Operator]) -> bool:
    numbers = equation.numbers
    number_of_operators_required = len(numbers) - 1

    possible_operators_combinations = product(operators, repeat=number_of_operators_required)

    for operators in possible_operators_combinations:
        result = numbers[0]
        for i, operator in enumerate(operators):
            result = operator(result, numbers[i+1])
        if result == equation.value:
            return True
    return False

def solve_part_1(equations: list[Equation]) -> int:
    return sum(
        equation.value
        for equation in equations
        if can_satisfy_equation(equation, [add, mul])
    )

def solve_part_2(equations: list[Equation]) -> int:
    def concatenate(num1: int, num2: int) -> int:
        return int(str(num1) + str(num2))

    return sum(
        equation.value
        for equation in equations
        if can_satisfy_equation(equation, [add, mul, concatenate])
    )

if __name__ == '__main__':
    equations = read_equations()

    print(f"Answer for part 1: {solve_part_1(equations)}")
    print(f"Answer for part 2: {solve_part_2(equations)}")
