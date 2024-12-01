import pandas as pd

def sum_distances(first_list: list, second_list: list) -> int:
    length = len(first_list) if len(first_list) <= len(second_list) else len(second_list)
    
    total_distance = 0
    for i in range(len(first_list)):
        distance = abs(first_list[i] -second_list[i])
        total_distance += distance

    return total_distance


def calc_similarity_score(first_list: list, second_list: list) -> int:
    occurance_dict = number_of_occurances(first_list, second_list)

    score = 0
    for key in first_list:
        num_occurance = occurance_dict[key]
        score += key * num_occurance

    return score


# For each value in first_list, it saves the number of occurancs in second_list in a dictanory.
def number_of_occurances(first_list: list, second_list: list) -> dict:
    occurance_dict = {}

    for key in first_list:
        if key not in occurance_dict:
            occurance_dict[key] = second_list.count(key)

    return occurance_dict


def part_one():
    df = pd.read_csv("input.csv", sep="   ", header=None, engine="python")

    first_column = df[0].tolist()
    second_column = df[1].tolist()

    first_column.sort()
    second_column.sort()

    total_distance = sum_distances(first_column, second_column)

    print("The total distance between both list is: {}".format(total_distance))


def part_two():
    df = pd.read_csv("input.csv", sep="   ", header=None, engine="python")

    first_column = df[0].tolist()
    second_column = df[1].tolist()

    similarity_score = calc_similarity_score(first_column, second_column)

    print("The similarity score is: {}".format(similarity_score))


if __name__ == "__main__":
    part_one()
    part_two()