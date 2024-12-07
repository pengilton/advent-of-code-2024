import numpy as np
import re

def preprocessing(file_name: str) -> np.ndarray:
    input_2d = []

    with open(file_name, mode="r") as f:
        for line in f:
            input_2d.append(list(line.strip()))

    return np.array(input_2d)


# We traverse the 2d input array horizontally and return how often we hit the pattern. 
# word_length of the pattern. E.g. XMAS -> word_length = 4.
def count_horizontally(input: np.ndarray, pattern: re.Pattern, word_length: int) -> int:
    num_rows = np.shape(input)[0]
    num_cols = np.shape(input)[1]
    
    count = 0
    for row in range(num_rows):
        for column in range(num_cols - word_length + 1):
            text = ""
            for i in range(word_length):
                # row is fixed because we traverse horizontally
                text += input[row][column + i]
            if re.match(pattern, text):
                count += 1
    
    return count


# We traverse the 2d input array vertically and return how often we hit the pattern. 
# word_length of the pattern. E.g. XMAS -> word_length = 4.
def count_vetically(input: np.ndarray, pattern: re.Pattern, word_length: int) -> int:
    num_rows = np.shape(input)[0]
    num_cols = np.shape(input)[1]
    
    count = 0
    for column in range(num_cols):
        for row in range(num_rows - word_length + 1):
            text = ""
            for i in range(word_length):
                # row is fixed because we traverse horizontally
                text += input[row + i][column]
            if re.match(pattern, text):
                count += 1
    
    return count


# We traverse the 2d input array diagonally to the right and return how often we hit the pattern. 
# word_length of the pattern. E.g. XMAS -> word_length = 4.
def count_diagonally_right(input: np.ndarray, pattern: re.Pattern, word_length: int) -> int:
    num_rows = np.shape(input)[0]
    num_cols = np.shape(input)[1]
    
    count = 0
    for row in range(num_rows - word_length + 1):
        for column in range(num_cols - word_length + 1):
            text = ""
            for i in range(word_length):
                # row is fixed because we traverse horizontally
                text += input[row + i][column + i]
            if re.match(pattern, text):
                count += 1
    
    return count


# We traverse the 2d input array diagonally to the left and return how often we hit the pattern. 
# word_length of the pattern. E.g. XMAS -> word_length = 4.
def count_diagonally_left(input: np.ndarray, pattern: re.Pattern, word_length: int) -> int:
    num_rows = np.shape(input)[0]
    num_cols = np.shape(input)[1]
    
    count = 0
    for row in range(num_rows - word_length + 1):
        for col in range(num_cols - word_length + 1):
            column = num_cols - 1 - col
            text = ""
            for i in range(word_length):
                # row is fixed because we traverse horizontally
                text += input[row + i][column - i]
            if re.match(pattern, text):
                count += 1
    
    return count


# We create the valid xmas pattern here.
def create_valid_xmas_pattern():
    # M.M
    # .A.
    # S.S
    pattern_1 = r"M.M.A.S.S"

    # M.S
    # .A.
    # M.S
    pattern_2 = r"M.S.A.M.S"

    # S.S
    # .A.
    # M.M
    pattern_3 = r"S.S.A.M.M"

    # S.M
    # .A.
    # S.M
    pattern_4 = r"S.M.A.S.M"

    pattern = re.compile("|".join([pattern_1, pattern_2, pattern_3, pattern_4]))
    return pattern


def count_pattern_block(input: np.ndarray, pattern: re.Pattern, shape: tuple) -> int:
    num_rows = np.shape(input)[0]
    num_cols = np.shape(input)[1]
    
    shape_row = shape[0]
    shape_col = shape[1]

    count = 0
    for row in range(num_rows - shape_row + 1):
        for col in range(num_cols - shape_col + 1):
            text = ""
            
            # picking block of text which will be checked
            for i in range(shape_row):
                for j in range(shape_col):
                    text += input[row + i][col + j]
            
            if re.match(pattern, text):
                count += 1
    
    return count


def part_one():
    file_name = "input_04.txt"

    input_2d: np.ndarray = preprocessing(file_name)
    pattern: re.Pattern = re.compile(r"XMAS|SAMX")
    word_length= 4

    hor_count = count_horizontally(input_2d, pattern, word_length)
    ver_count = count_vetically(input_2d, pattern, word_length)
    dia_right_count = count_diagonally_right(input_2d, pattern, word_length)
    dia_left_count = count_diagonally_left(input_2d, pattern, word_length)
    count = hor_count + ver_count + dia_right_count + dia_left_count

    print("XMAS appears {} many times!".format(count))


def part_two():
    file_name = "input_04.txt"
    input_2d: np.ndarray = preprocessing(file_name)
    pattern: re.Pattern = create_valid_xmas_pattern()
    # Even though our pattern only checks for a string of length 9, we will use this tuple as a way 
    # to store the dimension of the text block. We are checking 3x3-block of text.
    pattern_shape: tuple = (3, 3)

    count = count_pattern_block(input_2d, pattern, pattern_shape)
    
    print("X-MAS appears {} many times!".format(count))


if __name__ == "__main__":
    part_one()
    part_two()