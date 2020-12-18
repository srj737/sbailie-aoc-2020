import logging
import sys
import re

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

MULTIPLICATIVE_IDENTITY = 1
ADDITIVE_IDENTITY = 0


def solve_without_parenthesis(sum_string):
    # Parenthesis wrapping start and end are allowed, but if so, remove them.
    if sum_string[0] == '(':
        sum_string = sum_string[1:]
    if sum_string[-1] == ')':
        sum_string = sum_string[:-1]
    # Work left to right through the string
    values = []
    next_operation = ''
    while len(sum_string) > 0:
        char = sum_string[0]
        if char == '+' or char == '*':
            next_operation = char
            len_to_chop = 1
        else:
            leading_number = re.search('^[0-9]*', sum_string)[0]
            len_to_chop = len(leading_number)
            values.append(int(leading_number))
        sum_string = sum_string[len_to_chop:]
        # If we have 2 values we can perform the operation
        if len(values) > 1 and next_operation == '+':
            values = [values[0] + values[1]]
        if len(values) > 1 and next_operation == '*':
            values = [values[0] * values[1]]
    return str(values[0])


def calculate_sum(sum_string):
    # Intro
    sum_string = sum_string.strip()
    sum_string = sum_string.replace(' ', '')
    # Iteratively loop until there's only numbers left
    while not re.match('^[0-9]*$', sum_string):
        length = len(sum_string)
        # =========================
        # Assigns a "parenthesis level" to each char in string
        tracking_parenthesis = [0] * length
        current_parenthesis = 0
        for idx, char in enumerate(sum_string):
            if char == '(':
                current_parenthesis += 1
            tracking_parenthesis[idx] = current_parenthesis
            if char == ')':
                current_parenthesis -= 1
        max_parenthesis = max(tracking_parenthesis)
        # =========================
        # Get the first parenthesis substring at the deepest level
        first_deepest_lvl_sub_string = ''
        reached = False  # This flag is needed as there can be two of the same deepest level at a time.
        for idx, char in enumerate(sum_string):
            if tracking_parenthesis[idx] == max_parenthesis:
                first_deepest_lvl_sub_string += char
                reached = True
            if tracking_parenthesis[idx] < max_parenthesis and reached:
                break  # We only care for the first at this level right now.
        sum_string = sum_string.replace(first_deepest_lvl_sub_string,
                                        str(solve_without_parenthesis(first_deepest_lvl_sub_string)))
        # If we've solved all the issues with parenthesis and be can finally return the value. Else loop further.
        if '(' not in sum_string and ')' not in sum_string:
            return solve_without_parenthesis(sum_string)
    return sum_string


def day18(sums_array):
    total_sum = 0
    results = []
    for line in sums_array:
        value = int(calculate_sum(line))
        total_sum += value
        results.append(value)
    logging.info('RESULT: The final sum of all %d calculations is: %d', len(sums_array), total_sum)
    return results, total_sum


# Input Files
test_input = ingest_file.strings_on_lines('test-input/day18.txt')
main_input = ingest_file.strings_on_lines('input/day18.txt')

# Test Input - Part 1
if day18(test_input) != ([71, 51, 26, 437, 12240, 13632], 26457):
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day18(main_input)[1] != 24650385570008:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
# if day18(test_input) != 00000:
#    raise Exception("FAIL: Part 2 Test FAILED!")
# else:
#    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
# if day18(main_input) != 0000:
#    raise Exception("FAIL: Part 2 FAILED!")
# else:
#    logging.info("PASS: Part 2 PASSED")
