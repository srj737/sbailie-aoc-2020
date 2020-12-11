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


def calc_if_change(seat_matrix, i, j):
    value = seat_matrix[i][j]
    min_i, min_j, max_i, max_j = 0, 0, len(seat_matrix) - 1, len(seat_matrix[0]) - 1
    surrounding_indexes = [[i-1, j-1], [i-1, j], [i-1, j+1], [i+1, j-1], [i+1, j], [i+1, j+1], [i, j-1], [i, j+1]]
    surrounding_indexes_without_invalid = copy.deepcopy(surrounding_indexes)
    for indexes in surrounding_indexes:
        if indexes[0] < min_i or indexes[1] < min_j or indexes[0] > max_i or indexes[1] > max_j:
            surrounding_indexes_without_invalid.remove(indexes)  # Invalid index
    surrounding_occupied_count = 0
    for indexes in surrounding_indexes_without_invalid:
        if seat_matrix[indexes[0]][indexes[1]] == '#':
            surrounding_occupied_count += 1
    if value == 'L' and surrounding_occupied_count == 0:
        return '#'
    elif value == '#' and surrounding_occupied_count >= 4:
        return 'L'
    else:
        return value


def run_round_of_people_entering(seat_matrix):
    new_seat_matrix = copy.deepcopy(seat_matrix)
    for i, row in enumerate(seat_matrix):
        for j, col in enumerate(row):
            new_seat_matrix[i][j] = calc_if_change(seat_matrix, i, j)
    return new_seat_matrix


def day11_part1(seat_matrix):
    last_seat_count = False  # Initialise as something that's guaranteed to not match the first time
    seat_count = count_seats(seat_matrix)
    while last_seat_count != seat_count:
        seat_matrix = run_round_of_people_entering(seat_matrix)
        last_seat_count = seat_count
        seat_count = count_seats(seat_matrix)
        logging.info('Running: Occupied seat count at: %d', seat_count['#'])
    logging.info('RESULT: The final seat count once nothing changes is: %d', seat_count['#'])
    return seat_count


def day11_part2():
    return 0


test_array = ingest_file.char_matrix('test-input/day11.txt')
array = ingest_file.char_matrix('input/day11.txt')

# Test Input - Part 1
if day11_part1(test_array) != {'.': 29, 'L': 34, '#': 37}:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day11_part1(array) != {'.': 1490, 'L': 5001, '#': 2251}:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
# if day11_part2(test_array) != 8:
#    raise Exception("FAIL: Part 2 Test FAILED!")
# else:
#    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
# if day11_part2(array) != 14173478093824:
#    raise Exception("FAIL: Part 2 FAILED!")
# else:
#    logging.info("PASS: Part 2 PASSED")
