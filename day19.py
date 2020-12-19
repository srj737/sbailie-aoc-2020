import logging
import sys
import re

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

OR_SEPARATOR = '|'
SPACE_SEPARATOR = ' '


class MonsterMessages():

    def __init__(self, data_input):
        self.images = data_input['images'].copy()
        self.rules = data_input['rules'].copy()
        self.patterns_unresolved = set([x for x in self.rules])
        self.patterns_resolved = {}
        self.resolve_all_pattern()
        return

    def resolve_all_pattern(self):
        # Iterate until all rules get resolve into patterns
        while len(self.patterns_unresolved) != 0:
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
        for image in self.images:
            if self.check_against_rule(rule_number, image):
                count += 1
        return count

    def check_against_rule(self, rule_number, image):
        return re.match('^' + self.patterns_resolved[rule_number] + '$', image)


def day19(data_input):
    a = MonsterMessages(data_input)
    result = a.check_all_against_rule('0')
    logging.info('RESULT: The final sum of all images that match rule 0 is: %d', result)
    return result


# Input Files
test_input = ingest_file.process_rules_and_images('test-input/day19.txt')
main_input = ingest_file.process_rules_and_images('input/day19.txt')

# Test Input - Part 1
if day19(test_input) != 2:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day19(main_input) != 235:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
# if day19(test_input, 'B') != ([231, 51, 46, 1445, 669060, 23340], 694173):
#    raise Exception("FAIL: Part 2 Test FAILED!")
# else:
#    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
# if day19(main_input, 'B')[1] != 158183007916215:
#    raise Exception("FAIL: Part 2 FAILED!")
# else:
#    logging.info("PASS: Part 2 PASSED")
