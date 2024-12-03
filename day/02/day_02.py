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
        diff = abs(num_a - num_b)

        if ((diff < min_diff) or (max_diff < diff)):
            return False

        if (num_a == num_b):
            return False
        elif (num_a < num_b):
            is_decreasing = False
        else:
            is_increaasing = False

    return (is_increaasing or is_decreasing)


def recursive_safe_check(report: list, min_diff: int, max_diff:int, tolerance: int) -> bool:
    is_increaasing = True
    is_decreasing = True
    is_in_interval = True
    safe = True

    for i in range(len(report) - 1):
        num_a = report[i]
        num_b = report[i + 1]
        diff = abs(num_a - num_b)
        
        if ((diff < min_diff) or (max_diff < diff)):
            is_in_interval = False

        if (num_a == num_b):
            is_decreasing = False
            is_increaasing = False
        elif (num_a < num_b):
            is_decreasing = False
        else:
            is_increaasing = False
        
        safe = (is_increaasing or is_decreasing) and is_in_interval

        if (safe == False):
            if tolerance > 0:
                filtered_report = report.copy()
                del filtered_report[i]
                safe = recursive_safe_check(filtered_report, min_diff, max_diff, tolerance - 1)
    
    return safe


def increasing_safe_check(report: list, min_diff: int, max_diff: int, tolerance: int) -> bool:
    if len(report) < 2:
        return True
    
    safe: bool = False
    index: int = 1
    while (index < len(report)):
        # difference >= 0 because we assume that the list has increasing values
        difference = report[index] - report[index - 1]

        if (min_diff <= difference) and (difference <= max_diff):
            index += 1
        else:
            if tolerance > 0:
                filtered_report = report.copy()
                del filtered_report[index - 1]

                if increasing_safe_check(filtered_report, min_diff, max_diff, tolerance - 1):
                    return True


def decreaasing_safe_check(report: list, min_diff: int, max_diff: int, tolerance: int) -> bool:
    return False


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