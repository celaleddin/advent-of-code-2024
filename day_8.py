from typing import NamedTuple, Callable
from collections import defaultdict, Counter
from itertools import product

EMPTY_NODE = '.'

type MapSize = tuple[int, int]
type Position = tuple[int, int]

Antenna = NamedTuple('Antenna', [
    ('position', Position),
    ('frequency', str),
])

def read_antennas_and_map_size() -> tuple[list[Antenna], MapSize]:
    antennas = defaultdict(list)
    with open('./inputs/day_8.txt') as f:
        lines = f.readlines()
        row_count = len(lines)
        col_count = len(lines[0].rstrip())
        for i, line in enumerate(lines):
            for j, node in enumerate(line.rstrip()):
                if node != EMPTY_NODE:
                    antennas[node].append(
                        Antenna((i, j), frequency=node)
                    )
    return antennas, (row_count, col_count)

def find_antinode_positions(
        antennas: list[Antenna],
        frequency: str,
        check_limits: Callable,
        until_limits,
        include_antenna_positions,
) -> list[Position]:
    antinode_positions = []

    def get_antinodes_in_direction(initial, vector):
        candidate = initial[0] + vector[0], initial[1] + vector[1]
        if check_limits(candidate) and not until_limits:
            return [candidate]
        elif check_limits(candidate):
            return [candidate, *get_antinodes_in_direction(candidate, vector)]
        return []

    for antenna1, antenna2 in product(antennas[frequency], repeat=2):
        a, b = antenna1.position, antenna2.position
        if a == b:
            if include_antenna_positions:
                antinode_positions.append(a)
            continue

        v = b[0]-a[0], b[1]-a[1]

        antinode_positions += get_antinodes_in_direction(b, v)
        antinode_positions += get_antinodes_in_direction(a, (-v[0], -v[1]))

    return antinode_positions

def count_unique_antinodes(antennas: list[Antenna], map_size: MapSize, include_harmonics = False):
    def check_limits(position: Position):
        if (0 <= position[0] and position[0] < map_size[0] and
            0 <= position[1] and position[1] < map_size[1]):
            return True
        return False

    antinode_positions_in_map = [
        position
        for frequency in antennas.keys()
        for position in find_antinode_positions(
                antennas, frequency, check_limits,
                until_limits=include_harmonics,
                include_antenna_positions=include_harmonics,
        )
    ]
    return len(Counter(antinode_positions_in_map))

def solve_part_1(antennas: list[Antenna], map_size: MapSize) -> int:
    return count_unique_antinodes(antennas, map_size)

def solve_part_2(antennas: list[Antenna], map_size: MapSize) -> int:
    return count_unique_antinodes(antennas, map_size, include_harmonics=True)

if __name__ == '__main__':
    antennas, map_size = read_antennas_and_map_size()

    print(f"Answer for part 1: {solve_part_1(antennas, map_size)}")
    print(f"Answer for part 2: {solve_part_2(antennas, map_size)}")
