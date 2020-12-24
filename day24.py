import logging
import re
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


class TiledFloor:

    def __init__(self, size):
        self.size = size
        self.floor = [[False for j in range(size)] for i in range(size)]
        self.ref_x, self.ref_y = round(size / 2), round(size / 2)
        return

    def run_flips(self, instructions):
        for instruct in instructions:
            self.parse_instruction(instruct)
        return

    def parse_instruction(self, instruct):
        instruct = instruct.strip()
        curr_x, curr_y = self.ref_x, self.ref_y
        while len(instruct) > 0:
            if re.match('^(?:s|n)(?:w|e).*$', instruct):
                direction, instruct = instruct[:2], instruct[2:]
            else:
                direction, instruct = instruct[:1], instruct[1:]
            movement = getattr(self, 'move_' + str(direction), lambda: "Invalid movement")
            curr_x, curr_y = movement(curr_x, curr_y)
        self.floor[curr_x][curr_y] = not self.floor[curr_x][curr_y]
        return

    @staticmethod
    def move_e(i, j):
        return i + 2, j

    @staticmethod
    def move_w(i, j):
        return i - 2, j

    @staticmethod
    def move_ne(i, j):
        return i + 1, j + 1

    @staticmethod
    def move_nw(i, j):
        return i - 1, j + 1

    @staticmethod
    def move_se(i, j):
        return i + 1, j - 1

    @staticmethod
    def move_sw(i, j):
        return i - 1, j - 1

    def count_tiles(self):
        count = 0
        for row in self.floor:
            for value in row:
                if value:
                    count += 1
        return count

    def run_days(self, days):
        for n in range(days):
            self.run_day()
            logging.debug('PENDING: After %d of %d days, there are %d black tiles', n + 1, days, self.count_tiles())
        return

    def run_day(self):
        # Calculate the checks as to whether or not needs to flip
        to_flip = [[False for j in range(self.size)] for i in range(self.size)]
        for i, row in enumerate(self.floor):
            for j, value in enumerate(row):
                neighbours = self.neighbour_count(i, j)
                # Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
                if value and (neighbours == 0 or neighbours > 2):
                    to_flip[i][j] = True
                # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
                if not value and neighbours == 2:
                    to_flip[i][j] = True
        # Do the flipping
        for i, row in enumerate(to_flip):
            for j, value in enumerate(row):
                if value:  # True = needs to flip
                    self.floor[i][j] = not self.floor[i][j]
        return

    def neighbour_count(self, i, j):
        index_buffer = 3
        # Could find a better way to handle the edges but will just ignore and make 2D array bigger for now
        if i < index_buffer or j < index_buffer or i > self.size - index_buffer or j > self.size - index_buffer:
            tiles = []
        else:
            tiles = [
                self.floor[i + 2][j],
                self.floor[i - 2][j],
                self.floor[i + 1][j + 1],
                self.floor[i - 1][j + 1],
                self.floor[i + 1][j - 1],
                self.floor[i - 1][j - 1]
            ]
        return sum(tiles)


def day24_part1(data_input):
    lobby = TiledFloor(200)
    lobby.run_flips(data_input)
    result = lobby.count_tiles()
    logging.info('RESULT: After processing the instructions, the final number of black flipped tiles is: %s', result)
    return result


def day24_part2(data_input, days):
    lobby = TiledFloor(239)  # Trial and error-ed to be as low as possible
    lobby.run_flips(data_input)
    lobby.run_days(days)
    result = lobby.count_tiles()
    logging.info('RESULT: After processing the instructions, the final number of black flipped tiles after %d days '
                 'is: %s', days, result)
    return result


# Input Files
test_input = ingest_file.strings_on_lines('test-input/day24.txt')
main_input = ingest_file.strings_on_lines('input/day24.txt')

# Test Input - Part 1
if day24_part1(test_input) != 10:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day24_part1(main_input) != 473:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day24_part2(test_input, 100) != 2208:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day24_part2(main_input, 100) != 4070:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
