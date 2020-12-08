import ingest_file
from datetime import datetime


def process_instruction(instructs, pointer, accumulator):
    current_instruct = instructs[pointer].strip()
    operation = current_instruct.split(' ')[0]
    argument = int(current_instruct.split(' ')[1])
    running = True
    termination_code = False
    old_pointer = pointer
    # Kill this last instruction so we don't repeat it ever again
    instructs[pointer] = 'stop 0'
    if operation == 'acc':
        # Increase accumulator value by argument, and move to next instruction
        accumulator += argument
        pointer += 1
    elif operation == 'nop':
        # Do nothing, move to next instruction
        pointer += 1
    elif operation == 'jmp':
        # Do nothing, move by the value of the argument
        pointer += argument
    elif operation == 'stop':
        # We've done this instruction before, terminate now, otherwise will run forever
        running = False
        termination_code = 'Infinite Loop'
    if old_pointer >= len(instructs) - 1:
        # This is the last instruction, only do it if it is 'acc'
        running = False
        termination_code = 'Success'
    return pointer, accumulator, running, termination_code


def day8_part1(array):
    pointer = 0
    accumulator = 0
    running = True
    while running:
        pointer, accumulator, running, termination_code = process_instruction(array, pointer, accumulator)
        a = 5
    #print("RESULT AT " + str(datetime.now()) + ": The accumulator value is: " + str(accumulator))
    return accumulator, termination_code


def day8_part2(array):
    termination_code = False
    while termination_code != 'Success':
        for i, instruct in enumerate(array):
            print("Testing " + str(i) + "/" + str(len(array)))
            new_array = array.copy()
            operation = instruct.split(' ')[0]
            argument = instruct.split(' ')[1]
            if operation == 'nop':
                new_array[i] = 'jmp ' + argument
                try:
                    accumulator, termination_code = day8_part1(new_array)
                except IndexError:
                    print("Index error occurred")
            elif operation == 'jmp':
                new_array[i] = 'nop ' + argument
                try:
                    accumulator, termination_code = day8_part1(new_array)
                except IndexError:
                    print("Index error occurred")
    print(
        "RESULT AT " + str(datetime.now()) + ": Successfully terminating code found. The accumulator value is: " + str(
            accumulator))
    return accumulator


test_array = ingest_file.strings_on_lines('test-input/day8.txt')
array = ingest_file.strings_on_lines('input/day8.txt')

# Test Input - Part 1
if day8_part1(test_array) != (5, 'Infinite Loop'):
    raise Exception("Part 1 Test FAILED!")
else:
    print("Part 1 Test PASSED")

# Real Input - Part 1
if day8_part1(array) != (1727, 'Infinite Loop'):
    raise Exception("Part 1 FAILED!")
else:
    print("Part 1 PASSED")

test_array = ingest_file.strings_on_lines('test-input/day8.txt')
array = ingest_file.strings_on_lines('input/day8.txt')

# Test Input - Part 2
if day8_part2(test_array) != 8:
   raise Exception("Part 2 Test FAILED!")
else:
   print("Part 2 Test PASSED")

# Real Input - Part 2
if day8_part2(array) != 176035:
  raise Exception("Part 2 FAILED!")
else:
  print("Part 2 PASSED")
