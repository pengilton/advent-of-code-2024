import re

def preprocessing(file_name: str, pattern: re.Pattern) -> list:
    matched_strings = []

    with open(file_name, mode="r") as f:
        for lines in f:
            line = lines.rstrip()
            found_patterns = re.findall(pattern, line)
            matched_strings.extend(found_patterns)

    return matched_strings


# We expect a string like "mul(264,12)". Should contain exatcly 1-3 digits per number.
def multiply(instruction: str) -> int:
    pattern: re.Pattern = re.compile(r"\d{1,3}")
    factors = re.findall(pattern, instruction)

    factor_a = int(factors[0])
    factor_b = int(factors[1])

    return factor_a * factor_b


def part_one():
    file_name = "input.txt"

    pattern: re.Pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)")
    matched_instructions = preprocessing(file_name, pattern)
    
    sum = 0
    for instruction in matched_instructions:
        product = multiply(instruction)
        sum += product
    
    print("Result of our multiplication is: {}".format(sum))


def part_two():
    print()


if __name__ == "__main__":
    part_one()
    part_two()