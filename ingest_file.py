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


def char_matrix(filename):
    results = []
    with open(filename, 'r') as infile:
        for line in infile:
            result = []
            for char in line.strip():
                result.append(char)
            results.append(result)
    return results


def strings_separated_by_new_lines(filename, mid_obj_separator=''):
    results = []
    lines = strings_on_lines(filename)
    result = ""
    for line in lines:
        if line == '\n' or lines.index(line) >= len(lines) - 1:
            # New object
            result = result + mid_obj_separator + str(line)
            results.append(result)
            result = ""
        else:
            # Add to current object
            result = result + str(line)
    if result != '':
        results.append(result)
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


def string_separated_by_separator(filename, separator):
    line = strings_separated_by_new_lines(filename)[0].strip()
    return line.split(separator)


def ints_separated_by_separator(filename, seperator):
    line = strings_separated_by_new_lines(filename)[0].strip()
    numbers = line.split(seperator)
    results = []
    for number in numbers:
        results.append(int(number))
    return results


def ints_on_single_line(filename):
    line = strings_separated_by_new_lines(filename)[0].strip()
    numbers = []
    for number in line:
        numbers.append(int(number))
    return numbers


def process_train_tickets(filename):
    lines = strings_on_lines(filename)
    rules, my_ticket, other_tickets = [], '', []
    flag = 'Rules'
    for line in lines:
        line = line.strip()
        if line != '':
            if line == 'your ticket:':
                flag = 'myTicket'
            elif line == 'nearby tickets:':
                flag = 'otherTickets'
            else:
                if flag == 'Rules':
                    rules.append(line)
                elif flag == 'myTicket':
                    my_ticket = [int(i) for i in line.split(',')]
                elif flag == 'otherTickets':
                    other_tickets.append([int(i) for i in line.split(',')])
    rules_dict = {}
    for field in rules:
        field_name = field.split(': ')[0]
        ranges = field.split(': ')[1]
        lower_range = ranges.split(' or ')[0]
        upper_range = ranges.split(' or ')[1]
        lower_range_lb, lower_range_ub = int(lower_range.split('-')[0]), int(lower_range.split('-')[1])
        upper_range_lb, upper_range_ub = int(upper_range.split('-')[0]), int(upper_range.split('-')[1])
        rules_dict[field_name] = [lower_range_lb, lower_range_ub, upper_range_lb, upper_range_ub]
    return {'rules': rules_dict, 'my_ticket': my_ticket, 'other_tickets': other_tickets}


def process_rules_and_images(filename):
    rules, images, temp = [], [], []
    data = strings_on_lines(filename)
    for line in data:
        line = line.strip()
        if line == '':
            rules, temp = temp, []
            continue
        temp.append(line)
    images = temp
    rules_dict = {}
    for idx, rule in enumerate(rules):
        rules_dict[rule.split(': ')[0]] = rule.split(': ')[1].replace('\"', '').replace('\'', '')
    return {'rules': rules_dict, 'images': images}


def process_image_tiles(filename):
    tile_array = strings_separated_by_new_lines(filename, ' ')
    tile_dict = {}
    for tile in tile_array:
        tile_id = tile.split(': ')[0].replace('Tile ', '')
        tile_rows = tile.split(': ')[1].split(' ')
        tile_dict[tile_id] = tile_rows
    return tile_dict