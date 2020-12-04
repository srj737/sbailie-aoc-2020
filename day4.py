import ingest_file
import re

required_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
optional_keys = ['cid']


def validate_yr(value, min, max):
    # Four digits
    pattern = '^[0-9]{4}$'
    result = re.match(pattern, value)
    if not result:
        return False
    if int(value) < min or int(value) > max:
        return False
    return True


class Switcher(object):
    def validate_field(self, key, value):
        method_name = 'validate_' + str(key)
        method = getattr(self, method_name, lambda: "Invalid key")
        return method(value)

    def validate_byr(self, value):
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        if not validate_yr(value, 1920, 2002):
            return False
        return True

    def validate_iyr(self, value):
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        if not validate_yr(value, 2010, 2020):
            return False
        return True

    def validate_eyr(self, value):
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        if not validate_yr(value, 2020, 2030):
            return False
        return True

    def validate_hgt(self, value):
        # hgt (Height) - a number followed by either cm or in:
            # If cm, the number must be at least 150 and at most 193.
            # If in, the number must be at least 59 and at most 76.
        pattern = '^[0-9]{3}cm$|^[0-9]{2}in$'
        result = re.match(pattern, value)
        if not result:
            return False
        if len(value) == 5:
            # In cm
            num = int(value.replace('cm', '').strip())
            min = 150
            max = 193
        elif len(value) == 4:
            # In cm
            num = int(value.replace('in', '').strip())
            min = 59
            max = 76
        else:
            return False
        if num < min or num > max:
            return False
        return True

    def validate_hcl(self, value):
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        pattern = '^#([0-9]|[a-f]){6}$'
        result = re.match(pattern, value)
        if not result:
            return False
        return True

    def validate_ecl(self, value):
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        pattern = '^(amb|blu|brn|gry|grn|hzl|oth)$'
        result = re.match(pattern, value)
        if not result:
            return False
        return True

    def validate_pid(self, value):
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        pattern = '^[0-9]{9}$'
        result = re.match(pattern, value)
        if not result:
            return False
        return True

    def validate_cid(self, value):
        return True



# Verify Passport
def verify_req_fields_passport(array):
    valid_count = 0
    valid_list = []
    for passport in array:
        valid = True
        for key in required_keys:
            if key in passport:
                continue
            else:
                valid = False
        if valid is True:
            valid_list.append(passport)
            valid_count += 1
    print("Final valid passport count: " + str(valid_count))
    return valid_count, valid_list


# Verify Passport with data validation
def validate_fields_data_passports(array):
    a = Switcher()
    valid_count = 0
    for passport in array:
        valid = True
        for key in passport:
            value = passport[key]
            key_valid = a.validate_field(key, value)
            if key_valid is True:
                continue
            else:
                valid = False
        if valid is True:
            valid_count += 1
    print("Final valid passport count: " + str(valid_count))
    return valid_count


def day4_part1(array):
    return verify_req_fields_passport(array)[0]


def day4_part2(array):
    first_pass = verify_req_fields_passport(array)[1]
    return validate_fields_data_passports(first_pass)


test_array1 = ingest_file.list_of_dicts('test-input/day4.txt')
test_array2 = ingest_file.list_of_dicts('test-input/day4-part2-valid.txt')
test_array3 = ingest_file.list_of_dicts('test-input/day4-part2-invalid.txt')
array = ingest_file.list_of_dicts('input/day4.txt')

x = day4_part1(test_array1)
if x != 2:
    raise Exception("Part 1 Test FAILED!")
else:
    print("Part 1 Test PASSED")

y = day4_part2(test_array2)
if y != 4:
    raise Exception("Part 2 (Valid) Test FAILED!")
else:
    print("Part 2 (Valid) Test PASSED")

y = day4_part2(test_array3)
if y != 0:
    raise Exception("Part 2 (Invalid) Test FAILED!")
else:
    print("Part 2 (Invalid) Test PASSED")

x = day4_part1(array)
y = day4_part2(array)
