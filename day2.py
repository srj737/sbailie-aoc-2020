import ingest_file


def count_char_in_str(char, str):
    count = 0
    for i in str:
        if i == char:
            count += 1
    return count


def day2_part1(array):
    num_valid = 0
    for line in array:
        print("Completed: " + str(array.index(line) + 1) + "/" + str(len(array)))
        policy = line.split(':')[0]
        passwd = line.split(':')[1].strip()
        min = int(policy.split('-')[0])
        max = int(policy.split('-')[1].split()[0])
        letter = policy.split()[1]
        count = count_char_in_str(letter, passwd)
        if max >= count >= min:
            num_valid += 1
    print("Valid N# of Passwords: " + str(num_valid))
    return num_valid


def day2_part2(array):
    num_valid = 0
    for line in array:
        print("Completed: " + str(array.index(line) + 1) + "/" + str(len(array)))
        policy = line.split(':')[0]
        passwd = line.split(':')[1].strip()
        pos1 = int(policy.split('-')[0]) - 1
        pos2 = int(policy.split('-')[1].split()[0]) - 1
        letter = policy.split()[1]
        check1 = passwd[pos1]
        check2 = passwd[pos2]
        if (check1 == letter or check2 == letter) and not (check1 == letter and check2 == letter):
            num_valid += 1
    print("Valid N# of Passwords: " + str(num_valid))
    return num_valid


test_array = ingest_file.strings_on_lines('test-input/day2.txt')
array = ingest_file.strings_on_lines('input/day2.txt')

x = day2_part1(test_array)
if x != 2:
    raise Exception("Part 1 Test FAILED!")
else:
    print("Part 1 Test PASSED")

y = day2_part2(test_array)
if y != 1:
    raise Exception("Part 2 Test FAILED!")
else:
    print("Part 2 Test PASSED")

x = day2_part1(array)
y = day2_part2(array)
