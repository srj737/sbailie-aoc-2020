import logging
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

ACTIVE = '#'
INACTIVE = '.'


def calc_neighbour_indexes(dimensions, n, i, j, k, m):
    # 3D ==========
    if dimensions == 3:
        indexes = set([(x, y, z)
                       for x in range(i - 1, i + 2)
                       for y in range(j - 1, j + 2)
                       for z in range(k - 1, k + 2)
                       if (0 <= x < n and 0 <= y < n and 0 <= z < n)])
        indexes.remove((i, j, k))
    # 4D ==========
    elif dimensions == 4:
        indexes = set([(x, y, z, w)
                       for x in range(i - 1, i + 2)
                       for y in range(j - 1, j + 2)
                       for z in range(k - 1, k + 2)
                       for w in range(m - 1, m + 2)
                       if (0 <= x < n and 0 <= y < n and 0 <= z < n and 0 <= w < n)])
        indexes.remove((i, j, k, m))
    # Common =====
    return indexes


class ConwayCubes(object):

    def __init__(self, starting_2d_array, size, dimensions):
        self.size = size
        self.dimensions = dimensions
        offset = round(size / 2) - 1
        # 3D ==========
        if self.dimensions == 3:
            matrix = [[[INACTIVE for k in range(size)] for j in range(size)] for i in range(size)]
            for row_idx, row in enumerate(starting_2d_array):
                for col_idx, value in enumerate(row):
                    matrix[offset][row_idx + offset][col_idx + offset] = value
        # 4D ==========
        elif self.dimensions == 4:
            matrix = [[[[INACTIVE for m in range(size)] for k in range(size)] for j in range(size)] for i in
                      range(size)]
            for row_idx, row in enumerate(starting_2d_array):
                for col_idx, value in enumerate(row):
                    matrix[offset][offset][row_idx + offset][col_idx + offset] = value
        # Common =====
        self.matrix = matrix
        self.next_matrix = matrix
        self.energy_count = self.count_active_cubes()

    def cycle(self):
        # 3D ==========
        if self.dimensions == 3:
            next_matrix = [[[INACTIVE for k in range(self.size)] for j in range(self.size)] for i in range(self.size)]
            for i_idx, plane in enumerate(self.matrix):
                for j_idx, row in enumerate(plane):
                    for k_idx, value in enumerate(row):
                        next_matrix[i_idx][j_idx][k_idx] = self.calc_new_state(value, i_idx, j_idx, k_idx)
        # 4D ==========
        elif self.dimensions == 4:
            next_matrix = [[[[INACTIVE for m in range(self.size)] for k in range(self.size)] for j in range(self.size)]
                           for i in range(self.size)]
            for i_idx, space in enumerate(self.matrix):
                for j_idx, plane in enumerate(space):
                    for k_idx, row in enumerate(plane):
                        for m_idx, value in enumerate(row):
                            next_matrix[i_idx][j_idx][k_idx][m_idx] = self.calc_new_state(value, i_idx, j_idx, k_idx,
                                                                                          m_idx)
        # Common =====
        self.matrix = next_matrix
        self.energy_count = self.count_active_cubes()

    def calc_new_state(self, value, i, j, k, m=0):
        active_neighbour_count = 0
        neighbour_indexes = self.calc_neighbour_indexes(i, j, k, m)
        for index in neighbour_indexes:
            # 3D ==========
            if self.dimensions == 3:
                check = self.matrix[index[0]][index[1]][index[2]]
            # 4D ==========
            elif self.dimensions == 4:
                check = self.matrix[index[0]][index[1]][index[2]][index[3]]
            # Common =====
            if check == ACTIVE:
                active_neighbour_count += 1
            # As NOTHING will ever change if there are >3 active neighbours, we can break at 4 (Minor Performance)
            if active_neighbour_count > 3:
                break
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

    def calc_neighbour_indexes(self, i, j, k, m):
        n = self.size
        # 3D ==========
        if self.dimensions == 3:
            indexes = set([(x, y, z)
                           for x in range(i - 1, i + 2)
                           for y in range(j - 1, j + 2)
                           for z in range(k - 1, k + 2)
                           if (0 <= x < n and 0 <= y < n and 0 <= z < n)])
            indexes.remove((i, j, k))
        # 4D ==========
        elif self.dimensions == 4:
            indexes = set([(x, y, z, w)
                           for x in range(i - 1, i + 2)
                           for y in range(j - 1, j + 2)
                           for z in range(k - 1, k + 2)
                           for w in range(m - 1, m + 2)
                           if (0 <= x < n and 0 <= y < n and 0 <= z < n and 0 <= w < n)])
            indexes.remove((i, j, k, m))
        # Common =====
        return indexes

    def count_active_cubes(self):
        active_cubes = 0
        # 3D ==========
        if self.dimensions == 3:
            for i_idx, plane in enumerate(self.matrix):
                for j_idx, row in enumerate(plane):
                    for k_idx, value in enumerate(row):
                        if self.matrix[i_idx][j_idx][k_idx] == ACTIVE:
                            active_cubes += 1
        # 4D ==========
        elif self.dimensions == 4:
            for i_idx, space in enumerate(self.matrix):
                for j_idx, plane in enumerate(space):
                    for k_idx, row in enumerate(plane):
                        for m_idx, value in enumerate(row):
                            if self.matrix[i_idx][j_idx][k_idx][m_idx] == ACTIVE:
                                active_cubes += 1
        # Common =====
        return active_cubes


def day17(tickets_input, size, dimensions):
    pocket_dimension = ConwayCubes(tickets_input, size, dimensions)
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
# answer to get the best performance.

# Test Input - Part 1
if day17(test_input, 16, 3) != 112:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day17(main_input, 21, 3) != 310:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day17(test_input, 16, 4) != 848:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day17(main_input, 24, 4) != 2056:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
