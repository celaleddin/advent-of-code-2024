def read_reports() -> list[list[int]]:
    with open('./inputs/day_2.txt') as f:
        reports_data = [line.rstrip() for line in f]
    return [
        [int(level) for level in report_data.split()]
        for report_data in reports_data
    ]

def is_report_safe(report: list[int]) -> bool:
    ascending = True if report[0] < report[1] else False

    def is_safe_level_change(level, next_level):
        return ((level < next_level if ascending else level > next_level) and
                abs(level - next_level) <= 3)

    for level, next_level in zip(report, report[1:]):
        if not is_safe_level_change(level, next_level):
            return False
    return True

def is_report_safe_under_problem_dampener(report: list[int]) -> bool:
    if is_report_safe(report):
        return True

    def report_variations():
        for i in range(len(report)):
            yield report[0:i] + report[i+1:]

    return any(
        is_report_safe(report_variation)
        for report_variation in report_variations()
    )

def count_safe_reports(report_safety_fun):
    return sum(1 for report in reports if report_safety_fun(report))

def solve_part_1(reports: list[list[int]]) -> int:
    return count_safe_reports(is_report_safe)

def solve_part_2(reports: list[list[int]]) -> int:
    return count_safe_reports(is_report_safe_under_problem_dampener)

if __name__ == '__main__':
    reports = read_reports()
    print(f"Answer for part 1: {solve_part_1(reports)}")
    print(f"Answer for part 2: {solve_part_2(reports)}")
