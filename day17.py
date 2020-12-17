import logging
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

ACTIVE = '#'
INACTIVE = '.'


def get_3d_neighbour_indexes(i, j, k):
    return [
        (i - 1, j - 1, k - 1),
        (i - 1, j - 1, k + 0),
        (i - 1, j - 1, k + 1),
        (i - 1, j + 0, k - 1),
        (i - 1, j + 0, k + 0),
        (i - 1, j + 0, k + 1),
        (i - 1, j + 1, k - 1),
        (i - 1, j + 1, k + 0),
        (i - 1, j + 1, k + 1),
        (i + 0, j - 1, k - 1),
        (i + 0, j - 1, k + 0),
        (i + 0, j - 1, k + 1),
        (i + 0, j + 0, k - 1),
        # (i + 0, j + 0, k + 0),
        (i + 0, j + 0, k + 1),
        (i + 0, j + 1, k - 1),
        (i + 0, j + 1, k + 0),
        (i + 0, j + 1, k + 1),
        (i + 1, j - 1, k - 1),
        (i + 1, j - 1, k + 0),
        (i + 1, j - 1, k + 1),
        (i + 1, j + 0, k - 1),
        (i + 1, j + 0, k + 0),
        (i + 1, j + 0, k + 1),
        (i + 1, j + 1, k - 1),
        (i + 1, j + 1, k + 0),
        (i + 1, j + 1, k + 1)
    ]


class ConwayCubes(object):

    def __init__(self, starting_2d_array, size, dimensions):
        self.size = size
        matrix = [[[INACTIVE for k in range(size)] for j in range(size)] for i in range(size)]
        next_matrix = [[[INACTIVE for k in range(size)] for j in range(size)] for i in range(size)]
        offset = round(size / 2) - 1
        for row_idx, row in enumerate(starting_2d_array):
            for col_idx, value in enumerate(row):
                matrix[offset][row_idx + offset][col_idx + offset] = value
        self.matrix = matrix
        self.next_matrix = next_matrix

    def cycle(self):
        next_matrix = [[[INACTIVE for k in range(self.size)] for j in range(self.size)] for i in range(self.size)]
        for i_idx, plane in enumerate(self.matrix):
            for j_idx, row in enumerate(plane):
                for k_idx, value in enumerate(row):
                    next_matrix[i_idx][j_idx][k_idx] = self.calc_new_state(i_idx, j_idx, k_idx, value)
        self.matrix = next_matrix
        self.energy_count = self.count_active_cubes()

    def calc_new_state(self, i, j, k, value):
        neighbour_indexes = get_3d_neighbour_indexes(i, j, k)
        active_neighbour_count = 0
        for index in neighbour_indexes:
            if all(0 <= x < self.size for x in index):
                check = self.matrix[index[0]][index[1]][index[2]]
                if check == ACTIVE:
                    active_neighbour_count += 1
        # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
        # Otherwise, the cube becomes inactive.
        if value == ACTIVE:
            if active_neighbour_count == 2 or active_neighbour_count == 3:
                return ACTIVE
            else:
                return INACTIVE
        # Else if a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
        # Otherwise, the cube remains inactive.
        else:
            if active_neighbour_count == 3:
                return ACTIVE
            else:
                return INACTIVE

    def count_active_cubes(self):
        active_cubes = 0
        for i_idx, plane in enumerate(self.matrix):
            for j_idx, row in enumerate(plane):
                for k_idx, value in enumerate(row):
                    if self.matrix[i_idx][j_idx][k_idx] == ACTIVE:
                        active_cubes += 1
        return active_cubes


def day17_part1(tickets_input, size):
    pocket_dimension = ConwayCubes(tickets_input, size, 3)
    target = 6
    for n in range(target):
        pocket_dimension.cycle()
        logging.info('PENDING: After %d/%d cycles, the energy count is %d', n + 1, target,
                     pocket_dimension.energy_count)
    logging.info('RESULT: The final energy count after %d cycles is: %d', target, pocket_dimension.energy_count)
    return pocket_dimension.energy_count


# Input Files
test_input = ingest_file.char_matrix('test-input/day17.txt')
main_input = ingest_file.char_matrix('input/day17.txt')

# Note: Initially I just guessed the size the matrix had to be, and if the final output didn't change when increasing
# the size by +1 then I knew it was sufficient. I then attempted smaller and smaller sizes while getting the same
# answer to get the best perfromance.

# Test Input - Part 1
if day17_part1(test_input, 16) != 112:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day17_part1(main_input, 21) != 310:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
# if day17_part2(test_input):
#    raise Exception("FAIL: Part 2 Test FAILED!")
# else:
#    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
# if day17_part2(main_input) != 491924517533:
#    raise Exception("FAIL: Part 2 FAILED!")
# else:
#    logging.info("PASS: Part 2 PASSED")
