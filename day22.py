import logging
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


def calculate_score(deck):
    total = len(deck)
    score = 0
    for idx, card in enumerate(deck):
        score += card * (total - idx)
    return score


class Combat:

    def __init__(self, data_input):
        self.deck_1 = [int(x) for x in data_input[0].replace('Player 1: ', '').split(' ')]
        self.deck_2 = [int(x) for x in data_input[1].replace('Player 2: ', '').split(' ')]
        self.score_1, self.score_2 = 0, 0
        self.rounds = 0
        return

    def run_game(self):
        while len(self.deck_1) != 0 and len(self.deck_2) != 0:
            self.run_round()
        self.score_1, self.score_2 = calculate_score(self.deck_1), calculate_score(self.deck_2)
        return

    def run_round(self):
        self.rounds += 1
        draw_1, draw_2 = self.deck_1[0], self.deck_2[0]
        self.deck_1, self.deck_2 = self.deck_1[1:], self.deck_2[1:]
        if draw_1 > draw_2:
            self.deck_1.extend([draw_1, draw_2])
        elif draw_2 > draw_1:
            self.deck_2.extend([draw_2, draw_1])
        return


class RecursiveCombat:

    def __init__(self, data_input):
        if 'Player' in data_input[0]:
            self.deck_1 = [int(x) for x in data_input[0].replace('Player 1: ', '').split(' ')]
            self.deck_2 = [int(x) for x in data_input[1].replace('Player 2: ', '').split(' ')]
        else:
            self.deck_1, self.deck_2 = data_input[0], data_input[1]
        self.score_1, self.score_2 = 0, 0
        self.rounds = 0
        self.winner = 0
        self.history = []
        return

    def run_game(self):
        while len(self.deck_1) != 0 and len(self.deck_2) != 0 and self.winner == 0:
            self.run_round()
        if self.winner == 0:  # Didn't win game via history repeating itself, so we need to calculate scores now
            self.score_1, self.score_2 = calculate_score(self.deck_1), calculate_score(self.deck_2)
            if self.score_1 > self.score_2:
                self.winner = 1
            elif self.score_2 > self.score_1:
                self.winner = 2
        return

    def run_round(self):
        self.rounds += 1
        round_winner = 0

        # If this exact config has already occurred this game, then player 1 is immediate winner.
        if (self.deck_1, self.deck_2) in self.history:
            self.winner = 1
            return

        # Add cards to game history
        self.history.append((self.deck_1, self.deck_2))

        # Draw cards and remover from deck
        draw_1, draw_2 = self.deck_1[0], self.deck_2[0]
        self.deck_1, self.deck_2 = self.deck_1[1:], self.deck_2[1:]

        # Determine winner of round via a new Sub-Game
        if len(self.deck_1) >= draw_1 and len(self.deck_2) >= draw_2:
            sub_game = RecursiveCombat([self.deck_1.copy()[:draw_1], self.deck_2.copy()[:draw_2]])
            sub_game.run_game()
            round_winner = sub_game.winner

        # Otherwise, as normal, determine round winner of round via higher card
        else:
            if draw_1 > draw_2:
                round_winner = 1
            elif draw_2 > draw_1:
                round_winner = 2

        # Give cards to the round winner (always round winner's card first)
        if round_winner == 1:
            self.deck_1.extend([draw_1, draw_2])
        elif round_winner == 2:
            self.deck_2.extend([draw_2, draw_1])
        return


def day22_part1(data_input):
    game = Combat(data_input)
    game.run_game()
    winning_score = max([game.score_1, game.score_2])
    logging.info('RESULT: The winning score after %d rounds of Combat is: %d', game.rounds, winning_score)
    return winning_score


def day22_part2(data_input):
    game = RecursiveCombat(data_input)
    game.run_game()
    winning_score = max([game.score_1, game.score_2])
    logging.info('RESULT: The winning score after %d rounds of Combat is: %d', game.rounds, winning_score)
    return winning_score


# Input Files
test_input = ingest_file.strings_separated_by_new_lines('test-input/day22.txt')
main_input = ingest_file.strings_separated_by_new_lines('input/day22.txt')

# Test Input - Part 1
if day22_part1(test_input) != 306:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day22_part1(main_input) != 32162:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day22_part2(test_input) != 291:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day22_part2(main_input) != 32534:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
