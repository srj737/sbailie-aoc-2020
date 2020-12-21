import logging
import sys
import math

import ingest_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(levelname)s: %(asctime)s.%(msecs)03d - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

BACKGROUND = '.'
FOREGROUND = '#'
MONSTER_WIDTH = 20
MONSTER_HEIGHT = 3
MONSTER_SIZE = 15
BORDER_SIZE = 1
NUM_OF_EDGES = 8  # [top, bottom, left, right, reverse(top), reverse(bottom), reverse(left), reverse(right)]
ORIENTATIONS = 8


def reverse_string(string):
    return string[::-1]


def get_nessie_indexes(row_idx, col_idx):
    # Starting with the index at the top left corner, Nessie is present if the following indexes are FOREGROUND:
    # ..................O.
    # O....OO....OO....OOO
    # .O..O..O..O..O..O...
    #
    return [
        [row_idx, col_idx + 18],
        [row_idx + 1, col_idx],
        [row_idx + 1, col_idx + 5],
        [row_idx + 1, col_idx + 6],
        [row_idx + 1, col_idx + 11],
        [row_idx + 1, col_idx + 12],
        [row_idx + 1, col_idx + 17],
        [row_idx + 1, col_idx + 18],
        [row_idx + 1, col_idx + 19],
        [row_idx + 2, col_idx + 1],
        [row_idx + 2, col_idx + 4],
        [row_idx + 2, col_idx + 7],
        [row_idx + 2, col_idx + 10],
        [row_idx + 2, col_idx + 13],
        [row_idx + 2, col_idx + 16]
    ]


class ImageFromTiles:

    def __init__(self, data_input):
        self.tiles = data_input.copy()  # The master store for the tiles. Rotating and flipping is reflected here.
        self.unassigned = set(self.tiles.keys())  # A set of tile Ids not yet placed in the jigsaw
        self.image_size = int(round(math.sqrt(len(self.tiles))))  # The number of tiles in the image
        self.tile_size = int(len(list(self.tiles.values())[0]))  # The number of pixels in each tile
        # Initialise dicts and lists =========================================================================
        self.edges = {}  # Will store the current edges of the tiles (e.g. '2314': [t, b, l, r, r(t), r(b), r(l), r(r)]
        self.edge_matches = {}  # Will store the number of matches each edge currently has will all other tiles.
        self.corner_tiles = []  # Will store the four corner tiles. (for ease of answer to part 1).
        self.monster_counts = []  # Will store the num of monsters found for each of the 8 orientations of the image.
        # BELOW: An array representation of the tile ids once edges have been matched
        self.combined_tile_ids = [[0 for j in range(self.image_size)] for i in range(self.image_size)]
        # BELOW: An 2D array of the final image
        self.final_image = [[0 for j in range(self.image_size * self.tile_size - BORDER_SIZE * 2 * self.image_size)] for
                            i in
                            range(self.image_size * self.tile_size - BORDER_SIZE * 2 * self.image_size)]
        for tile_id in self.tiles:
            self.calc_edges(tile_id)  # Edges are calculated and assigned to 'self.edges'.
        for tile_id in self.tiles:
            self.edge_matches[tile_id] = [-1] * NUM_OF_EDGES  # '-1' is just to initialise.
            self.calc_edge_matches(tile_id)  # Edge matches are calculated and assigned to 'self.edge_matches'.
            # This needs to be a separate for loop as the edges need calculated first.
        # Process tiles into a single final image ===========================================================
        self.find_corner_tiles()
        self.fit_tiles_together()
        self.build_final_image()
        return

    def calc_edges(self, tile_id):
        tile = self.tiles[tile_id]
        t, b = tile[0], tile[-1]
        l, r = '', ''
        for row in tile:
            l += row[0]
            r += row[-1]
        self.edges[tile_id] = [t, b, l, r, reverse_string(t), reverse_string(b), reverse_string(l), reverse_string(r)]
        return

    def calc_edge_matches(self, tile_id):
        for idx, edge in enumerate(self.edges[tile_id]):
            matching = []
            for poss_match_id, poss_match_edges in self.edges.items():
                if poss_match_id != tile_id:  # Obviously a tile's edge cannot match with an edge from the same tile.
                    if edge in poss_match_edges:
                        matching.append(poss_match_id)
            self.edge_matches[tile_id][idx] = len(matching)
        return

    def find_corner_tiles(self):
        corners = []
        for tile_id, edge_match_counts in self.edge_matches.items():
            match_sum = 0
            for match_count in edge_match_counts:
                match_sum += match_count
            if match_sum == 4:  # Only 4 matching edges means a corner. (i.e. 2 Edges plus two reverse_strings.)
                corners.append(tile_id)
        self.corner_tiles = corners
        return

    def fit_tiles_together(self):
        top_left = self.corner_tiles[0]  # Just pick any corner tile as the top left.
        # Orientate top left tile ======================
        if self.edge_matches[top_left] != [0, 1, 0, 1, 0, 1, 0, 1]:
            for check_state in range(ORIENTATIONS):
                self.next_orientation(top_left, check_state)
                if self.edge_matches[top_left] == [0, 1, 0, 1, 0, 1, 0, 1]:
                    break
        # Complete the jigsaw: first down left hand column, then out to the right for each row
        for row_idx in range(0, self.image_size):
            if row_idx == 0:
                next_tile = top_left
            else:
                next_tile = self.find_next_tile(self.combined_tile_ids[row_idx - 1][0], 'below')
            self.combined_tile_ids[row_idx][0] = next_tile
            self.unassigned.remove(next_tile)
            for col_idx in range(1, self.image_size):
                next_one = self.find_next_tile(self.combined_tile_ids[row_idx][col_idx - 1], 'right')
                self.combined_tile_ids[row_idx][col_idx] = next_one
                self.unassigned.remove(next_one)
        return

    def find_next_tile(self, tile_id, direction):
        if direction == 'below':
            # This title's BOTTOM edge must match the next tile's TOP edge.
            current_tile_edge_index = 1  # Edge index '1' is the BOTTOM edge
            next_tile_edge_index = 0  # Edge index '0' is the TOP edge
        elif direction == 'right':
            # This title's RIGHT edge must match the next tile's LEFT edge. (Not reverse as L&R both read top to bottom)
            current_tile_edge_index = 3  # Edge index '3' is the RIGHT edge
            next_tile_edge_index = 2  # Edge index '2' is the LEFT edge
        found_match = False
        edge_to_match = self.edges[tile_id][current_tile_edge_index]
        for possible in self.unassigned:
            for check_state in range(ORIENTATIONS):
                self.next_orientation(possible, check_state)
                if self.edges[possible][next_tile_edge_index] == edge_to_match:
                    found_match = possible
                    break
            if found_match:
                break
        return found_match

    def build_final_image(self):
        for tile_row_idx, tile_row in enumerate(self.combined_tile_ids):
            for tile_col_idx, tile_id in enumerate(tile_row):
                borderless = self.strip_border(tile_id)
                x_off = tile_row_idx * (self.tile_size - 2 * BORDER_SIZE)
                y_off = tile_col_idx * (self.tile_size - 2 * BORDER_SIZE)
                for row_idx, row in enumerate(borderless):
                    for col_idx, char in enumerate(row):
                        self.final_image[x_off + row_idx][y_off + col_idx] = char
        return

    def strip_border(self, tile_id):
        old_tile = self.tiles[tile_id]
        new_tile = []
        for old_row_idx, old_row in enumerate(old_tile):
            if old_row_idx != 0 and old_row_idx != len(old_tile) - 1:
                new_tile.append(old_row[1:-1])
        return new_tile

    def count_foreground(self):
        counter = 0
        for row_idx, row in enumerate(self.final_image):
            for col_idx, value in enumerate(row):
                if value == FOREGROUND:
                    counter += 1
        return counter

    # ================================================================
    # Below 3 functions are rotating and flipping an individual tile
    # ================================================================

    def next_orientation(self, tile_id, state):
        if state == 0:
            return
        else:
            self.rotate_tile(tile_id)
            if state == 4:
                self.flip_tile(tile_id)
            return

    def flip_tile(self, tile_id):
        old_tile = self.tiles[tile_id]
        new_tile = []
        for row in old_tile:
            new_tile.insert(0, row)
        self.tiles[tile_id] = new_tile
        self.calc_edges(tile_id)  # Recalculate edges
        self.calc_edge_matches(tile_id)  # Recalculate edge matching
        return

    def rotate_tile(self, tile_id):
        old_tile = self.tiles[tile_id]
        new_tile = []
        for n in range(len(old_tile)):
            new_row = ''
            for old_row in old_tile:
                new_row = old_row[n] + new_row
            new_tile.append(new_row)
        self.tiles[tile_id] = new_tile
        self.calc_edges(tile_id)  # Recalculate edges
        self.calc_edge_matches(tile_id)  # Recalculate edge matching
        return

    # ================================================================
    # Below 3 functions are rotating and flipping the final image
    # ================================================================

    def next_orientation_final_image(self, state):
        if state == 0:
            return
        else:
            self.rotate_final_image()
            if state == 4:
                self.flip_final_image()
            return

    def flip_final_image(self):
        old_final_image = self.final_image
        new_final_image = []
        for old_row in old_final_image:
            new_final_image.insert(0, old_row)
        self.final_image = new_final_image
        return

    def rotate_final_image(self):
        old_final_image = self.final_image
        new_final_image = []
        for n in range(len(old_final_image)):
            new_row = []
            for old_row in old_final_image:
                new_row.insert(0, old_row[n])
            new_final_image.append(new_row)
        self.final_image = new_final_image
        return

    # ================================================================
    # Below 3 functions are rotating and flipping the final image
    # ================================================================

    def search_for_nessie(self):
        for check_state in range(ORIENTATIONS):
            self.next_orientation_final_image(check_state)
            monster_count = 0
            for row_idx, row in enumerate(self.final_image):
                for col_idx, value in enumerate(row):
                    if 0 <= row_idx <= len(self.final_image) - MONSTER_HEIGHT and 0 <= col_idx <= len(
                            row) - MONSTER_WIDTH:
                        indexes = get_nessie_indexes(row_idx, col_idx)
                        if all(self.final_image[index[0]][index[1]] == FOREGROUND for index in indexes):
                            # Monster Found!
                            monster_count += 1
            self.monster_counts.append(monster_count)
            logging.debug('Using orientation state: %d, there were %d monsters found!', check_state, monster_count)
        return


def day20_part1(image):
    result = math.prod([int(x) for x in image.corner_tiles])
    logging.info('RESULT: The product of all 4 tile Ids of the 4 corner tiles is: %d', result)
    return result


def day20_part2(image):
    image.search_for_nessie()
    result = image.count_foreground() - max(image.monster_counts) * MONSTER_SIZE
    logging.info('RESULT: The number of # in the image that are NOT involved in the %d found monsters is: %d',
                 max(image.monster_counts), result)
    return result


# Input Files
test_input = ingest_file.process_image_tiles('test-input/day20.txt')
main_input = ingest_file.process_image_tiles('input/day20.txt')

# Process Tiles
test_image = ImageFromTiles(test_input)
main_image = ImageFromTiles(main_input)

# Test Input - Part 1
if day20_part1(test_image) != 20899048083289:
    raise Exception("FAIL: Part 1 Test FAILED!")
else:
    logging.info("PASS: Part 1 Test PASSED")

# Real Input - Part 1
if day20_part1(main_image) != 54755174472007:
    raise Exception("FAIL: Part 1 FAILED!")
else:
    logging.info("PASS: Part 1 PASSED")

# Test Input - Part 2
if day20_part2(test_image) != 273:
    raise Exception("FAIL: Part 2 Test FAILED!")
else:
    logging.info("PASS: Part 2 Test PASSED")

# Real Input - Part 2
if day20_part2(main_image) != 1692:
    raise Exception("FAIL: Part 2 FAILED!")
else:
    logging.info("PASS: Part 2 PASSED")
