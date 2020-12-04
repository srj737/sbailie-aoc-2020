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


def strings_separated_by_new_lines(filename):
    results = []
    lines = strings_on_lines(filename)
    result = ""
    for line in lines:
        if lines.index(line) == 1167:
            a = 1
        if line == '\n' or lines.index(line) >= len(lines) - 1:
            #New object
            result = result + str(line)
            results.append(result)
            result = ""
        else:
            #Add to current object
            result = result + str(line)
    finals = []
    for line in results:
        finals.append(line.replace('\n', ' ').strip())
    return finals



def list_of_dicts(filename):
    lines = strings_separated_by_new_lines(filename)
    results = []
    for line in lines:
        single_list = line.split(' ')
        single_dict = {}
        for aspect in single_list:
            key = aspect.split(':')[0]
            value = aspect.split(':')[1]
            single_dict[key] = value
        results.append(single_dict)
    return results
