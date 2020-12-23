import logging
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


class Cups:

    def __init__(self, data_input):
        self.cups = data_input.copy()
        self.round = 0
        self.current_label = self.cups[0]
        return

    def run_game(self, game_length):
        while self.round < game_length:
            self.run_round()
        return

    def run_round(self):
        self.round += 1
        current_idx = self.cups.index(self.current_label)

        # Picks up next three cups
        pick_up = self.pick_up_cups(current_idx, 3)

        # Selects destination cup
        destination_idx = self.find_destination_index(self.current_label)

        # Places picked up cups after destination
        for cup in pick_up:
            destination_idx += 1
            self.cups.insert(destination_idx, cup)

        # Iterate current cup (directly clockwise of current cup)
        self.current_label = self.cups[(self.cups.index(self.current_label) + 1) % len(self.cups)]
        return

    def find_destination_index(self, label):
        destination_index = 'NotFound'
        while destination_index == 'NotFound':
            destination_label = label - 1
            if destination_label in self.cups:
                destination_index = self.cups.index(destination_label)
            label -= 1  # Keep searching down
            if label < min(self.cups):
                label = max(self.cups) + 1
        return destination_index

    def pick_up_cups(self, current_idx, number_to_pick):
        pu_start = current_idx + 1
        pu_end = current_idx + 1 + number_to_pick
        cup_length = len(self.cups)
        if pu_start < cup_length and pu_end < cup_length:
            pick_up = self.cups[pu_start: pu_end]
            del (self.cups[pu_start: pu_end])
        elif pu_start < cup_length and pu_end >= cup_length:
            pu_end = pu_end % cup_length
            pick_up = self.cups[pu_start:] + self.cups[:pu_end]
            del (self.cups[pu_start:])
            del (self.cups[:pu_end])
        elif pu_start >= len(self.cups) and pu_end >= cup_length:
            pu_start = pu_start % cup_length
            pu_end = pu_end % cup_length
            pick_up = self.cups[pu_start: pu_end]
            del (self.cups[pu_start: pu_end])
        return pick_up

    def get_order_string(self):
        result = ''.join([str(x) for x in self.cups])
        return result.split('1')[1] + result.split('1')[0]


def day23_part1(data_input, rounds):
    game = Cups(data_input)
    game.run_game(rounds)
    result = game.get_order_string()
    logging.info('RESULT: The final order of cups after %d rounds of Cup is: %s', game.round, result)
    return result


def day23_part2(data_input):
    game = Cups(data_input)
    game.run_game(100)
    # logging.info('RESULT: The winning score after %d rounds of Combat is: %d', game.rounds, winning_score)
    return game


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
if day23_part1(main_input, 100) != 32162:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
#if day23_part2(test_input) != 291:
#    raise Exception("FAIL: Part 2 Test FAILED!")
#else:
#    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
#if day23_part2(main_input) != 32534:
#    raise Exception("FAIL: Part 2 FAILED!")
#else:
#    logging.info("PASS: Part 2 PASSED")
