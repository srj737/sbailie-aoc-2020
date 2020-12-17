import logging
import sys
import re

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

TARGET_TURN_PART1 = 2020
TARGET_TURN_PART2 = 30000000


class GameRun(object):

    def __init__(self, starting_numbers):
        self.spoken_memory = {}
        self.spoken_list = []
        self.turn_count = 1
        for number in starting_numbers:
            self.spoken_list.append(number)
            self.spoken_memory[number] = [self.turn_count]
            self.turn_count += 1

    def speak(self, number):
        if number in self.spoken_memory:  # If it HAS been spoken before
            if len(self.spoken_memory[number]) == 1:  # But only ONCE before
                num_to_say = 0
            else:  # If it has been spoken before MULTIPLE times
                num_to_say = self.spoken_memory[number][-1] - self.spoken_memory[number][-2]
            self.spoken_list.append(num_to_say)
            if num_to_say in self.spoken_memory:
                self.spoken_memory[num_to_say] = [self.spoken_memory[num_to_say][-1], self.turn_count]
            else:
                self.spoken_memory[num_to_say] = [self.turn_count]
        else:  # If it HASN'T been spoken before
            print('OH SHIT - NOT POSSIBLE')

    def iteration(self):
        last_number = self.spoken_list[-1]
        self.speak(last_number)
        self.turn_count += 1


def day15(starting_numbers, target):
    game = GameRun(starting_numbers)
    while game.turn_count <= target:
        game.iteration()
        if game.turn_count % 1000000 == 0:
            logging.info('PROCESSING: %s', "{:.2%}".format(game.turn_count / target))
    logging.info('RESULT: The last spoken number was: %d', game.spoken_list[-1])
    return game.spoken_list[-1]


# Input Files
test_input = ingest_file.ints_separated_by_separator('test-input/day15.txt', ',')
test_input_extra1 = ingest_file.ints_separated_by_separator('test-input/day15-extra1.txt', ',')
test_input_extra2 = ingest_file.ints_separated_by_separator('test-input/day15-extra2.txt', ',')
test_input_extra3 = ingest_file.ints_separated_by_separator('test-input/day15-extra3.txt', ',')
test_input_extra4 = ingest_file.ints_separated_by_separator('test-input/day15-extra4.txt', ',')
test_input_extra5 = ingest_file.ints_separated_by_separator('test-input/day15-extra5.txt', ',')
test_input_extra6 = ingest_file.ints_separated_by_separator('test-input/day15-extra6.txt', ',')
main_input = ingest_file.ints_separated_by_separator('input/day15.txt', ',')

# Test Input - Part 1
if day15(test_input, TARGET_TURN_PART1) != 436:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Test Input - Part 1 (Extra 1)
if day15(test_input_extra1, TARGET_TURN_PART1) != 1:
    raise Exception("FAIL: Part 1 Test (Extra 1) FAILED!")
else:
    logging.info("PASS: Part 1 Test (Extra 1) PASSED")

# Test Input - Part 1 (Extra 2)
if day15(test_input_extra2, TARGET_TURN_PART1) != 10:
    raise Exception("FAIL: Part 1 Test (Extra 2) FAILED!")
else:
    logging.info("PASS: Part 1 Test (Extra 2) PASSED")

# Test Input - Part 1 (Extra 3)
if day15(test_input_extra3, TARGET_TURN_PART1) != 27:
    raise Exception("FAIL: Part 1 Test (Extra 3) FAILED!")
else:
    logging.info("PASS: Part 1 Test (Extra 3) PASSED")

# Test Input - Part 1 (Extra 4)
if day15(test_input_extra4, TARGET_TURN_PART1) != 78:
    raise Exception("FAIL: Part 1 Test (Extra 4) FAILED!")
else:
    logging.info("PASS: Part 1 Test (Extra 4) PASSED")

# Test Input - Part 1 (Extra 5)
if day15(test_input_extra5, TARGET_TURN_PART1) != 438:
    raise Exception("FAIL: Part 1 Test (Extra 5) FAILED!")
else:
    logging.info("PASS: Part 1 Test (Extra 5) PASSED")

# Test Input - Part 1 (Extra 6)
if day15(test_input_extra6, TARGET_TURN_PART1) != 1836:
    raise Exception("FAIL: Part 1 Test (Extra 6) FAILED!")
else:
    logging.info("PASS: Part 1 Test (Extra 6) PASSED")

# Real Input - Part 1
if day15(main_input, TARGET_TURN_PART1) != 253:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day15(test_input, TARGET_TURN_PART2) != 175594:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Test Input - Part 2 (Extra 1)
if day15(test_input_extra1, TARGET_TURN_PART2) != 2578:
    raise Exception("FAIL: Part 2 Test (Extra 1) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra 1) PASSED")

# Test Input - Part 2 (Extra 2)
if day15(test_input_extra2, TARGET_TURN_PART2) != 3544142:
    raise Exception("FAIL: Part 2 Test (Extra 2) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra 2) PASSED")

# Test Input - Part 2 (Extra 3)
if day15(test_input_extra3, TARGET_TURN_PART2) != 261214:
    raise Exception("FAIL: Part 2 Test (Extra 3) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra 3) PASSED")

# Test Input - Part 2 (Extra 4)
if day15(test_input_extra4, TARGET_TURN_PART2) != 6895259:
    raise Exception("FAIL: Part 2 Test (Extra 4) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra 4) PASSED")

# Test Input - Part 2 (Extra 5)
if day15(test_input_extra5, TARGET_TURN_PART2) != 18:
    raise Exception("FAIL: Part 2 Test (Extra 5) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra 5) PASSED")

# Test Input - Part 2 (Extra 6)
if day15(test_input_extra6, TARGET_TURN_PART2) != 362:
    raise Exception("FAIL: Part 2 Test (Extra 6) FAILED!")
else:
    logging.info("PASS: Part 2 Test (Extra 6) PASSED")

# Real Input - Part 2
if day15(main_input, TARGET_TURN_PART2) != 13710:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
