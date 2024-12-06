from collections import defaultdict
from math import floor

type page_order_rules = dict[int, dict[int]]
type update_pages = list[int]

def read_raw_rules_and_updates() -> tuple[list[str], list[str]]:
    rules = []
    updates = []
    reading_rules = True
    with open('./inputs/day_5.txt') as f:
        for line in f:
            entry = line.rstrip()
            if entry == '':
                reading_rules = False
                continue
            (rules if reading_rules else updates).append(entry)
    return rules, updates

def format_rules(rules: list[str]) -> page_order_rules:
    formatted_rules = defaultdict(dict)
    for rule in rules:
        [page_before, page_after] = [int(page) for page in rule.split('|')]
        formatted_rules[page_before][page_after] = True
    return formatted_rules

def format_updates(updates: list[str]) -> list[update_pages]:
    return [
        [int(page_number) for page_number in update.split(',')]
        for update in updates
    ]

def check_update(update: update_pages, rules: page_order_rules) -> tuple[bool, int]:
    "Return check result (bool) and rule breaking page (int)"
    page_to_check = update[0]
    rest_of_update = update[1:]

    if len(rest_of_update) == 0:
        return True, None

    for page in rest_of_update:
        if rules[page].get(page_to_check, False):
            return False, page_to_check

    return check_update(rest_of_update, rules)

def get_middle_page(update: update_pages) -> int:
    return update[floor(len(update) / 2)]

def find_incorrect_updates(updates: update_pages, rules: page_order_rules) -> list[update_pages]:
    return [
        update
        for update in updates
        if not check_update(update, rules)[0]
    ]

def fix_update_order(update: update_pages, rules: page_order_rules):
    _, breaking_page = check_update(update, rules)
    new_update_order = [*update]
    new_update_order.remove(breaking_page)
    new_update_order.append(breaking_page)
    if (check_update(new_update_order, rules)[0]):
        return new_update_order
    return fix_update_order(new_update_order, rules)

def solve_part_1(updates: update_pages, rules: page_order_rules):
    return sum(
        get_middle_page(update)
        for update in updates
        if check_update(update, rules)[0]
    )

def solve_part_2(updates: update_pages, rules: page_order_rules):
    incorrect_updates = find_incorrect_updates(updates, rules)
    return sum(
        get_middle_page(fix_update_order(update, rules))
        for update in incorrect_updates
    )

if __name__ == '__main__':
    raw_rules, raw_updates = read_raw_rules_and_updates()
    rules = format_rules(raw_rules)
    updates = format_updates(raw_updates)

    print(f"Answer for part 1: {solve_part_1(updates, rules)}")
    print(f"Answer for part 2: {solve_part_2(updates, rules)}")
