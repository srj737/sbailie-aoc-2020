import logging
import sys
import re

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


class Menu:

    def __init__(self, data_input):
        allergens, ingredients = [], []
        self.working_dict = {}
        for line in data_input:
            prepped_line = line.strip().replace('(', '').replace(')', '').replace(',', '')
            item_allergens = prepped_line.split('contains')[1].strip().split(' ')
            item_ingredients = prepped_line.split('contains')[0].strip().split(' ')
            allergens.extend(item_allergens)
            ingredients.extend(item_ingredients)
            for item_allergen in item_allergens:
                if item_allergen not in self.working_dict:
                    self.working_dict[item_allergen] = [item_ingredients]
                else:
                    self.working_dict[item_allergen].append(item_ingredients)
        self.allergens, self.ingredients = set(allergens), set(ingredients)
        self.final_mapping = {}
        return

    def resolve(self):
        while len(self.allergens) != 0:
            dictionary = {k: [] for k in self.allergens}
            for allergen in self.allergens:
                for ingredient in self.ingredients:
                    if all(ingredient in x for x in self.working_dict[allergen]):
                        logging.debug('Ingredient: %s, was present for all items flagged for Allergen: %s', ingredient,
                                      allergen)
                        dictionary[allergen].append(ingredient)
            to_remove = []
            while any(len(x) == 1 for x in dictionary.values()):
                for allergen in dictionary:
                    if len(dictionary[allergen]) == 1:
                        self.found_mapping(dictionary[allergen][0], allergen)
                        to_remove.append(allergen)
                for allergen in to_remove:
                    del (dictionary[allergen])
        return

    def found_mapping(self, ingredient, allergen):
        self.allergens.remove(allergen)
        self.ingredients.remove(ingredient)
        self.final_mapping[allergen] = ingredient
        del (self.working_dict[allergen])
        for dict_allergen, dict_recipes in self.working_dict.items():
            for idx, item in enumerate(dict_recipes):
                if ingredient in item:
                    self.working_dict[dict_allergen][idx].remove(ingredient)
        return


def day21_part1(data_input):
    menu = Menu(data_input)
    menu.resolve()
    non_allergen_occurrences = 0
    full_raw_menu = ''  # Needed as with full input, false positives are tripped by substrings
    for line in data_input:
        # So we put it all into a single string where we can assure all ingredients are surrounded by spaces.
        full_raw_menu = full_raw_menu + ' ' + line
    for non_allergen_ingredient in menu.ingredients:
        non_allergen_occurrences += len(re.findall(' ' + non_allergen_ingredient + ' ', full_raw_menu))
    logging.info('RESULT: The number of times ingredients WITH NO allergen occurred in the menu is: %d',
                 non_allergen_occurrences)
    return non_allergen_occurrences


def day21_part2(data_input):
    menu = Menu(data_input)
    menu.resolve()
    result = ''
    sorted_allergens = [i for i in sorted(menu.final_mapping.keys())]
    for allergens in sorted_allergens:
        result += menu.final_mapping[allergens] + ','
    result = result[:-1]  # Remove last comma
    logging.info('RESULT: The comma separated ingredients sorted by alphabetised allergens are: %s', result)
    return result


# Input Files
test_input = ingest_file.strings_on_lines('test-input/day21.txt')
main_input = ingest_file.strings_on_lines('input/day21.txt')

# Test Input - Part 1
if day21_part1(test_input) != 5:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day21_part1(main_input) != 2125:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day21_part2(test_input) != 'mxmxvkd,sqjhc,fvjkl':
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day21_part2(main_input) != 'phc,spnd,zmsdzh,pdt,fqqcnm,lsgqf,rjc,lzvh':
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
