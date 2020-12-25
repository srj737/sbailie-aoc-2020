import logging
import sys

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


class DoorLockCrypto:

    def __init__(self, start, subject):
        self.value = start
        self.subject = subject
        self.modulo = 20201227
        self.loop = 0
        return

    def iterate(self):
        self.loop += 1
        self.value = (self.value * self.subject) % self.modulo
        return

    def encrypt(self, loop_size):
        for n in range(loop_size):
            self.iterate()
        return self.value


def find_loop_size(start_value, subject_number, public_key):
    check = DoorLockCrypto(start_value, subject_number)
    while check.value != public_key:
        check.iterate()
    return check.loop


def day25_part1(data_input):
    public_key = {'door': data_input[0], 'card': data_input[1]}
    loop_size = {'door': find_loop_size(1, 7, public_key['door']), 'card': find_loop_size(1, 7, public_key['card'])}
    encryption_key = DoorLockCrypto(1, public_key['card']).encrypt(loop_size['door'])
    logging.info('RESULT: The encryption key found is: %d', encryption_key)
    return encryption_key


# Input Files
test_input = ingest_file.int_on_lines('test-input/day25.txt')
main_input = ingest_file.int_on_lines('input/day25.txt')

# Test Input - Part 1
if day25_part1(test_input) != 14897079:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day25_part1(main_input) != 3217885:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# No Part 2 (Woo!)
