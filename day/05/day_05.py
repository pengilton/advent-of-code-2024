from collections import defaultdict
import re

def file_reading(file_name: str) -> list[str]:
    input = []

    with open(file_name, mode="r") as f:
        for line in f:
            input.append(line.strip())

    return input


# Creates the rule dictonary according the pattern xx|xx where x is a digit.
# X|Y means that X has to oocure before Y.
def create_rules(input: list[str]) -> defaultdict:
    rules = defaultdict(list)
    rule_pattern = re.compile(r"\d\d\|\d\d")

    for rule in input:
        if re.match(rule_pattern, rule):
            numbers = rule.split("|")
            key = int(numbers[0])
            value = int(numbers[1])
            rules[key].append(value)
    
    return rules


def create_updates(input: list[str]) -> list[list[int]]:
    updates = []
    rule_pattern = re.compile(r"\d\d\|\d\d")

    for update in input:
        if not (re.match(rule_pattern, update) or update == ""):
            numbers = list(map(int, update.split(",")))
            updates.append(numbers)
    
    return updates


def is_correct(update: list[int], rules: dict) -> bool:
    # We reserve the list because I don't want to bother with calculating indices.
    reversed_update = list(reversed(update))
    for i in range(len(reversed_update)):
        # Number which will be checked
        page = reversed_update[i]
        for j in range(i + 1, len(reversed_update)):
            # page has to be printed before this one
            previous_page = reversed_update[j]
            if previous_page in rules[page]:
                return False
    
    return True

def filter_ordered_updates(updates: list[list[int]], rules: dict) -> list[int]:
    ordered_updates = []

    for update in updates:
        if is_correct(update, rules):
            ordered_updates.append(update)

    return ordered_updates


def part_one():
    file_name = "input_05.txt"

    input_list = file_reading(file_name)
    rules_dict = create_rules(input_list)
    updates = create_updates(input_list)
    ordered_updates = filter_ordered_updates(updates, rules_dict)

    count = 0
    for update in ordered_updates:
        middle = len(update) // 2
        count += update[middle]

    print("Sum of all middle page numbers of the correctly-ordered updates: {}".format(count))


def part_two():
    file_name = "input_05.txt"

    count = 0
    
    print("X-MAS appears {} many times!".format(count))


if __name__ == "__main__":
    part_one()
    part_two()