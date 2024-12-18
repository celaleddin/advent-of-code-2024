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

def get_cost_of_as_many_prizes_as_possible(cost_function, configs: list[Config]):
    total_cost = 0
    for config in configs:
        cost = cost_function(config)
        if cost != inf:
            total_cost += cost
    return total_cost

def get_min_cost_by_solving_equations(config: Config):
    # a_x*Times_a + b_x*Times_b = p_x
    # a_y*Times_a + b_y*Times_b = p_y
    a_config, b_config, prize_config = config
    a_x, a_y = a_config
    b_x, b_y = b_config
    p_x, p_y = prize_config
    # p_x*b_y - p_y*b_x = Times_a*(a_x*b_y - a_y*b_x)
    try:
        times_a = (p_x*b_y - p_y*b_x) / (a_x*b_y - a_y*b_x)
        times_b = (p_x - a_x*times_a) / b_x
        if times_a == int(times_a) and times_b == int(times_b):
            return int(times_a*A_PRICE + times_b*B_PRICE)
        return inf
    except:
        return inf

def solve_part_1(configs: list[Config]):
    return get_cost_of_as_many_prizes_as_possible(get_min_cost, configs)

def solve_part_2(configs: list[Config]):
    error = 10000000000000
    config_with_fixed_prize = [
        (config[0], config[1], (config[2][0]+error, config[2][1]+error))
        for config in configs
    ]
    return get_cost_of_as_many_prizes_as_possible(
        get_min_cost_by_solving_equations,
        config_with_fixed_prize,
    )

if __name__ == '__main__':
    configs = read_configs()

    print(f"Answer for part 1: {solve_part_1(configs)}")
    print(f"Answer for part 2: {solve_part_2(configs)}")
