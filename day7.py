import ingest_file
import re
from datetime import datetime


def check_if_contains(bag_dictionary, check_bag, check_colour):
    if check_colour in bag_dictionary[check_bag]:
        # It's directly in the bag we are looking at
        return True
    else:
        # Otherwise check in all constituent parts
        return any(
            check_if_contains(bag_dictionary, inner_bag, check_colour) for inner_bag in bag_dictionary[check_bag])


def process_bag_rules(rules):
    dictionary = {}
    for rule in rules:
        key_colour = rule.split(' bags contain ')[0]
        values = (rule.split(' bags contain ')[1]).strip().replace('.', '').replace(' bags', '').replace(' bag',
                                                                                                         '').split(', ')
        processed_values = []
        if values == ['no other']:
            processed_values = []
        else:
            for value in values:
                preceding_num_pattern = "^[0-9]*"
                ending_2_word_pattern = "[a-z]*\s[a-z]*$"
                num = int(re.match(preceding_num_pattern, value)[0])
                colour = re.search(ending_2_word_pattern, value)[0]
                for i in range(num):
                    processed_values.append(colour)
        dictionary[key_colour] = processed_values
    return dictionary


# Took 16 minutes to process with the real array, lol...
def day7_part1(array, target):
    bag_dictionary = process_bag_rules(array)
    contains_target_count, bags_checked = 0, 0
    for bag in bag_dictionary:
        if check_if_contains(bag_dictionary, bag, target):
            contains_target_count += 1
            bag_dictionary[bag] = [
                target]  # We found a target bag in here, so we can replace it's inner bags with just the target
        else:
            bag_dictionary[bag] = [
            ]  # We never found a target bag in here, so we can replace it's inner bags with nothing
        bags_checked += 1
        print("Tested " + str(bags_checked) + " out of " + str(len(bag_dictionary)) + " bags.")
    print("RESULT AT " + str(datetime.now()) + ": The count of all bags that contain at least one " + str(
        target) + " bag, is: " + str(
        contains_target_count))
    return contains_target_count


def add_counts_to_dictionary(dictionary):
    for k, v in dictionary.items():
        dictionary[k] = [False, v]
    return dictionary


def count_inner_bags(bag_dictionary_with_counts, check_bag):
    if bag_dictionary_with_counts[check_bag][0] is not False:
        # Already counted this bag, don't bother counting again
        return bag_dictionary_with_counts[check_bag][0]
    component_bags = bag_dictionary_with_counts[check_bag][1]
    count = len(component_bags)
    for inner_bag in component_bags:
        # For each inner bag
        if bag_dictionary_with_counts[inner_bag][0] is not False:
            # We already have counted this inner bag, so just remove add it's sub-bags to the count
            count += bag_dictionary_with_counts[inner_bag][0]
        else:
            # We haven't counted this bag yet, so count it now
            count += count_inner_bags(bag_dictionary_with_counts, inner_bag)
    # Assign count value so we don't need to check again
    bag_dictionary_with_counts[check_bag] = [count, []]
    return count


# Took literal seconds to process with the real array, lol...
def day7_part2(array, target):
    bags_checked = 0
    bag_dictionary = add_counts_to_dictionary(process_bag_rules(array))
    for bag in bag_dictionary:
        count_inner_bags(bag_dictionary, bag)
        bags_checked += 1
        print("Tested " + str(bags_checked) + " out of " + str(len(bag_dictionary)) + " bags.")
    target_count = bag_dictionary[target][0]
    print("RESULT AT " + str(datetime.now()) + ": The number of bags within " + str(
        target) + ", is: " + str(
        target_count))
    return target_count


target_colour = 'shiny gold'

test_array_p1 = ingest_file.strings_on_lines('test-input/day7-part1.txt')
test_array_p2 = ingest_file.strings_on_lines('test-input/day7-part2.txt')
array = ingest_file.strings_on_lines('input/day7.txt')

# Test Input - Part 1
if day7_part1(test_array_p1, target_colour) != 4:
    raise Exception("Part 1 Test FAILED!")
else:
    print("Part 1 Test PASSED")

# Real Input - Part 1
# if day7_part1(array, target_colour) != 242:
#    raise Exception("Part 1 FAILED!")
# else:
#    print("Part 1 PASSED")

# Test Input - Part 2
if day7_part2(test_array_p2, target_colour) != 126:
    raise Exception("Part 2 Test FAILED!")
else:
    print("Part 2 Test PASSED")

# Real Input - Part 2
if day7_part2(array, target_colour) != 176035:
   raise Exception("Part 2 FAILED!")
else:
   print("Part 2 PASSED")
