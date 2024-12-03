# Reads a file line by line and returns a list of a list of numbers.
def preprocessing(file_name: str, sep: str) -> list:
    reports = []

    with open(file_name, mode="r") as f:
        for lines in f:
            line = lines.rstrip()
            # We cast each number to an int
            report = list(map(int, line.split(sep)))
            reports.append(report)

    return reports

# Checks for a given report if its levels are either increasing or decreasing. And if 
# difference between two adjacent leves is min_diff <= difference <= max_diff. 
def safe_check(report: list, min_diff: int, max_diff:int) -> bool:
    is_increaasing = True
    is_decreasing = True

    for i in range(len(report) - 1):
        num_a = report[i]
        num_b = report[i + 1]

        if (abs(num_a - num_b) < min_diff) or (max_diff < abs(num_a - num_b)):
            return False

        if (num_a == num_b):
            return False
        elif (num_a < num_b):
            is_decreasing = False
        else:
            is_increaasing = False

    return (is_increaasing or is_decreasing)


def part_one():
    file_name = "input.txt"
    seperator = " "
    MIN_DIFF = 1
    MAX_DIFF = 3
    
    reports = preprocessing(file_name, seperator)

    safe_count = 0
    for report in reports:
        if safe_check(report, MIN_DIFF, MAX_DIFF):
            safe_count += 1

    print("{} reports are safe!".format(safe_count))


def part_two():
    return


if __name__ == "__main__":
    part_one()
    part_two()