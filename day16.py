import logging
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


def check_valid(value, rule):
    if value in range(rule[0], rule[1] + 1) or value in range(rule[2], rule[3] + 1):
        return True
    else:
        return False


def validate_tickets(tickets_input):
    invalid_tickets, valid_tickets, invalid_values_sum = [], [], 0
    for ticket in tickets_input['other_tickets']:
        valid = True  # Presume ticket valid
        for value in ticket:
            if all(not check_valid(value, rule) for rule in tickets_input['rules'].values()):
                valid = False
                invalid_values_sum += value
        if valid:
            valid_tickets.append(ticket)
        else:
            invalid_tickets.append(ticket)
    tickets_input['valid_tickets'] = valid_tickets
    tickets_input['invalid_values_sum'] = invalid_values_sum
    return


def day16_part1(tickets_input):
    validate_tickets(tickets_input)
    logging.info('RESULT: The sum of totally invalid values (i.e. don''t fit any field at all) is: %d',
                 tickets_input['invalid_values_sum'])
    return tickets_input['invalid_values_sum']


def day16_part2(tickets_input):
    # Work out the 'valid_tickets'
    validate_tickets(tickets_input)

    # Rules that still need to be assigned an index and their ranges. e.g. { 'row': [1,4,45,47] }
    outstanding_rules = tickets_input['rules']

    # Take all the values from each field from EVERY ticket and gather them together. e.g. [[1,2,2], [43,45,43]]
    valid_values_per_field = [[]] * len(tickets_input['valid_tickets'][0])
    for ticket in tickets_input['valid_tickets']:
        for index, value in enumerate(ticket):
            valid_values_per_field[index] = valid_values_per_field[index] + [value]

    # Initially check which indexes can be possible for every rule name.
    possibilities = {}  # e.g. { 'row': [0,2], 'seat': [1], 'date': [1,2] }
    for rule_name, rule_ranges in outstanding_rules.items():
        for index, field in enumerate(valid_values_per_field):
            if all(check_valid(value, rule_ranges) for value in field):
                # Then this index IS possible for this rule
                if rule_name in possibilities:
                    possibilities[rule_name] = possibilities[rule_name] + [index]
                else:
                    possibilities[rule_name] = [index]

    # Will store the VERIFIED rules mapping. Index -> Rule Name. e.g. { 0: 'row', 1: 'seat' }
    rules_mapping = {}

    # Loop until all rules are assigned an index from the tickets array.
    while len(outstanding_rules) > 0:

        # Any rule that only have one possible index in 'possibilities' can be accepted as 'just found'.
        just_found_indexes = []
        for rule_name, rule_possibilities in possibilities.items():
            if len(rule_possibilities) == 1:
                rules_mapping[rule_possibilities[0]] = rule_name
                just_found_indexes.append(rule_possibilities[0])

        # For every 'just found index':
        # 1) Remove the rule from the 'Outstanding Rules' that we are checking until empty.
        # 2) Remove the rule from the 'Possibilities'.
        # 3) Remove the assigned index from any OTHER rule's possibilities in 'Possibilities'.
        for found_index in just_found_indexes:
            outstanding_rules.pop(rules_mapping[found_index])  # (1)
            possibilities.pop(rules_mapping[found_index])  # (2)
        for rule_name, rule_possibilities in possibilities.items():
            for found_index in just_found_indexes:
                if found_index in rule_possibilities:
                    rule_possibilities.pop(rule_possibilities.index(found_index))  # (3)

    # By here ALL rules have been successfully mapped to an index. (Fields in the ticket array).

    # But the actual output is the product of all the values on our ticket, where the field name contains 'departure'.
    departure_field_values = []
    for index, value in enumerate(tickets_input['my_ticket']):
        if "departure" in rules_mapping[index]:
            departure_field_values.append(value)
    if len(departure_field_values) == 0:
        departure_field_product = False
    else:
        departure_field_product = 1
        for x in departure_field_values:
            departure_field_product *= x

    logging.info('RESULT: The product of all fields on my ticket that contain \'departure\' is: %d',
                 departure_field_product)
    return departure_field_product


# Input Files
test_input_a = ingest_file.process_train_tickets('test-input/day16-a.txt')
main_input = ingest_file.process_train_tickets('input/day16.txt')

# Test Input - Part 1 A
if day16_part1(test_input_a) != 71:
    raise Exception("FAIL: Part 1 A Test FAILED!")
else:
    logging.info("PASS: Part 1 A Test PASSED")

# Real Input - Part 1
if day16_part1(main_input) != 27850:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# RESET TEST INPUTS
# Input Files
test_input_a = ingest_file.process_train_tickets('test-input/day16-a.txt')
test_input_b = ingest_file.process_train_tickets('test-input/day16-b.txt')
test_input_c = ingest_file.process_train_tickets('test-input/day16-c.txt')
main_input = ingest_file.process_train_tickets('input/day16.txt')

# Test Input - Part 2 A
if day16_part2(test_input_a):
    raise Exception("FAIL: Part 2 Test A FAILED!")
else:
    logging.info("PASS: Part 2 Test A PASSED")

# Test Input - Part 2 B
if day16_part2(test_input_b):
    raise Exception("FAIL: Part 2 Test B FAILED!")
else:
    logging.info("PASS: Part 2 Test B PASSED")

# Test Input - Part 2 C
if day16_part2(test_input_c) != 156:
    raise Exception("FAIL: Part 2 Test C FAILED!")
else:
    logging.info("PASS: Part 2 Test C PASSED")

# Real Input - Part 2
if day16_part2(main_input) != 491924517533:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
