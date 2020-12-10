import logging
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


def day10_part1(adapters):
    adapters.append(max(adapters) + 3)
    adapters = sorted(adapters)
    jump_count = {1: 0, 2: 0, 3: 0}
    last_adapter = 0
    for adapter in adapters:
        jump_count[adapter - last_adapter] += 1
        last_adapter = adapter
    logging.info(
        'RESULT: In the chain of using every adapter, the jumps of 1, 2 & 3 jolts respectively are: %d, %d & %d',
        jump_count[1], jump_count[2], jump_count[3])
    return jump_count


def day10_part2(adapters):
    adapters.append(0)
    adapters.append(max(adapters) + 3)
    adapters = sorted(adapters)
    cumulative_path_count = [0] * len(adapters)
    cumulative_path_count[0] = 1
    for index, adapter in enumerate(adapters):
        for prev_index in range(index-3, index):
            if abs(adapters[prev_index] - adapters[index]) <= 3:
                cumulative_path_count[index] += cumulative_path_count[prev_index]
    logging.info(
        'RESULT: The cumulative path count by the end is: %d', cumulative_path_count[-1])
    return cumulative_path_count[-1]


test_array_small = ingest_file.int_on_lines('test-input/day10-small.txt')
test_array_large = ingest_file.int_on_lines('test-input/day10-large.txt')
array = ingest_file.int_on_lines('input/day10.txt')

# Test Input - Part 1 (Small Example)
if day10_part1(test_array_small) != {1: 7, 2: 0, 3: 5}:
    raise Exception("FAIL: Part 1 Test (Small Example) FAILED!")
else:
    logging.info("PASS: Part 1 Test (Small Example) PASSED")

# Test Input - Part 1 (Large Example)
if day10_part1(test_array_large) != {1: 22, 2: 0, 3: 10}:
    raise Exception("FAIL: Part 1 Test (Large Example) FAILED!")
else:
    logging.info("PASS: Part 1 Test (Large Example) PASSED")

# Real Input - Part 1
if day10_part1(array) != {1: 67, 2: 0, 3: 28}:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2 (Small Example)
if day10_part2(test_array_small) != 8:
    raise Exception("FAIL: Part 2 Test (Small Example) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Small Example) PASSED")

# Test Input - Part 1 (Large Example)
if day10_part2(test_array_large) != 19208:
    raise Exception("FAIL: Part 2 Test (Large Example) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Large Example) PASSED")

# Real Input - Part 1
if day10_part2(array) != 14173478093824:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")