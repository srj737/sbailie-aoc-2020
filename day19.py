import logging
import sys
import re

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

OR_SEPARATOR = '|'
SPACE_SEPARATOR = ' '


class MonsterMessages:

    def __init__(self, data_input):
        self.images = data_input['images'].copy()
        self.rules = data_input['rules'].copy()
        self.patterns_unresolved = set([x for x in self.rules])
        self.patterns_resolved = {}
        return

    def resolve_all_pattern(self, target=0):
        # Iterate until all rules get resolve into patterns
        while len(self.patterns_unresolved) != target:
            to_resolve = []  # Stores all the ones ready to resolve after this iteration
            for rule_number in self.patterns_unresolved:
                # Already just letters
                if re.match('^[A-Za-z]*$', self.rules[rule_number]):
                    to_resolve.append(rule_number)
                    continue
                # Otherwise check if every component has been resolved
                components = self.rules[rule_number].split(' ')
                all_components_resolve = True
                for component in components:
                    if re.match('^[0-9]*$', component) and component not in self.patterns_resolved:
                        all_components_resolve = False
                if all_components_resolve:
                    to_resolve.append(rule_number)
                    continue
            # Resolve the pattern
            for rule_number in to_resolve:
                self.resolve_pattern(rule_number)
        return

    def resolve_pattern(self, rule_number):
        rule_content = self.rules[rule_number]
        # If just letters, easy to create regex pattern
        if re.match('^[A-Za-z]*$', rule_content):
            pattern = '(?:[' + rule_content + '])'
        # Otherwise it needs some work to make the regex pattern
        else:
            # If there's an OR separator then calculate all options
            if OR_SEPARATOR in rule_content:
                options = rule_content.split(OR_SEPARATOR)
            else:
                options = [rule_content]  # But if just the one
            pattern = '(?:'  # Pattern start
            for option in options:
                option_pattern = '(?:'  # Option pattern start
                for component in (option.strip()).split(SPACE_SEPARATOR):
                    option_pattern += self.patterns_resolved[component]
                option_pattern += ')'  # Option pattern end
                if options.index(option) + 1 != len(options):
                    option_pattern += '|'  # Concatenate a OR pipe if more to go
                pattern += option_pattern
            pattern += ')'  # Pattern end
        # Common ======================================================
        self.patterns_resolved[rule_number] = pattern
        self.patterns_unresolved.remove(rule_number)
        return

    def check_all_against_rule(self, rule_number):
        count = 0
        pattern_lookup = self.patterns_resolved[rule_number]
        # The rule is just a single regex pattern (i.e. Part 1)
        if type(pattern_lookup) is str:
            for image in self.images:
                if re.match('^' + pattern_lookup + '$', image):
                    count += 1
        # The rule is a list of possible regex patterns (i.e. Part 2)
        else:
            for image in self.images:
                valid_image = False  # Presume False
                for pattern in pattern_lookup:
                    if re.match('^' + pattern + '$', image):
                        count += 1
                        valid_image = True
                if valid_image:
                    continue
        return count

    def resolve_all_patterns_with_loops(self):
        self.resolve_all_pattern(3)
        # 0: 8 11
        # 8: 42 | 42 8
        # 11: 42 31 | 42 11 31
        # ==========
        # 0:
        # - 42 42 31
        # - 42 42 *11* 31
        # - 42 *8* 42 31
        # - 42 *8* 42 *11* 31
        # - 42 42 42 31
        # - 42 42 *8* 42 31
        # - 42 42 42 31
        # - 42 42 42 31
        # - 42 42 *8* 42 *11* 31
        # - 42 42 42 42 *11* 31 31
        # Ultimately, it's just gonna be a variable number of rule 42s + a variable number of rule 31s
        # (Where there are more rule 42s than rule 31s)
        # And because there's a limit to the image size, so we can just try under e.g. 50
        # (After getting the answer, I reduced until it found smaller ranges that still worked, improving performance)
        pattern_42 = self.patterns_resolved['42']
        pattern_31 = self.patterns_resolved['31']
        pattern_0 = []
        for x in range(2, 7):
            for y in range(1, 5):
                if x > y:
                    pattern_0.append(pattern_42 * x + pattern_31 * y)
        self.patterns_resolved['0'] = pattern_0
        return


def day19_part1(data_input):
    a = MonsterMessages(data_input)
    a.resolve_all_pattern()
    result = a.check_all_against_rule('0')
    logging.info('RESULT: The final sum of all images that match rule 0 is: %d', result)
    return result


def day19_part2(data_input):
    # Instructions are to manually change rules 8 & 11
    data_input['rules']['8'] = '42 | 42 8'
    data_input['rules']['11'] = '42 31 | 42 11 31'
    a = MonsterMessages(data_input)
    a.resolve_all_patterns_with_loops()
    result = a.check_all_against_rule('0')
    logging.info('RESULT: The final sum of all images that match rule 0 is: %d', result)
    return result


# Input Files
test_input = ingest_file.process_rules_and_images('test-input/day19.txt')
main_input = ingest_file.process_rules_and_images('input/day19.txt')
test_input_extra = ingest_file.process_rules_and_images('test-input/day19-extra.txt')

# Test Input - Part 1
if day19_part1(test_input) != 2:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day19_part1(main_input) != 235:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 1 (Extra)
if day19_part1(test_input_extra) != 3:
    raise Exception("FAIL: Part 1 Test (Extra) FAILED!")
else:
    logging.info("PASS: Part 1 Test (Extra) PASSED")

# Test Input - Part 2
if day19_part2(test_input_extra) != 12:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day19_part2(main_input) != 379:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
