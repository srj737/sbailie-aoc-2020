import logging
import sys
import math

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


def day13_part1(data_input):
    time = int(data_input[0])
    bus_ids = data_input[1].split(',')
    best_bus = {'time': time * 2}  # Initialise with a bus that is without a doubt too late
    for bus_id in bus_ids:
        if bus_id != 'x':
            bus_id = int(bus_id)
            first_avail = math.ceil(time / bus_id) * bus_id
            if first_avail < best_bus['time']:
                best_bus['time'], best_bus['id'] = first_avail, bus_id
    wait = abs(time - best_bus['time'])
    result = wait * best_bus['id']
    logging.info(
        'RESULT: When getting to the stop at %d mins, the next available bus is at: %d mins (Bus ID: %d). Wait time: '
        '%d (Result: %d)',
        time, best_bus['time'], best_bus['id'], wait, result)
    return result


def check_bus_id(bus_id, offset, target):
    if (target + offset) < bus_id:
        return False
    elif (target + offset) % bus_id == 0:
        return True
    else:
        return False


def day13_part2(data_input):
    bus_ids = data_input[1].split(',')
    break_flag = False
    loop = 1
    while not break_flag:
        target = int(bus_ids[0]) * loop
        for index, bus_id in enumerate(bus_ids):
            # Don't bother for first bus (it's captured in target) or if the bus id is 'x'
            if index != 0 and bus_id != 'x':
                if not check_bus_id(int(bus_id), index, target):
                    # This target doesn't work, break the for and loop to try a new target
                    break
            if index == len(bus_ids) - 1:
                # Got to the end, woo!
                break_flag = True
        #        print(target)
        loop += 1
        if loop % 10000 == 0:
            logging.info('RUNNING: Checking: %d', target)
    logging.info(
        'RESULT: The earliest timestamp at which all the weird offsets occur is: %d mins',
        target)
    return target


def productList(myList):
    result = 1
    for x in myList:
        result = result * x
    return result


def day13_part2_crt(data_input):
    bus_ids = data_input[1].split(',')
    ordered_remainders, ordered_modulo = [], []
    for index, bus_id in enumerate(bus_ids):
        if bus_id != 'x':
            ordered_remainders.append(-index)
            ordered_modulo.append(int(bus_id))
    big_m = productList(ordered_modulo)
    to_name = []

    for modulo in ordered_modulo:
        modulo_to_multiply = ordered_modulo.copy()
        modulo_to_multiply.remove(modulo)
        next_value_1 = productList(modulo_to_multiply)
        next_value_2 = next_value_1 % modulo
        next_value_3 = pow(next_value_2, -1, modulo)
        next_value_4 = (next_value_3 * next_value_1) % big_m
        to_name.append(next_value_4)

    target = 0
    for index, remainder in enumerate(ordered_remainders):
        target += ordered_remainders[index] * to_name[index]

    result = target % big_m
    return target % big_m


# Input Files
test_input = ingest_file.strings_on_lines('test-input/day13.txt')
test_input_extra1 = ingest_file.strings_on_lines('test-input/day13-extra1.txt')
test_input_extra2 = ingest_file.strings_on_lines('test-input/day13-extra2.txt')
test_input_extra3 = ingest_file.strings_on_lines('test-input/day13-extra3.txt')
test_input_extra4 = ingest_file.strings_on_lines('test-input/day13-extra4.txt')
test_input_extra5 = ingest_file.strings_on_lines('test-input/day13-extra5.txt')
main_input = ingest_file.strings_on_lines('input/day13.txt')

# Test Input - Part 1
if day13_part1(test_input) != 295:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day13_part1(main_input) != 205:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day13_part2_crt(test_input) != 1068781:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Test Input - Part 2 (Extra Example 1)
if day13_part2_crt(test_input_extra1) != 3417:
    raise Exception("FAIL: Part 2 Test (Extra Example 1) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra Example 1) PASSED")

# Test Input - Part 2 (Extra Example 2)
if day13_part2_crt(test_input_extra2) != 754018:
    raise Exception("FAIL: Part 2 Test (Extra Example 2) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra Example 2) PASSED")

# Test Input - Part 2 (Extra Example 3)
if day13_part2_crt(test_input_extra3) != 779210:
    raise Exception("FAIL: Part 2 Test (Extra Example 3) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra Example 3) PASSED")

# Test Input - Part 2 (Extra Example 4)
if day13_part2_crt(test_input_extra4) != 1261476:
    raise Exception("FAIL: Part 2 Test (Extra Example 4) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra Example 4) PASSED")

# Test Input - Part 2 (Extra Example 5)
if day13_part2_crt(test_input_extra5) != 1202161486:
    raise Exception("FAIL: Part 2 Test (Extra Example 5) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra Example 5) PASSED")

# Real Input - Part 2
if day13_part2_crt(main_input) != 803025030761664:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
