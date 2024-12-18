from itertools import batched
from typing import NamedTuple
from math import inf

type Vector = tuple[int, int]
type Config = list[Vector]

A_PRICE = 3
B_PRICE = 1

def read_configs() -> list[Config]:
    def read_button_config(s: str):
        return tuple(int(c) for c in s.split('X')[1].split(', Y'))
    configs = []
    with open('./inputs/day_13.txt') as f:
        for a, b, prize, _ in batched(f, 4):
            configs.append([
                read_button_config(a),
                read_button_config(b),
                tuple(int(c) for c in prize.split('X=')[1].split(', Y=')),
            ])
    return configs

def get_cost(
        a_config: Config,
        a_times: int,
        b_config: Config,
        b_times: int,
        prize_config: Config,
) -> int:
    a_x, a_y = a_config
    b_x, b_y = b_config
    p_x, p_y = prize_config

    satisfies_prize = ((a_times * a_x + b_times * b_x) == p_x and
                       (a_times * a_y + b_times * b_y) == p_y)
    if not satisfies_prize:
        return inf
    return a_times * A_PRICE + b_times * B_PRICE

def get_min_cost(config: Config):
    a_config, b_config, prize_config = config
    return min(
        get_cost(a_config, i, b_config, j, prize_config)
        for i in range(1, 101)
        for j in range(1, 101)
    )

def get_cost_of_as_many_prize_as_possible(configs: list[Config]):
    total_cost = 0
    for config in configs:
        cost = get_min_cost(config)
        if cost != inf:
            total_cost += cost
    return total_cost

def solve_part_1(configs: list[Config]):
    return get_cost_of_as_many_prize_as_possible(configs)

if __name__ == '__main__':
    configs = read_configs()

    print(f"Answer for part 1: {solve_part_1(configs)}")
