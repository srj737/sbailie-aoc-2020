import logging
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


def process_instruction(instructions, pointer, accumulator):
    current_instruction = instructions[pointer].strip()
    operation = current_instruction.split(' ')[0]
    argument = int(current_instruction.split(' ')[1])
    # Presume currently running (0 = 'Still Running'; 1 = 'Successfully Ended'; -1 = 'Infinite Run Stop')
    return_code = 0
    # Start with the next_pointer at the current pointer
    next_pointer = pointer
    # Kill this last instruction so we don't repeat it ever again, as if we do, it will repeat indefinitely
    instructions[pointer] = 'stop 0'
    # Act on operation
    if operation == 'acc':
        # Increase accumulator value by argument, and move to next instruction
        accumulator += argument
        next_pointer += 1
    elif operation == 'nop':
        # Do nothing, move to next instruction
        next_pointer += 1
    elif operation == 'jmp':
        # Do nothing, move by the value of the argument
        next_pointer += argument
    elif operation == 'stop':
        # We've done this instruction before, terminate now, otherwise will run forever
        return_code = -1
    if pointer >= len(instructions) - 1:
        # The previous instruction was the last instruction, so the programme successfully terminates
        return_code = 1
    return next_pointer, accumulator, return_code


def run_programme(instructions):
    pointer, accumulator, return_code = 0, 0, 0
    while return_code == 0:
        pointer, accumulator, return_code = process_instruction(instructions, pointer, accumulator)
    return accumulator, return_code


def day8_part1(instructions):
    accumulator, return_code = run_programme(instructions.copy())
    logging.info('RESULT: The accumulator value is: %d', accumulator)
    return accumulator, return_code


def day8_part2(instructions):
    return_code = 0
    while return_code != 1:  # (0 = 'Still Running'; 1 = 'Successfully Ended'; -1 = 'Infinite Run Stop')
        for i, instruction in enumerate(instructions):  # Test changing each instruction in the instructions list
            logging.debug('Testing possibly changing instruction: %d/%d', i, len(instructions))
            operation, argument = instruction.split(' ')
            if (operation != 'nop') and (operation != 'jmp'):
                # Don't bother changing or testing
                continue
            else:
                new_instructions = instructions.copy()
                if operation == 'nop':
                    new_instructions[i] = instruction.replace('nop', 'jmp')
                elif operation == 'jmp':
                    new_instructions[i] = instruction.replace('jmp', 'nop')
                try:
                    accumulator, return_code = run_programme(new_instructions)
                    if return_code == 1:
                        # We found the answer
                        # Break out of the inner 'for' loop now, the outer 'while' loop will break based on return code.
                        break
                except IndexError:
                    logging.warning("Index error occurred")
    logging.info('RESULT: Successfully terminating code found. The accumulator value is: %d', accumulator)
    return accumulator


test_array = ingest_file.strings_on_lines('test-input/day8.txt')
array = ingest_file.strings_on_lines('input/day8.txt')

# Test Input - Part 1
if day8_part1(test_array) != (5, -1):
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day8_part1(array) != (1727, -1):
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day8_part2(test_array) != 8:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day8_part2(array) != 552:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
