import ingest_file


def calc_unique_yeses(code):
    string = code.replace(' ', '')  # Strip Spaces
    sorted_characters = sorted(string)  # Sort letters into a list
    no_duplicates = list(
        dict.fromkeys(sorted_characters))  # Convert to dictionary then back to a list to remove duplicates
    count = len(no_duplicates)  # Count unique answers
    return count, no_duplicates


def calc_unique_yeses_part2(code):
    list_of_peep = code.split(' ')  # Strip into a list of each person
    cumulative = calc_unique_yeses(list_of_peep[0])[1]  # Initialise with first person
    for persons_code in list_of_peep:
        this_person = calc_unique_yeses(persons_code)[1]
        cumulative = list(set(this_person) & set(cumulative))
    count = len(cumulative)  # Count unique answers
    return count


def process_forms(array, part=1):
    sum_value = 0
    for form in array:
        if part == 1:
            sum_value += calc_unique_yeses(form)[0]
        if part == 2:
            sum_value += calc_unique_yeses_part2(form)
    return sum_value


def day6_part1(array):
    result = process_forms(array)
    print("The sum of yes answers from all members in all groups: " + str(result))
    return result


def day6_part2(array):
    result = process_forms(array, 2)
    print("The sum of yes answers from all members in all groups: " + str(result))
    return result


test_array = ingest_file.strings_separated_by_new_lines('test-input/day6.txt')
array = ingest_file.strings_separated_by_new_lines('input/day6.txt')

# Test Input - Part 1
if day6_part1(test_array) != 11:
    raise Exception("Part 1 Test FAILED!")
else:
    print("Part 1 Test PASSED")

# Real Input - Part 1
if day6_part1(array) != 6387:
    raise Exception("Part 1 FAILED!")
else:
    print("Part 1 PASSED")

# Test Input - Part 2
if day6_part2(test_array) != 6:
    raise Exception("Part 2 Test FAILED!")
else:
    print("Part 2 Test PASSED")

# Real Input - Part 2
if day6_part2(array) != 3039:
    raise Exception("Part 2 FAILED!")
else:
    print("Part 2 PASSED")
