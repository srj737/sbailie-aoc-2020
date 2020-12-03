def int_on_lines(filename):
    results = []
    with open(filename, 'r') as infile:
        for line in infile:
            results.append(int(line))
    return results


def strings_on_lines(filename):
    results = []
    with open(filename, 'r') as infile:
        for line in infile:
            results.append(line)
    return results


def dot_hash_matrix(filename):
    results = []
    with open(filename, 'r') as infile:
        for line in infile:
            result = []
            for char in line.strip():
                result.append(char)
            results.append(result)
    return results
