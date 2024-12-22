import numpy as np

def read_file(file_name: str) -> np.ndarray:
    input_2d = []

    with open(file_name, mode="r") as f:
        for line in f:
            input_2d.append(list(line.strip()))

    return np.array(input_2d)


def get_antena_coordinates(antena_map: np.ndarray, empty_spots: str = ".") -> list[tuple]:
    coordinates = []

    rows = antena_map.shape[0]
    columns = antena_map.shape[1]

    for i in range(rows):
        for j in range(columns):
            if antena_map[i][j] != empty_spots:
                coordinates.append((i, j))
    
    return coordinates


def is_inside_map(antena_map: np.ndarray, coord: tuple) -> bool:
    num_rows = antena_map.shape[0]
    num_cols = antena_map.shape[1]

    x = coord[0]
    y = coord[1]

    return  (0 <= x) and (x < num_rows) and (0 <= y) and (y < num_cols)


def get_antinode_coords(antena_map: np.ndarray, firs_coord: tuple, second_cord: tuple) -> list[tuple]:
    valid_coords = []

    delta_coords = tuple(map(lambda x, y: x - y, second_cord, firs_coord))

    first_antinode = tuple(map(lambda x, y: x - y, firs_coord, delta_coords))
    if is_inside_map(antena_map, first_antinode):
        valid_coords.append(first_antinode)
    
    second_antinode = tuple(map(lambda x, y: x + y, second_cord, delta_coords))
    if is_inside_map(antena_map, second_antinode):
        valid_coords.append(second_antinode)

    return valid_coords


def get_all_antinode_coords(antena_map: np.ndarray, antena_coordinates: list[tuple]) -> set:
    valid_coords = set()

    # We compare each antena with each other
    for i in range(len(antena_coordinates) - 1):
        first_coord: tuple = antena_coordinates[i]
        for j in range(i + 1, len(antena_coordinates)):
            second_coord: tuple = antena_coordinates[j]

            first_antena = antena_map[first_coord[0]][first_coord[1]]
            second_antena = antena_map[second_coord[0]][second_coord[1]]

            # Only do stuff when both equel.
            if first_antena == second_antena:
                antinode_cords = get_antinode_coords(antena_map, first_coord, second_coord)

                # We check for each valid antinode coord if the spot is empty 
                for antinode_cord in antinode_cords:
                    valid_coords.add(antinode_cord)

    return valid_coords


# Variant for part 2
def get_antinode_coords_2(antena_map: np.ndarray, first_coord: tuple, second_cord: tuple, max_iter_count: int = 1) -> list[tuple]:
    valid_coords = []

    delta_coords = tuple(map(lambda x, y: x - y, second_cord, first_coord))

    for k in range(max_iter_count + 1):
        first_antinode = (first_coord[0] - k * delta_coords[0], first_coord[1] - k * delta_coords[1])
        if is_inside_map(antena_map, first_antinode):
            valid_coords.append(first_antinode)
    
    for k in range(max_iter_count + 1):
        second_antinode = (second_cord[0] + k * delta_coords[0], second_cord[1] + k * delta_coords[1])
        if is_inside_map(antena_map, second_antinode):
            valid_coords.append(second_antinode)

    return valid_coords

# Variant for part 2
def get_all_antinode_coords_2(antena_map: np.ndarray, antena_coordinates: list[tuple]) -> set:
    valid_coords = set()
    max_iter_count = max(antena_map.shape[0], antena_map.shape[1])

    # We compare each antena with each other
    for i in range(len(antena_coordinates) - 1):
        first_coord: tuple = antena_coordinates[i]
        for j in range(i + 1, len(antena_coordinates)):
            second_coord: tuple = antena_coordinates[j]

            first_antena = antena_map[first_coord[0]][first_coord[1]]
            second_antena = antena_map[second_coord[0]][second_coord[1]]

            # Only do stuff when both equel.
            if first_antena == second_antena:
                antinode_cords = get_antinode_coords_2(antena_map, first_coord, second_coord, max_iter_count)

                # We check for each valid antinode coord if the spot is empty 
                for antinode_cord in antinode_cords:
                    valid_coords.add(antinode_cord)

    return valid_coords


def place_antinodes(antena_map: np.ndarray, antena_coordinates: list[tuple], antinode: str = "#", empty_spot: str = "."):
    # We compare each antena with each other
    for i in range(len(antena_coordinates) - 1):
        first_coord: tuple = antena_coordinates[i]
        for j in range(i + 1, len(antena_coordinates)):
            second_coord: tuple = antena_coordinates[j]

            first_antena = antena_map[first_coord[0]][first_coord[1]]
            second_antena = antena_map[second_coord[0]][second_coord[1]]

            # Only do stuff when both equel.
            if first_antena == second_antena:
                antinode_cords = get_antinode_coords(antena_map, first_coord, second_coord)

                # We check for each valid antinode coord if the spot is empty 
                for antinode_cord in antinode_cords:
                    if antena_map[antinode_cord[0]][antinode_cord[1]] == empty_spot:
                        antena_map[antinode_cord[0]][antinode_cord[1]] = antinode


def count_antinodes(antena_map: np.ndarray, antinode: str = "#") -> int:
    counter = 0
    for row in antena_map:
        for possible_antena in row:
            if possible_antena == antinode:
                counter += 1
    return counter


def part_one():
    file_name = "input_08.txt"

    antena_map = read_file(file_name)
    antena_coordinates = get_antena_coordinates(antena_map)
    all_antinodes: set = get_all_antinode_coords(antena_map, antena_coordinates)

    number_of_antinodes = len(all_antinodes)

    print("There are {} many anitnodes.".format(number_of_antinodes))


def part_two():
    file_name = "input_08.txt"

    antena_map = read_file(file_name)
    antena_coordinates = get_antena_coordinates(antena_map)
    all_antinodes: set = get_all_antinode_coords_2(antena_map, antena_coordinates)

    number_of_antinodes = len(all_antinodes)

    print("There are {} many anitnodes.".format(number_of_antinodes))


if __name__ == "__main__":
    part_one()
    part_two()