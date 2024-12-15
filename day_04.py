import re

type matrix = list[str]

def read_matrix() -> matrix:
    "Each string in the list is a row, each character in the string is a column"
    with open('./inputs/day_04.txt') as f:
        return [line.rstrip() for line in f]

def get_horizontals(matrix: matrix) -> list[str]:
    return [row for row in matrix]

def get_verticals(matrix: matrix) -> list[str]:
    return [
        "".join([row[column_index] for row in matrix])
        for column_index in range(len(matrix[0]))
    ]

def get_diagonals(matrix: matrix) -> list[str]:
    row_count = len(matrix)
    column_count = len(matrix[0])
    diagonals = []

    def get_diagonal(start_row, start_col):
        i = start_row
        j = start_col
        diagonal = ""
        while i < row_count and j < column_count:
            diagonal += matrix[i][j]
            i += 1
            j += 1
        return diagonal

    for row in range(row_count-1, 0, -1):
        diagonals.append(get_diagonal(row, 0))
    for col in range(column_count):
        diagonals.append(get_diagonal(0, col))

    return diagonals

def get_diagonals_from_right(matrix: matrix) -> list[str]:
    return get_diagonals(mirror(matrix))

def mirror(matrix: matrix) -> matrix:
    return ["".join(reversed(row)) for row in matrix]

def solve_part_1(matrix: matrix) -> int:
    xmas_pattern = re.compile("XMAS")
    reverse_xmas_pattern = re.compile("SAMX")
    directional_strings = [
        *get_horizontals(matrix),
        *get_verticals(matrix),
        *get_diagonals(matrix),
        *get_diagonals_from_right(matrix),
    ]
    return sum(
        len(re.findall(xmas_pattern, s)) +
        len(re.findall(reverse_xmas_pattern, s))
        for s in directional_strings
    )

def count_x_mas_matches(matrix: matrix) -> int:
    number_of_matches = 0
    row_count = len(matrix)
    column_count = len(matrix[0])

    def check_x_mas_pattern(i, j) -> bool:
        top_right = matrix[i-1][j+1]
        top_left = matrix[i-1][j-1]
        bottom_right = matrix[i+1][j+1]
        bottom_left = matrix[i+1][j-1]
        return ((
            (top_right == 'M' and bottom_left == 'S') or
            (top_right == 'S' and bottom_left == 'M')
        ) and (
            (top_left == 'M' and bottom_right == 'S') or
            (top_left == 'S' and bottom_right == 'M')
        ))

    for i in range(1, row_count-1):
        for j in range(1, column_count-1):
            char = matrix[i][j]
            if char == 'A' and check_x_mas_pattern(i, j):
                number_of_matches += 1

    return number_of_matches


def solve_part_2(matrix: matrix) -> int:
    return count_x_mas_matches(matrix)

if __name__ == '__main__':
    matrix = read_matrix()
    print(f"Answer for part 1: {solve_part_1(matrix)}")
    print(f"Answer for part 2: {solve_part_2(matrix)}")
