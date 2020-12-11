import logging
import sys
import copy

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


def count_seats(seat_matrix):
    seat_count = {'.': 0, 'L': 0, '#': 0}
    for row in seat_matrix:
        for value in row:
            seat_count[value] += 1
    return seat_count


def check_slope(seat_matrix, slope_x, slope_y, i, j, min_i, min_j, max_i, max_j):
    curr_i, curr_j = i + slope_x, j + slope_y
    occupied_seat_flag = False

    while min_i <= curr_i <= max_i and min_j <= curr_j <= max_j:
        check = seat_matrix[curr_i][curr_j]
        if check == 'L':
            occupied_seat_flag = False
            break
        if check == '#':
            occupied_seat_flag = True
            break
        curr_i, curr_j = curr_i + slope_x, curr_j + slope_y
    return occupied_seat_flag


def calc_if_change(seat_matrix, i, j, part):
    value = seat_matrix[i][j]

    if value == '.':
        return '.'

    min_i, min_j, max_i, max_j = 0, 0, len(seat_matrix) - 1, len(seat_matrix[0]) - 1

    if part == 1:
        # Part 1: Indexes to check are the surrounding 8
        indexes_to_check = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1], [i + 1, j - 1], [i + 1, j], [i + 1, j + 1],
                            [i, j - 1], [i, j + 1]]
        occupied_seat_threshold = 4
        surrounding_indexes_without_invalid = copy.deepcopy(indexes_to_check)
        for indexes in indexes_to_check:
            if indexes[0] < min_i or indexes[1] < min_j or indexes[0] > max_i or indexes[1] > max_j:
                surrounding_indexes_without_invalid.remove(indexes)  # Invalid index
        surrounding_occupied_count = 0
        for indexes in surrounding_indexes_without_invalid:
            if seat_matrix[indexes[0]][indexes[1]] == '#':
                surrounding_occupied_count += 1

    else:
        # Part 2: Indexes to check are the first visible in each 8 directions
        slopes_to_check = [[1, 1], [1, 0], [1, -1], [-1, 1], [-1, 0], [-1, -1], [0, 1], [0, -1]]
        surrounding_occupied_count = 0
        for slopes in slopes_to_check:
            if check_slope(seat_matrix, slopes[0], slopes[1], i, j, min_i, min_j, max_i, max_j):
                surrounding_occupied_count += 1
        occupied_seat_threshold = 5

    if value == 'L' and surrounding_occupied_count == 0:
        return '#'
    elif value == '#' and surrounding_occupied_count >= occupied_seat_threshold:
        return 'L'
    else:
        return value


def run_round_of_people_entering(seat_matrix, part):
    new_seat_matrix = copy.deepcopy(seat_matrix)
    for i, row in enumerate(seat_matrix):
        for j, col in enumerate(row):
            new_seat_matrix[i][j] = calc_if_change(seat_matrix, i, j, part)
    return new_seat_matrix


def day11(seat_matrix, part=1):
    last_seat_count = False  # Initialise as something that's guaranteed to not match the first time
    seat_count = count_seats(seat_matrix)
    while last_seat_count != seat_count:
        seat_matrix = run_round_of_people_entering(seat_matrix, part)
        last_seat_count = seat_count
        seat_count = count_seats(seat_matrix)
        logging.info('Running: Occupied seat count at: %d', seat_count['#'])
    logging.info('RESULT: The final seat count once nothing changes is: %d', seat_count['#'])
    return seat_count


test_array = ingest_file.char_matrix('test-input/day11.txt')
test_array_mini1 = ingest_file.char_matrix('test-input/day11-mini1.txt')
test_array_mini2 = ingest_file.char_matrix('test-input/day11-mini2.txt')
test_array_mini3 = ingest_file.char_matrix('test-input/day11-mini3.txt')
array = ingest_file.char_matrix('input/day11.txt')

# Test Input - Part 1
if day11(test_array) != {'.': 29, 'L': 34, '#': 37}:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day11(array) != {'.': 1490, 'L': 5001, '#': 2251}:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2 (Mini Example 1)
if day11(test_array_mini1, 2) != {'.': 72, 'L': 1, '#': 8}:
    raise Exception("FAIL: Part 2 Test (Mini Example 1) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Mini Example 1) PASSED")

# Test Input - Part 2 (Mini Example 2)
if day11(test_array_mini2, 2) != {'.': 33, 'L': 1, '#': 5}:
    raise Exception("FAIL: Part 2 Test (Mini Example 2) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Mini Example 2) PASSED")

# Test Input - Part 2 (Mini Example 3)
if day11(test_array_mini3, 2) != {'.': 24, 'L': 16, '#': 9}:
    raise Exception("FAIL: Part 2 Test (Mini Example 3) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Mini Example 3) PASSED")

# Test Input - Part 2
if day11(test_array, 2) != {'.': 29, 'L': 45, '#': 26}:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day11(array, 2) != {'.': 1490, 'L': 5233, '#': 2019}:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
