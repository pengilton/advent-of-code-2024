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


def get_all_visited_places(map_of_lab: np.ndarray, visited_by_guard: str) -> list[tuple]:
    visited_placces: list[tuple] = []

    num_rows = np.shape(map_of_lab)[0]
    num_cols = np.shape(map_of_lab)[1]

    for row in range(num_rows):
        for col in range(num_cols):
            if map_of_lab[row][col] == visited_by_guard:
                visited_placces.append((row, col))

    return visited_placces


def brute_force_all_obstruction_positions(map_of_lab: np.ndarray, visited_places: list[tuple], pattern: re.Pattern, fixed_obstacle: str, visited_by_guard: str, placed_obstacle: str):
    guard_pos = get_guard_pos(map_of_lab, pattern)
    # We remove the start position
    visited_places.remove(guard_pos)

    obstalce_pattern = re.compile("|".join([fixed_obstacle, placed_obstacle]))

    num_rows = np.shape(map_of_lab)[0]
    num_cols = np.shape(map_of_lab)[1]
    max_tries = 2 * num_rows * num_cols

    count = 0
    for visited_place in visited_places:
        tries = 0

        mab_of_lab_copy = map_of_lab.copy()
        mab_of_lab_copy[visited_place[0]][visited_place[1]] = placed_obstacle

        guard_pos = get_guard_pos(mab_of_lab_copy, pattern)

        while is_inside_map(mab_of_lab_copy, guard_pos) and (tries < max_tries):
            guard_x = guard_pos[0]
            guard_y = guard_pos[1]
            guard_direction = mab_of_lab_copy[guard_x][guard_y]

            next_pos = get_next_pos(guard_pos, guard_direction)
            next_x = next_pos[0]
            next_y = next_pos[1]
            
            if is_inside_map(mab_of_lab_copy, next_pos):
                if re.match(obstalce_pattern, mab_of_lab_copy[next_x][next_y]):
                    # We rotate to the right
                    new_direction = rotate_right(guard_direction)
                    mab_of_lab_copy[guard_x][guard_y] = new_direction
                else:
                    # We move the guard to the new position
                    mab_of_lab_copy[next_x][next_y] = mab_of_lab_copy[guard_x][guard_y]
                    # Set the old position to visited_by_guard
                    mab_of_lab_copy[guard_x][guard_y] = visited_by_guard
                    # We update guard's psoition
                    guard_pos = next_pos
            else:
                # Guard would move out of map -> we set its location as visited and move them out
                mab_of_lab_copy[guard_x][guard_y] = visited_by_guard
                guard_pos = next_pos
            
            tries += 1
        
        if tries >= max_tries:
            count += 1

    return count


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
    file_name = "input_06.txt"

    map_of_lab = preprocessing(file_name)
    map_of_lab_tracked = map_of_lab.copy()

    guard_pattern = re.compile(r"\^|>|v|<")
    fixed_obstacle = "#"
    visited_by_guard = "X"
    placed_obstacle = "O"

    track_guard(map_of_lab_tracked, guard_pattern, fixed_obstacle, visited_by_guard)
    visited_places = get_all_visited_places(map_of_lab_tracked, visited_by_guard)

    count = brute_force_all_obstruction_positions(map_of_lab, visited_places, guard_pattern, fixed_obstacle, visited_by_guard, placed_obstacle)

    print("There are {} many different positions for possible obstructions.".format(count))


if __name__ == "__main__":
    part_one()
    part_two()