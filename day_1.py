def read_location_lists() -> tuple[list[int], list[int]]:
    with open('./inputs/day_1.txt') as f:
        lines = f.readlines()
    left = []
    right = []
    for line in lines:
        pair = [int(i) for i in line.split()]
        left.append(pair[0])
        right.append(pair[1])
    return sorted(left), sorted(right)

def solve_part_1(left: list[int], right: list[int]) -> int:
    return sum(
        abs(left_loc - right[i]) for i, left_loc in enumerate(left)
    )

def solve_part_2(left: list[int], right: list[int]) -> int:
    from collections import Counter

    right_counter = Counter(right)
    return sum(
        left_loc * right_counter.get(left_loc, 0)
        for left_loc in left
    )


if __name__ == '__main__':
    left, right = read_location_lists()
    print(f"Answer for part 1: {solve_part_1(left, right)}")
    print(f"Answer for part 2: {solve_part_2(left, right)}")
