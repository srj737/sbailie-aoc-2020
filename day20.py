import logging
import sys
import math

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


def reverse_string(string):
    return string[::-1]


class ImageFromTiles:

    def __init__(self, data_input):
        self.tiles = data_input.copy()
        self.edges = {}
        self.edge_matches = {}
        self.corner_tiles = []
        for tile_id, tile in self.tiles.items():
            t, b = tile[0], tile[-1]
            l, r = '', ''
            for row in tile:
                l += row[0]
                r += row[-1]
            self.edges[tile_id] = [t, b, l, r, reverse_string(t), reverse_string(b), reverse_string(l), reverse_string(r)]
            self.edge_matches[tile_id] = [-1] * 8
        return

    def find_edge_matches(self):
        for tile_id in self.edges:
            for idx, edge in enumerate(self.edges[tile_id]):
                self.edge_matches[tile_id][idx] = len(self.get_matching_edges(edge, tile_id))
        return

    def get_matching_edges(self, edge_string, tile_id):
        matching = []
        for poss_match_id, poss_match_edges in self.edges.items():
            if poss_match_id != tile_id:
                if edge_string in poss_match_edges:
                    matching.append(poss_match_id)
        return matching

    def find_corner_tiles(self):
        corners = []
        for tile_id, edge_match_counts in self.edge_matches.items():
            match_sum = 0
            for match_count in edge_match_counts:
                match_sum += match_count
            if match_sum == 4:  # Only 4 matching edges means a corner. i.e. 2 Edges plus two reverse_strings.
                corners.append(int(tile_id))
        self.corner_tiles = corners
        return


def day20_part1(data_input):
    a = ImageFromTiles(data_input)
    a.find_edge_matches()
    a.find_corner_tiles()
    result = math.prod(a.corner_tiles)
    logging.info('RESULT: The product of all 4 tile Ids of the 4 corner tiles is: %d', result)
    return result


def day20_part2(data_input):
    return 0


# Input Files
test_input = ingest_file.process_image_tiles('test-input/day20.txt')
main_input = ingest_file.process_image_tiles('input/day20.txt')

# Test Input - Part 1
if day20_part1(test_input) != 20899048083289:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day20_part1(main_input) != 54755174472007:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
# if day20_part2(test_input) != 12:
#    raise Exception("FAIL: Part 2 Test FAILED!")
# else:
#    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
# if day20_part2(main_input) != 379:
#    raise Exception("FAIL: Part 2 FAILED!")
# else:
#    logging.info("PASS: Part 2 PASSED")
