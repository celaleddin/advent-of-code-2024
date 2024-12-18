from typing import NamedTuple

Plot = NamedTuple('Plot', [('x', int), ('y', int), ('plant', str)])
Region = NamedTuple('Region', [
    ('plots', list[Plot]),
    ('plant', str),
])

def read_map() -> list[str]:
    with open('./inputs/day_12.txt') as f:
        return [line.rstrip() for line in f]

def read_regions() -> list[Region]:
    map = read_map()
    visited = {}

    def read_connected_plots(plant: str, position: tuple[int, int]) -> list[Plot]:
        x, y = position
        visit_key = f"{x},{y}"

        if x >= len(map) or x < 0 or y >= len(map[0]) or y < 0:
            return []

        if plant != map[x][y] or visited.get(visit_key):
            return []
        visited[visit_key] = True
        return [
            Plot(x, y, plant),
            *read_connected_plots(plant, (x-1, y  )),
            *read_connected_plots(plant, (x+1, y  )),
            *read_connected_plots(plant, (  x, y-1)),
            *read_connected_plots(plant, (  x, y+1)),
        ]

    regions = []
    for x, row in enumerate(map):
        for y, plant in enumerate(row):
            plots = read_connected_plots(plant, (x, y))
            if len(plots):
                regions.append(Region(plots, plant))

    return regions

def count_touching_sides(region: Region) -> int:
    count = 0
    for i, plot in enumerate(region.plots):
        for other_plot in region.plots[i:]:
            if ((abs(plot.x - other_plot.x) == 1 and plot.y == other_plot.y) or
                (abs(plot.y - other_plot.y) == 1 and plot.x == other_plot.x)):
                count += 1
    return count

def calculate_perimeter(region: Region) -> int:
    return 4 * len(region.plots) - 2 * count_touching_sides(region)

def calculate_area(region: Region) -> int:
    return len(region.plots)

def solve_part_1(regions: list[Region]):
    return sum(
        calculate_area(region) * calculate_perimeter(region)
        for region in regions
    )

if __name__ == '__main__':
    regions = read_regions()

    print(f"Answer for part 1: {solve_part_1(regions)}")
