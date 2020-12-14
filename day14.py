import logging
import sys
import re

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


def bitmask_v1(value, mask):
    value_string = '{0:036b}'.format(value)
    result = ''
    for index, char in enumerate(mask):
        if char == 'X':
            result += value_string[index]
        else:
            result += char
    return int(result, 2)


def bitmask_v2(value, mask):
    value_string = '{0:036b}'.format(value)
    result = ''
    for index, char in enumerate(mask):
        if char == '0':
            result += value_string[index]
        else:
            result += char
    return result


def parse_instruction(instruction, mask):
    index, value = False, False
    if re.match('^mask = .*', instruction):
        mask = instruction.strip().replace('mask = ', '')
    elif re.match('^mem.*', instruction):
        search = re.search('^mem\[([0-9]*)\] = ([0-9]*)', instruction.strip())
        index, value = int(search.group(1)), int(search.group(2))
    return mask, index, value


def day14_part1(initialization):
    memory = {}  # Blank memory
    mask = ''  # The first instruction is a mask, so can initialize nothing here
    for instruction in initialization:
        mask, index, value = parse_instruction(instruction, mask)
        if not not index:
            memory[index] = bitmask_v1(value, mask)
    result_sum = 0
    for value in memory.values():
        result_sum += value
    logging.info('RESULT: The sum of memory values is: %d', result_sum)
    return result_sum


def calc_floating_addresses(input_masked_index):
    # Initial check if mask has a floating 'X's
    more_floating = False  # Presume done
    if re.search('[X]', input_masked_index):
        more_floating = True
    # The below while loop actually works through all the addresses so far.
    result_array = [input_masked_index]
    while more_floating:
        for masked_index in result_array:
            replacement = []
            for index, char in enumerate(masked_index):
                if char == 'X':
                    swap_with_0, swap_with_1 = list(masked_index), list(masked_index)
                    swap_with_0[index], swap_with_1[index] = '0', '1'
                    replacement.append("".join(swap_with_0))
                    replacement.append("".join(swap_with_1))
            if len(replacement) != 0:
                try:
                    result_array.remove(masked_index)
                except ValueError:
                    logging.debug('Already removed. Likely by \'list(set())\' duplicate removal')
                result_array += replacement
            result_array = list(set(result_array))  # Remove duplicates
        # Another check to see is any address mask still has floating 'X's
        more_floating = False  # Presume done
        for masked_index in result_array:
            # Check if continue
            if re.search('[X]', masked_index):
                more_floating = True
    # Convert binary string to int index address
    for ind, val in enumerate(result_array):
        result_array[ind] = int(val, 2)
    return result_array


def day14_part2(initialization):
    memory = {}  # Blank memory
    mask = ''  # The first instruction is a mask, so can initialize nothing here
    for n, instruction in enumerate(initialization):
        logging.info('PROCESSING: Instruction %d/%d', n, len(initialization))
        mask, index, value = parse_instruction(instruction, mask)
        if not not index:
            masked_index = bitmask_v2(index, mask)
            indexes_array = calc_floating_addresses(masked_index)
            for single_index in indexes_array:
                memory[single_index] = value
    result_sum = 0
    for value in memory.values():
        result_sum += value
    logging.info('RESULT: The sum of memory values is: %d', result_sum)
    return result_sum


# Input Files
test_input_part1 = ingest_file.strings_on_lines('test-input/day14-part1.txt')
test_input_part2 = ingest_file.strings_on_lines('test-input/day14-part2.txt')
main_input = ingest_file.strings_on_lines('input/day14.txt')

# Test Input - Part 1
if day14_part1(test_input_part1) != 165:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day14_part1(main_input) != 5875750429995:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day14_part2(test_input_part2) != 208:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day14_part2(main_input) != 5272149590143:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
