from typing import Callable

type Map = list[list[int]]
type Position = tuple[int, int]

def read_map() -> Map:
    with open('./inputs/day_10.txt') as f:
        return [
            [int(height) for height in line.rstrip()]
            for line in f
        ]

def follow_trail(map: Map, position: Position, previous_height: int, on_trail_end: Callable):
    x, y = position
    if x < 0 or x >= len(map) or y < 0 or y >= len(map[0]):
        return

    current_height = map[x][y]
    if current_height - previous_height != 1:
        return
    elif current_height == 9:
        on_trail_end(position)
        return

    follow_trail(map, (x, y+1), current_height, on_trail_end)
    follow_trail(map, (x, y-1), current_height, on_trail_end)
    follow_trail(map, (x-1, y), current_height, on_trail_end)
    follow_trail(map, (x+1, y), current_height, on_trail_end)
    return

def evaluate_trailhead_score(map: Map, trailhead_position: Position) -> int:
    found_trail_ends = dict()

    def on_trail_end(p):
        found_trail_ends[f"{p[0],p[1]}"] = True

    follow_trail(map, trailhead_position, -1, on_trail_end)
    return len(found_trail_ends)

def evaluate_trailhead_rating(map: Map, trailhead_position: Position) -> int:
    rating = 0

    def on_trail_end(p):
        nonlocal rating
        rating += 1

    follow_trail(map, trailhead_position, -1, on_trail_end)
    return rating

def get_total_trailhead_point(map: Map, evaluation_function: Callable) -> int:
    return sum(
        evaluation_function(map, (x, y))
        for x in range(len(map))
        for y in range(len(map[0]))
        if map[x][y] == 0
    )

def solve_part_1(map: Map):
    return get_total_trailhead_point(map, evaluate_trailhead_score)

def solve_part_2(map: Map):
    return get_total_trailhead_point(map, evaluate_trailhead_rating)

if __name__ == '__main__':
    map = read_map()

    print(f"Answer for part 1: {solve_part_1(map)}")
    print(f"Answer for part 1: {solve_part_2(map)}")
