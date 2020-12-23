import logging
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


class Cups:

    def __init__(self, data_input, total):
        self.cups = {}
        for idx, cup in enumerate(data_input):
            self.cups[cup] = data_input[(idx + 1) % len(data_input)]
        if len(self.cups) < total:
            next_key = data_input[-1]
            next_value = max(self.cups) + 1
            while next_value <= total:
                self.cups[next_key] = next_value
                next_key, next_value = next_value, next_value + 1
            self.cups[next_value - 1] = data_input[0]
        self.round = 0
        self.current = data_input[0]
        self.min = min(self.cups)
        self.max = max(self.cups)
        return

    def run_game(self, game_length):
        while self.round < game_length:
            self.run_round()
            if self.round % 1000000 == 0:
                logging.info('PENDING: Completed round %d/%d', self.round, game_length)
        return

    def run_round(self):
        self.round += 1
        # Picks up next three cups
        pick_up = [self.cups[self.current],
                   self.cups[self.cups[self.current]],
                   self.cups[self.cups[self.cups[self.current]]]]
        self.cups[self.current] = self.cups[self.cups[self.cups[self.cups[self.current]]]]
        # Selects destination cup
        destination = self.find_destination_index(self.current, pick_up)
        # Places the picked up cups after destination
        self.cups[pick_up[2]] = self.cups[destination]
        self.cups[pick_up[1]] = pick_up[2]
        self.cups[pick_up[0]] = pick_up[1]
        self.cups[destination] = pick_up[0]
        # Iterate current cup (directly clockwise of current cup)
        self.current = self.cups[self.current]
        return

    def find_destination_index(self, current, pick_up):
        check = current - 1
        while True:
            if check in self.cups and check not in pick_up:
                destination = check
                break
            if check < self.min:
                check = self.max + 1
            else:
                check -= 1
        return destination

    def get_order_string(self):
        result = ''
        key = 1
        for n in range(8):
            result += str(self.cups[key])
            key = self.cups[key]
        return result

    def get_two_labels_clockwise_of_one(self):
        return self.cups[1], self.cups[self.cups[1]]


def day23_part1(data_input, rounds):
    game = Cups(data_input, len(data_input))
    game.run_game(rounds)
    result = game.get_order_string()
    logging.info('RESULT: The final order of cups after %d rounds of Cup is: %s', game.round, result)
    return result


def day23_part2(data_input, rounds):
    game = Cups(data_input, 1000000)
    game.run_game(rounds)
    result_1, result_2 = game.get_two_labels_clockwise_of_one()
    logging.info('RESULT: After %d rounds of Cup, the two cups clockwise of \'1\' are: %d & %d (Product: %d)',
                 game.round, result_1, result_2, result_1 * result_2)
    return result_1 * result_2


# Input Files
test_input = ingest_file.ints_on_single_line('test-input/day23.txt')
main_input = ingest_file.ints_on_single_line('input/day23.txt')

# Test Input - Part 1 (10 Rounds)
if day23_part1(test_input, 10) != '92658374':
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Test Input - Part 1 (100 Rounds)
if day23_part1(test_input, 100) != '67384529':
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day23_part1(main_input, 100) != '38925764':
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day23_part2(test_input, 10000000) != 149245887792:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day23_part2(main_input, 10000000) != 131152940564:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
