from itertools import chain
from collections import defaultdict

type Stone = int

def read_stones() -> list[Stone]:
    with open('./inputs/day_11.txt') as f:
        return [int(stone_number) for stone_number in f.readline().rstrip().split()]

def blink(stones: list[Stone]) -> list[Stone]:
    return list(chain(*[transform_stone(stone) for stone in stones]))

def transform_stone(stone: Stone) -> list[Stone]:
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        middle = len(stone_str) // 2
        return [int(stone_str[0:middle]), int(stone_str[middle:])]
    else:
        return [stone * 2024]

def blink_times(stones: list[Stone], times: int):
    new_stones = [*stones]
    for _ in range(times):
        new_stones = blink(new_stones)
    return new_stones

def solve_part_1(stones: list[Stone]):
    return len(blink_times(stones, 25))

def solve_part_2_naive(stones: list[Stone]):
    return len(blink_times(stones, 75))

def solve_part_2(stones: list[Stone]):
    return blink_times_counter(stones, 75)

def blink_times_counter(stones: list[Stone], times: int):
    stone_count_map = defaultdict(int)
    for stone in stones:
        stone_count_map[stone] += 1

    for _ in range(times):
        for stone, count in {**stone_count_map}.items():
            stone_count_map[stone] -= count
            for new_stone in transform_stone(stone):
                stone_count_map[new_stone] += count

    return sum(c for c in stone_count_map.values())


if __name__ == '__main__':
    stones = read_stones()

    print(f"Answer for part 1: {solve_part_1(stones)}")
    print(f"Answer for part 2: {solve_part_2(stones)}")
