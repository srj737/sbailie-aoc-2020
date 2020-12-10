import logging
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


def add_to_unique_list(target_list, entry):
    if entry not in target_list:
        target_list.append(entry)
        target_list = sorted(set(target_list))
    return target_list


def process_xmas_cipher(code, preamble_size):
    invalid_index = -1
    for index, number in enumerate(code):
        if index < preamble_size:
            continue
        else:
            possible_targets = []
            for i in range(index - preamble_size, index):
                for j in range(index - preamble_size, index):
                    possible_targets = add_to_unique_list(possible_targets, code[i] + code[j])
            if number in possible_targets:
                continue
            else:
                invalid_index = index
                break
    return invalid_index


def find_contiguous_range(code, target):
    contiguous, found_it = [], False
    for start_index, number in enumerate(code):
        contiguous = []
        for index in range(start_index, len(code)):
            contiguous.append(code[index])
            current_sum = sum(contiguous)
            if current_sum > target:
                # This contiguous range is over the target, hence break and check the next starting index.
                break
            elif current_sum == target:
                # This contiguous range is exactly target, hence break stop checking starting indexes.
                found_it = True
                break
        if found_it:
            break
    return contiguous


def day9_part1(code, preamble_size):
    first_invalid_index = process_xmas_cipher(code, preamble_size)
    first_invalid_value = code[first_invalid_index]
    logging.info('RESULT: The first invalid value is %d (with an index of: %d)', first_invalid_value,
                 first_invalid_index)
    return first_invalid_value, first_invalid_index


def day9_part2(code, preamble_size):
    target = code[process_xmas_cipher(code, preamble_size)]
    contiguous = find_contiguous_range(code, target)
    smallest, largest, result = min(contiguous), max(contiguous), min(contiguous) + max(contiguous)
    logging.info(
        'RESULT: The first invalid value, %d, can be reached by summing a contiguous range: %d -> %d. They add to get '
        'a result of: %d',
        target, smallest,
        largest, result)
    return result


test_array = ingest_file.int_on_lines('test-input/day9.txt')
array = ingest_file.int_on_lines('input/day9.txt')

# Test Input - Part 1
if day9_part1(test_array, 5) != (127, 14):
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day9_part1(array, 25) != (731031916, 617):
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day9_part2(test_array, 5) != 62:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day9_part2(array, 25) != 93396727:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
