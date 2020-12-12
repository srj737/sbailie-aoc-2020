import logging
import sys
import re

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


def manhattan_dist(x, y):
    return abs(x) + abs(y)


def move(x, y, value, direction):
    if direction == 'N':
        y += value
    elif direction == 'S':
        y -= value
    elif direction == 'E':
        x += value
    elif direction == 'W':
        x -= value
    return x, y


def turn(facing, rotation, angle):
    rotation = {'L': -1, 'R': 1}[rotation]
    facing = {'N': 0, 'E': 90, 'S': 180, 'W': 270}[facing]
    new_facing = (facing + rotation * angle) % 360
    return {0: 'N', 90: 'E', 180: 'S', 270: 'W'}[new_facing]


def rotate_waypoint_90(w_x, w_y, char):
    if char == 'L':
        # Rotate waypoint relative to boat - LEFT
        w_x, w_y = -w_y, w_x
    elif char == 'R':
        # Rotate waypoint relative to boat - RIGHT
        w_x, w_y = w_y, -w_x
    return w_x, w_y


# WITHOUT WAYPOINT (i.e. Part 1)
def process_instruction(x, y, facing, instruction):
    regex = re.match('^([A-Z])([0-9]*).*$', instruction.strip())
    char, value = regex.group(1), int(regex.group(2))
    if char == 'F':
        # Forward (Move value by facing)
        x, y = move(x, y, value, facing)
    elif char in {'N', 'S', 'E', 'W'}:
        # Cardinal
        x, y = move(x, y, value, char)
    elif char in {'L', 'R'}:
        # Turn Left or Right
        facing = turn(facing, char, value)
    return x, y, facing


# WITH WAYPOINT (i.e. Part 2)
def process_instruction_waypoints(x, y, w_x, w_y, facing, instruction):
    regex = re.match('^([A-Z])([0-9]*).*$', instruction.strip())
    char, value = regex.group(1), int(regex.group(2))
    if char == 'F':
        # Forward (Move to waypoint * value, irregardless of facing)
        for i in range(value):
            x, y = x + w_x, y + w_y
    elif char in {'N', 'S', 'E', 'W'}:
        # Cardinal (But move waypoint)
        w_x, w_y = move(w_x, w_y, value, char)
    elif char in {'L', 'R'}:
        if value == 90:
            w_x, w_y = rotate_waypoint_90(w_x, w_y, char)
        elif value == 180:
            # Doesn't matter which way (Left or right)
            w_x, w_y = -w_x, -w_y
        elif value == 270:
            # Equivalent to 90 degree the other way
            char = {'L': 'R', 'R': 'L'}[char]
            w_x, w_y = rotate_waypoint_90(w_x, w_y, char)
    return x, y, w_x, w_y, facing


def day12_part1(instructions):
    x, y, facing = 0, 0, 'E'
    for instruction in instructions:
        x, y, facing = process_instruction(x, y, facing, instruction)
    logging.info(
        'RESULT: At the end of the instructions, the ship facing %s at: %d, %d (Thus a Manhattan distance of: %d)',
        facing, x, y, manhattan_dist(x, y))
    return manhattan_dist(x, y)


def day12_part2(instructions):
    # x and y represent the boat (starting at 0,0)
    # w_x and w_y represent the waypoint RELATIVE to the boat (starting at 10,1)
    x, y, w_x, w_y, facing = 0, 0, 10, 1, 'E'
    for instruction in instructions:
        x, y, w_x, w_y, facing = process_instruction_waypoints(x, y, w_x, w_y, facing, instruction)
    logging.info('RESULT: At the end of the instructions, the ship facing %s at: %d, %d (Thus a Manhattan distance '
                 'of: %d), with a relative waypoint of %d, %d',
                 facing, x, y, manhattan_dist(x, y), w_x, w_y)
    return manhattan_dist(x, y)


test_array = ingest_file.strings_on_lines('test-input/day12.txt')
array = ingest_file.strings_on_lines('input/day12.txt')

# Test Input - Part 1
if day12_part1(test_array) != 25:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day12_part1(array) != 820:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day12_part2(test_array) != 286:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day12_part2(array) != 66614:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
