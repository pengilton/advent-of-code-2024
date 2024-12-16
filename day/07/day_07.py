import numpy as np

def preprocessing(file_name: str) -> list[list[int]]:
    input = []

    with open(file_name, mode="r") as f:
        for line in f:
            stripped_line = line.strip()
            numbers_str_list = stripped_line.split(" ")
            solution = numbers_str_list[0]
            solution = solution.replace(":", "")
            numbers_str_list[0] = solution
            numbers_list = list(map(int, numbers_str_list))
            input.append(numbers_list)

    return input


def calc_equation(equation: list[int], operators: str, avail_opertors: list[str]) -> int:
    result = equation[0]
    for i in range(1, len(equation)):
        num = equation[i]
        operator_index = int(operators[i - 1])
        operator = avail_opertors[operator_index]

        match operator:
            case "+":
                result += num
            case "*":
                result *= num
            case "||":
                restult_str = str(result)
                restult_str += str(num)
                result = int(restult_str)
    
    return result


def check_equation(equation: list[int], avail_opeartors: list[str]) -> bool:
    solution: int = equation[0]
    numbers: list[int] = equation[1:]
    # An equation with k numbers needs k-1 operators i.e. a string of length k-1
    num_of_needed_operators: int = len(numbers) - 1
    # If it is two, a bianry string is enough. Else we need a tenerary string or another base.
    num_avail_operators = len(avail_opeartors)
    
    for option in range(num_avail_operators ** num_of_needed_operators):
        # We represent the number in base=num_avail_operators and fill zeros if not enough bits.
        coded_operators = np.base_repr(option, num_avail_operators).zfill(num_of_needed_operators)
        result = calc_equation(numbers, coded_operators, avail_opeartors)

        if result == solution:
            return True

    return False


def part_one():
    file_name = "input_07.txt"

    equations: list[list[int]] = preprocessing(file_name)
    avail_operators = ["+", "*"]

    total_calibtration_result = 0
    for equation in equations:
        solution = equation[0]
        if check_equation(equation, avail_operators):
            total_calibtration_result += solution

    print("Total calibration result is {}.".format(total_calibtration_result))


def part_two():
    file_name = "input_07.txt"

    equations: list[list[int]] = preprocessing(file_name)
    avail_operators = ["+", "*", "||"]

    total_calibtration_result = 0
    for equation in equations:
        solution = equation[0]
        if check_equation(equation, avail_operators):
            total_calibtration_result += solution

    print("Total calibration result is {}.".format(total_calibtration_result))


if __name__ == "__main__":
    part_one()
    part_two()