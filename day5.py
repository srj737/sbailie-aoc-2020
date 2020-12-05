import ingest_file

num_of_row_chars = 7
num_of_col_chars = 3
row_bin_zero = "F"
row_bin_one = "B"
col_bin_zero = "L"
col_bin_one = "R"


def calc_seat(code):
    row, col = "", ""
    for i, char in enumerate(code):
        if i < num_of_row_chars:
            if char == row_bin_zero:
                row += '0'
            elif char == row_bin_one:
                row += '1'
        else:
            if char == col_bin_zero:
                col += '0'
            elif char == col_bin_one:
                col += '1'
    row = int(row, 2)
    col = int(col, 2)
    print("Seat Number: Row " + str(row) + " and Column " + str(col))
    return row, col

def calc_seat_id(code):
    row, col = calc_seat(code)
    return (row * 8) + col


def calc_seat_ids(array):
    results = []
    for code in array:
        results.append(calc_seat_id(code))
    return results


def day5_part1(array):
    results = calc_seat_ids(array)
    value = max(results)
    print("Maximum Seat Id on Flight: " + str(value))
    return value


def day5_part2(array):
    results = []
    for code in array:
        results.append(calc_seat_id(code))
    results.sort()
    missing = []
    for i in range(min(results) + 1, max(results)):
        if ((i - 1) in results) and (i not in results) and ((i + 1) in results):
            missing.append(i)
    print("Seat IDs missing from flight!: " + str(missing))
    return missing


test_array = ingest_file.strings_on_lines('test-input/day5.txt')
array = ingest_file.strings_on_lines('input/day5.txt')

x = calc_seat_ids(test_array)
if x != [357, 567, 119, 820]:
    raise Exception("Part 1 Test FAILED!")
else:
    print("Part 1 Test PASSED")

x = day5_part1(array)
y = day5_part2(array)
if y != [623]:
    raise Exception("Part 2 (Valid) Test FAILED!")
else:
    print("Part 2 (Valid) Test PASSED")
