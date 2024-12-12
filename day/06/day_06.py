import numpy as np
import re
import sys
import operator

def preprocessing(file_name: str) -> np.ndarray:
    input_2d = []

    with open(file_name, mode="r") as f:
        for line in f:
            input_2d.append(list(line.strip()))

    return np.array(input_2d)


def get_guard_pos(map_of_lab: np.ndarray, pattern: re.Pattern) -> tuple:
    num_rows = np.shape(map_of_lab)[0]
    num_cols = np.shape(map_of_lab)[1]

    for i in range(num_rows):
        for j in range(num_cols):
            field: str = map_of_lab[i][j]
            if re.match(pattern, field):
                return (i, j)
    
    return (sys.maxsize, sys.maxsize)


def get_next_pos(guard_pos: tuple, guard_direction: str) -> tuple:
    x = guard_pos[0]
    y = guard_pos[1]

    match guard_direction:
        case "^":
            return (x - 1, y)
        case ">":
            return (x, y + 1)
        case "v":
            return (x + 1, y)
        case "<":
            return (x, y - 1)
        case _:
            raise ValueError("Undefined direction!")


def is_inside_map(map_of_lab: np.ndarray, guard_pos: tuple) -> bool:
    num_rows = np.shape(map_of_lab)[0]
    num_cols = np.shape(map_of_lab)[1]

    x = guard_pos[0]
    y = guard_pos[1]

    return  (0 <= x) and (x < num_rows) and (0 <= y) and (y < num_cols)


def rotate_right(direction: str) -> str:
    match direction:
        case "^":
            return ">"
        case ">":
            return "v"
        case "v":
            return "<"
        case "<":
            return "^"
        case _:
            raise ValueError("Undefined direction!")


# We update map inplace
def track_guard(map_of_lab: np.ndarray, pattern: re.Pattern, obstacle, visited_by_guard):
    guard_pos = get_guard_pos(map_of_lab, pattern)

    while is_inside_map(map_of_lab, guard_pos):
        x = guard_pos[0]
        y = guard_pos[1]
        guard_direction = map_of_lab[x][y]

        next_pos = get_next_pos(guard_pos, guard_direction)
        next_x = next_pos[0]
        next_y = next_pos[1]
        
        if is_inside_map(map_of_lab, next_pos):
            if map_of_lab[next_x][next_y] == obstacle:
                # We rotate to the right
                new_direction = rotate_right(guard_direction)
                map_of_lab[x][y] = new_direction
            else:
                # We move the guard to the new position
                map_of_lab[next_x][next_y] = map_of_lab[x][y]
                # Set the old position to visited_by_guard
                map_of_lab[x][y] = visited_by_guard
                # We update guard's psoition
                guard_pos = next_pos
        else:
            # Guard would move out of map -> we set its location as visited and move them out
            map_of_lab[x][y] = visited_by_guard
            guard_pos = next_pos


def count_visited_places(map_of_lab: np.ndarray, visited_by_guard: str) -> int:
    count = 0
    for row in map_of_lab:
        for col in row:
            if col == visited_by_guard:
                count += 1
    
    return count


# Returns True if we can create a rectanle out of the four corners.
def check_for_loop(three_corners: list[tuple], fourth_corner: tuple) -> bool:
    corner_a = three_corners[0]
    corner_b = three_corners[1]
    corner_c = three_corners[2]

    vector_ba = tuple(map(operator.sub, corner_a, corner_b))
    
    corner_d = tuple(map(operator.add, corner_c, vector_ba))

    if fourth_corner == corner_d:
        return True
    else:
        return False


def find_all_possible_obstructions(map_of_lab: np.ndarray, pattern: re.Pattern, obstacle: str, visited_by_guard: str) -> list[tuple]:
    obstacle_locations: list[tuple] = []
    # We keep the last three corners
    last_three_corners: list[tuple] = []

    guard_pos = get_guard_pos(map_of_lab, pattern)

    while is_inside_map(map_of_lab, guard_pos):
        guard_pos_x = guard_pos[0]
        guard_pos_y = guard_pos[1]
        guard_direction = map_of_lab[guard_pos_x][guard_pos_y]

        next_pos = get_next_pos(guard_pos, guard_direction)
        next_x = next_pos[0]
        next_y = next_pos[1]

        if is_inside_map(map_of_lab, next_pos):
            if map_of_lab[next_x][next_y] == obstacle:
                # if we don't have three corners yet, we append until we get three
                # else we are removing the first entry and append a new one
                if len(last_three_corners) < 3:
                    # current postition is going to be a corner
                    last_three_corners.append(guard_pos)
                else:
                    last_three_corners.pop(0)
                    last_three_corners.append(guard_pos)

                new_direction = rotate_right(guard_direction)
                map_of_lab[guard_pos_x][guard_pos_y] = new_direction
            else:
                if len(last_three_corners) == 3:
                    # We check if we can block him to create a loop
                    if check_for_loop(last_three_corners, guard_pos):
                        obstacle_locations.append(next_pos)

                # We move the guard to the new position
                map_of_lab[next_x][next_y] = map_of_lab[guard_pos_x][guard_pos_y]
                # Set the old position to visited_by_guard
                map_of_lab[guard_pos_x][guard_pos_y] = visited_by_guard
                # We update guard's psoition
                guard_pos = next_pos
        else:
            # Guard would move out of map -> we set its location as visited and move them out
            map_of_lab[guard_pos_x][guard_pos_y] = visited_by_guard
            guard_pos = next_pos
        
        if guard_pos == (9, 6):
            print(guard_pos)

    return obstacle_locations


def part_one():
    file_name = "input_06.txt"

    map_of_lab = preprocessing(file_name)

    guard_pattern = re.compile(r"\^|>|v|<")
    obstacle = "#"
    visited_by_guard = "X"

    track_guard(map_of_lab, guard_pattern, obstacle, visited_by_guard)

    count = count_visited_places(map_of_lab, visited_by_guard)

    print("The guard will visit {} distinct positions.".format(count))


def part_two():
    file_name = "test.txt"

    map_of_lab = preprocessing(file_name)

    guard_pattern = re.compile(r"\^|>|v|<")
    fixed_obstacle = "#"
    visited_by_guard = "X"

    possible_obstructions = find_all_possible_obstructions(map_of_lab, guard_pattern, fixed_obstacle, visited_by_guard)

    count = len(possible_obstructions)

    print("There are {} many different positions for possible obstructions.".format(count))


if __name__ == "__main__":
    part_one()
    part_two()