type map = list[str]
type position = tuple[int, int]
type direction = str
type path = list[position]

UP = '^'
DOWN = 'v'
RIGHT = '>'
LEFT = '<'
OBSTACLE = '#'

def read_map() -> map:
    with open('./inputs/day_06.txt') as f:
        return [line.rstrip() for line in f]

# `p` is `position` and `t` is `times: int` below
go_up    = lambda p, t=1: (p[0]-t, p[1]  )
go_down  = lambda p, t=1: (p[0]+t, p[1]  )
go_right = lambda p, t=1: (  p[0], p[1]+t)
go_left  = lambda p, t=1: (  p[0], p[1]-t)
def go(start_position: position, direction: direction, times: int):
    handlers = { UP: go_up, DOWN: go_down, RIGHT: go_right, LEFT: go_left }
    return handlers[direction](start_position, times)

def turn_right(direction: direction) -> direction:
    return { UP: RIGHT, DOWN: LEFT, RIGHT: DOWN, LEFT: UP}[direction]

def find_position_and_direction(map: map) -> tuple[position, direction]:
    return [
        ((i, j), col)
        for i, row in enumerate(map)
        for j, col in enumerate(row)
        if col in [UP, RIGHT, LEFT, DOWN]
    ][0]

def get_path(start: position, end: position) -> path:
    i1, j1 = start
    i2, j2 = end
    def step(lower, upper):
        return 1 if lower < upper else -1
    step_i = step(i1, i2)
    step_j = step(j1, j2)
    return [
        (i, j)
        for i in range(i1, i2+step_i, step_i)
        for j in range(j1, j2+step_j, step_j)
    ]

def move_until_obstacle(map, start_position, direction) -> tuple[position, direction, path]:
    row_count = len(map)
    col_count = len(map[0])
    start_i, start_j = start_position

    def get_obstacle_or_exit_distance(ahead) -> tuple[int, bool]:
        "Return the distance to an obstacle or map exit, and whether it was an exit"
        try:
            return ahead.index(OBSTACLE)-1, False
        except:
            return len(ahead)-1, True

    ahead = []
    if direction == UP:
        ahead = [map[i][start_j] for i in range(start_i, -1, -1)]
    elif direction == DOWN:
        ahead = [map[i][start_j] for i in range(start_i, row_count)]
    elif direction == RIGHT:
        ahead = [map[start_i][j] for j in range(start_j, col_count)]
    elif direction == LEFT:
        ahead = [map[start_i][j] for j in range(start_j, -1, -1)]

    distance, is_exit = get_obstacle_or_exit_distance(ahead)

    end_position = go(start_position, direction, distance)
    path = get_path(start_position, end_position)

    if is_exit:
        return None, None, path
    return end_position, turn_right(direction), path

def solve_part_1(map: map):
    current_position, current_direction = find_position_and_direction(map)
    patrol_path = []
    visited_positions = {}
    while current_position:
        current_position, current_direction, path = move_until_obstacle(
            map, current_position, current_direction
        )
        path = path or []
        patrol_path += path
        for pos in path:
            visited_positions[f"{pos[0]},{pos[1]}"] = True
    return len(visited_positions), patrol_path

def find_loop_convenient_obstacle_trios(map: map) -> list[tuple[position, position, position]]:
    pass

def solve_part_2(map: map, patrol_path: list[position]):
    pass

if __name__ == '__main__':
    map = read_map()
    part_1_answer, patrol_path = solve_part_1(map)
    print(f"Answer for part 1: {part_1_answer}")
