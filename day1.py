import ingest_file
import pandas


def day1_part1(array):
    results = []
    for i in array:
        print("Completed: " + str(array.index(i) + 1) + "/" + str(len(array)))
        for j in array:
            i_idx = array.index(i)
            j_idx = array.index(j)
            if i_idx != j_idx:
                if (i + j) == target:
                    factors = [i, j]
                    factors.sort()
                    i, j = factors[0], factors[1]
                    final = [i * j, i + j, i, j]
                    if final not in results:
                        results.append(final)
    print(pandas.DataFrame(results))
    return results


def day1_part2(array):
    results = []
    for i in array:
        print("Completed: " + str(array.index(i) + 1) + "/" + str(len(array)))
        for j in array:
            for k in array:
                i_idx = array.index(i)
                j_idx = array.index(j)
                k_idx = array.index(k)
                if (i_idx != j_idx) and (i_idx != k_idx) and (j_idx != k_idx):
                    if (i + j + k) == target:
                        factors = [i, j, k]
                        factors.sort()
                        i, j, k = factors[0], factors[1], factors[2]
                        final = [i * j * k, i + j + k, i, j, k]
                        if final not in results:
                            results.append(final)
    print(pandas.DataFrame(results))
    return results


test_array = ingest_file.int_on_lines('test-input/day1.txt')
array = ingest_file.int_on_lines('input/day1.txt')
target = 2020

x = day1_part1(test_array)
if x != [[514579, 2020, 299, 1721]]:
    raise Exception("Part 1 Test FAILED!")
else:
    print("Part 1 Test PASSED")

y = day1_part2(test_array)
if y != [[241861950, 2020, 366, 675, 979]]:
    raise Exception("Part 2 Test FAILED!")
else:
    print("Part 2 Test PASSED")

x = day1_part1(array)
y = day1_part2(array)
