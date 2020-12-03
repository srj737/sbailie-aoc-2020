import ingest_file

part1_slope = [3, 1]
part2_slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]


def day3_part1(array, slope_x, slope_y):
    tree_count = 0
    curr_x, curr_y = 0, 0
    max_y = len(array) - 1
    max_x = len(array[0]) - 1
    while curr_y <= max_y:
        check = array[curr_y][curr_x]
        if check is '#':
            tree_count += 1
        curr_x = (curr_x + slope_x) % (max_x + 1)
        curr_y = curr_y + slope_y
        print("Currently at row " + str(curr_y) + "/" + str(max_y))
    print("Final tree count: " + str(tree_count))
    return tree_count


def day3_part2(array, array_of_slopes):
    product = 1
    for slope in array_of_slopes:
        product *= day3_part1(array, slope[0], slope[1])
    print("Final multiplication of all trees in all slopes: " + str(product))
    return product


test_array = ingest_file.dot_hash_matrix('test-input/day3.txt')
array = ingest_file.dot_hash_matrix('input/day3.txt')

x = day3_part1(test_array, part1_slope[0], part1_slope[1])
if x != 7:
    raise Exception("Part 1 Test FAILED!")
else:
    print("Part 1 Test PASSED")

y = day3_part2(test_array, part2_slopes)
if y != 336:
    raise Exception("Part 2 Test FAILED!")
else:
    print("Part 2 Test PASSED")

x = day3_part1(array, part1_slope[0], part1_slope[1])
y = day3_part2(array, part2_slopes)
