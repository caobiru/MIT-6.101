"""
6.101 Lab 7:
Six Double-Oh Mines
"""
#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    keys = ("board", "dimensions", "state", "visible")
    # ^ Uses only default game keys. If you modify this you will need
    # to update the docstrings in other functions!
    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(nrows, ncolumns, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       mines (list): List of mines, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """

    def neighbor_mines_count(row, col):
        """
        helper function to count board[row][col]'s neighboring mines 
        """
        neighbor_mines = 0
        for r in range(max(0, row - 1), min(nrows, row + 2)):
            for c in range(max(0, col - 1), min(ncolumns, col + 2)):
                if (r,c) != (row, col) and board[r][c] == ".":
                    neighbor_mines += 1

        return neighbor_mines

    # set up visible and board
    visible = [[False] * ncolumns for _ in range(nrows)]
    board = [[0] * ncolumns for _ in range(nrows)]

    for mine in mines:
        board[mine[0]][mine[1]] = "."

    for row in range(nrows):
        for col in range(ncolumns):
            if board[row][col] == 0:
                board[row][col] = neighbor_mines_count(row, col)

    return {
        "dimensions": (nrows, ncolumns),
        "board": board,
        "visible": visible,
        "state": "ongoing",
    }

    # Original Code
    # board = []
    # for r in range(nrows):
    #     row = []
    #     for c in range(ncolumns):
    #         if [r, c] in mines or (r, c) in mines:
    #             row.append(".")
    #         else:
    #             row.append(0)
    #     board.append(row)
    # visible = []
    # for r in range(nrows):
    #     row = []
    #     for c in range(ncolumns):
    #         row.append(False)
    #     visible.append(row)
    #
    # for r in range(nrows):
    #     for c in range(ncolumns):
    #         if board[r][c] == 0:
    #             neighbor_mines = 0
    #             if 0 <= r - 1 < nrows:
    #                 if 0 <= c - 1 < ncolumns:
    #                     if board[r - 1][c - 1] == ".":
    #                         neighbor_mines += 1
    #             if 0 <= r < nrows:
    #                 if 0 <= c - 1 < ncolumns:
    #                     if board[r][c - 1] == ".":
    #                         neighbor_mines += 1
    #             if 0 <= r + 1 < nrows:
    #                 if 0 <= c - 1 < ncolumns:
    #                     if board[r + 1][c - 1] == ".":
    #                         neighbor_mines += 1
    #             if 0 <= r - 1 < nrows:
    #                 if 0 <= c < ncolumns:
    #                     if board[r - 1][c] == ".":
    #                         neighbor_mines += 1
    #             if 0 <= r < nrows:
    #                 if 0 <= c < ncolumns:
    #                     if board[r][c] == ".":
    #                         neighbor_mines += 1
    #             if 0 <= r + 1 < nrows:
    #                 if 0 <= c < ncolumns:
    #                     if board[r + 1][c] == ".":
    #                         neighbor_mines += 1
    #             if 0 <= r - 1 < nrows:
    #                 if 0 <= c + 1 < ncolumns:
    #                     if board[r - 1][c + 1] == ".":
    #                         neighbor_mines += 1
    #             if 0 <= r < nrows:
    #                 if 0 <= c + 1 < ncolumns:
    #                     if board[r][c + 1] == ".":
    #                         neighbor_mines += 1
    #             if 0 <= r + 1 < nrows:
    #                 if 0 <= c + 1 < ncolumns:
    #                     if board[r + 1][c + 1] == ".":
    #                         neighbor_mines += 1
    #             board[r][c] = neighbor_mines


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mines (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one mine
    is visible on the board after digging (i.e. game['visible'][mine_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    mine) and no mines are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]
    """

    nrows, ncolumns = game["dimensions"]
    # if game state is defeat or victory, return 0
    if game["state"] == "defeat" or game["state"] == "victory" or game["visible"][row][col]:
        return 0

    # reveal the cell
    game["visible"][row][col] = True
    revealed = 1

    # if the cell is a mine, the game should be changed to 'defeat'
    if game["board"][row][col] == ".":
        game["state"] = "defeat"
        return revealed

    # if the cell has no adjacent mines, then recursively reveal (dig up) its eight neighbors.
    if game["board"][row][col] == 0:
        for r in range(max(0, row - 1), min(nrows, row + 2)):
            for c in range(max(0, col - 1), min(ncolumns, col + 2)):
                if not game["visible"][r][c]:
                    additional_revealed = dig_2d(game, r, c)
                    if additional_revealed is not None:
                        revealed += additional_revealed

    # check for victory condition
    if all(game["visible"][r][c] or game["board"][r][c] == "." for r in range(nrows) for c in range(ncolumns)):
        game["state"] = "victory"

    return revealed

    # Original Code
    # if game["state"] == "defeat" or game["state"] == "victory":
    #     game["state"] = game["state"]  # keep the state the same
    #     return 0
    # if game["board"][row][col] == ".":
    #     game["visible"][row][col] = True
    #     game["state"] = "defeat"
    #     return 1
    # num_revealed_mines = 0
    # num_revealed_squares = 0
    #
    # for r in range(game["dimensions"][0]):
    #     for c in range(game["dimensions"][1]):
    #         if game["board"][r][c] == ".":
    #             if game["visible"][r][c] == True:
    #                 num_revealed_mines += 1
    #         elif game["visible"][r][c] == False:
    #             num_revealed_squares += 1
    # if num_revealed_mines != 0:
    #     # if num_revealed_mines is not equal to zero, set the game state to
    #     # defeat and return 0
    #     game["state"] = "defeat"
    #     return 0
    # if num_revealed_squares == 0:
    #     game["state"] = "victory"
    #     return 0

    # if game["visible"][row][col] != True:
    #     game["visible"][row][col] = True
    #     revealed = 1
    # else:
    #     return 0
    #
    # if game["board"][row][col] == 0:
    #     nrows, ncolumns = game["dimensions"]
    #     if 0 <= row - 1 < nrows:
    #         if 0 <= col - 1 < ncolumns:
    #             if game["board"][row - 1][col - 1] != ".":
    #                 if game["visible"][row - 1][col - 1] == False:
    #                     revealed += dig_2d(game, row - 1, col - 1)
    #     if 0 <= row < nrows:
    #         if 0 <= col - 1 < ncolumns:
    #             if game["board"][row][col - 1] != ".":
    #                 if game["visible"][row][col - 1] == False:
    #                     revealed += dig_2d(game, row, col - 1)
    #     if 0 <= row + 1 < nrows:
    #         if 0 <= col - 1 < ncolumns:
    #             if game["board"][row + 1][col - 1] != ".":
    #                 if game["visible"][row + 1][col - 1] == False:
    #                     revealed += dig_2d(game, row + 1, col - 1)
    #     if 0 <= row - 1 < nrows:
    #         if 0 <= col < ncolumns:
    #             if game["board"][row - 1][col] != ".":
    #                 if game["visible"][row - 1][col] == False:
    #                     revealed += dig_2d(game, row - 1, col)
    #     if 0 <= row < nrows:
    #         if 0 <= col < ncolumns:
    #             if game["board"][row][col] != ".":
    #                 if game["visible"][row][col] == False:
    #                     revealed += dig_2d(game, row, col)
    #     if 0 <= row + 1 < nrows:
    #         if 0 <= col < ncolumns:
    #             if game["board"][row + 1][col] != ".":
    #                 if game["visible"][row + 1][col] == False:
    #                     revealed += dig_2d(game, row + 1, col)
    #     if 0 <= row - 1 < nrows:
    #         if 0 <= col + 1 < ncolumns:
    #             if game["board"][row - 1][col + 1] != ".":
    #                 if game["visible"][row - 1][col + 1] == False:
    #                     revealed += dig_2d(game, row - 1, col + 1)
    #     if 0 <= row < nrows:
    #         if 0 <= col + 1 < ncolumns:
    #             if game["board"][row][col + 1] != ".":
    #                 if game["visible"][row][col + 1] == False:
    #                     revealed += dig_2d(game, row, col + 1)
    #     if 0 <= row + 1 < nrows:
    #         if 0 <= col + 1 < ncolumns:
    #             if game["board"][row + 1][col + 1] != ".":
    #                 if game["visible"][row + 1][col + 1] == False:
    #                     revealed += dig_2d(game, row + 1, col + 1)
    # num_revealed_mines = 0  # set number of mines to 0
    # num_revealed_squares = 0
    # for r in range(game["dimensions"][0]):
    #     # for each r,
    #     for c in range(game["dimensions"][1]):
    #         # for each c,
    #         if game["board"][r][c] == ".":
    #             if game["visible"][r][c] == True:
    #                 # if the game visible is True, and the board is '.',
    #                 # add 1 to mines revealed
    #                 num_revealed_mines += 1
    #         elif game["visible"][r][c] == False:
    #             num_revealed_squares += 1
    # bad_squares = num_revealed_mines + num_revealed_squares
    # if bad_squares > 0:
    #     game["state"] = "ongoing"
    #     return revealed
    # else:
    #     game["state"] = "victory"
    #     return revealed


def render_2d_locations(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored
    and all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)

    >>> game = {'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, True, False],
    ...                   [False, False, True, False]]}
    >>> render_2d_locations(game, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations(game, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """

    visible = game["visible"]
    board = game["board"]
    render = [["_" for _ in range(len(visible[0]))] for _ in range(len(visible))]

    for row in range(len(visible)):
        for col in range(len(visible[0])):
            if all_visible or visible[row][col]:
                if board[row][col] == ".":
                    render[row][col] = "."
                elif board[row][col] == 0:
                    render[row][col] = " "
                else:
                    render[row][col] = str(board[row][col])
            else:
                render[row][col] = "_"
    return render


def render_2d_board(game, all_visible=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'visible':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    string_game = ""
    visible = game["visible"]
    board = game["board"]

    for row in range(len(visible)):
        if row > 0:
            string_game += "\n"
        for col in range(len(visible[0])):
            # when all_visible is True, add the character to the string, if Flase, add "_"
            if not all_visible and not visible[row][col]:
                string_game += "_"
                continue
            # when all_visible is Flase, add every character to the string
            if board[row][col] == 0:
                string_game += " "
            else:
                string_game += str(board[row][col])
    return string_game


# N-D IMPLEMENTATION


def new_game_nd(dimensions, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Args:
       dimensions (tuple): Dimensions of the board
       mines (list): mine locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """

    def nested_list(value, dimensions, level = 0):
        """
        helper function that creates a new N-d array, each value in the array is the given value.
        """
        if level == len(dimensions)- 1:
            return [value for _ in range(dimensions[level])]
        return [nested_list(value, dimensions, level + 1) for _ in range(dimensions[level])]

    # initialize the board with 0
    board = nested_list(0, dimensions)

    def product(*args):
        pools = [tuple(pool) for pool in args]  # Convert input to tuple to ensure immutability
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)

    # place mines and increment numbers around mines
    for mine in mines:
        # Place mine
        current = board
        for dim in mine[:-1]:
            current = current[dim]
        current[mine[-1]] = "."

        # increment numbers around the mine
        for delta in product(*[range(-1, 2) for _ in dimensions]):
            if all(d == 0 for d in delta):  # Skip the mine itself
                continue
            neighbor = tuple(m + d for m, d in zip(mine, delta))
            if all(0 <= n < dimensions[i] for i, n in enumerate(neighbor)):
                current = board
                for dim in neighbor[:-1]:
                    current = current[dim]
                if isinstance(current[neighbor[-1]], int):
                    current[neighbor[-1]] += 1

    # initialize visibility
    visible = nested_list(False, dimensions)

    return {
        "dimensions": dimensions,
        "board": board,
        "visible": visible,
        "state": "ongoing",
    }


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    mine.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one mine is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a mine) and no mines are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: defeat
    visible:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    # helper function to generate all possible combinations for the product
    def product(*args):
        # Generate all combinations of indices around a square
        pools = [tuple(pool) for pool in args]
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)

    # helper function to check if a square is a mine
    def is_mine(board, coords):
        current = board
        for coord in coords[:-1]:
            current = current[coord]
        return current[coords[-1]] == "."

    # helper function to reveal squares
    def reveal(game, coords):
        # Recursive function to reveal squares
        nonlocal revealed_count
        current = game["visible"]
        for coord in coords[:-1]:
            current = current[coord]
        if not current[coords[-1]]:
            current[coords[-1]] = True
            revealed_count += 1
            # Only continue recursion if the square has no adjacent mines
            if game["board"][coords[0]][coords[1]][coords[2]] == 0:
                for delta in product(*[range(-1, 2) for _ in game["dimensions"]]):
                    if all(d == 0 for d in delta):  # Skip the current square itself
                        continue
                    neighbor = tuple(c + d for c, d in zip(coords, delta))
                    if all(0 <= n < game["dimensions"][i] for i, n in enumerate(neighbor)):
                        reveal(game, neighbor)

    # check if the game is ongoing
    if game["state"] != "ongoing":
        return 0

    revealed_count = 0
    if is_mine(game["board"], coordinates):
        game["visible"][coordinates[0]][coordinates[1]][coordinates[2]] = True
        game["state"] = "defeat"
        revealed_count = 1
    else:
        reveal(game, coordinates)
        # check for victory
    if all(all(all(cell == '.' or vis for cell, vis in zip(row, vis_row))
            for row, vis_row in zip(board_layer, vis_layer))
        for board_layer, vis_layer in zip(game['board'], game['visible'])):
        game['state'] = 'victory'

    return revealed_count


def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  The game['visible'] array indicates which squares should be
    visible.  If all_visible is True (the default is False), the game['visible']
    array is ignored and all cells are shown.

    Args:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    # helper function to create an N-dimensional nested list
    def nested_list(dimensions, value, level=0):
        if level == len(dimensions) - 1:
            return [value for _ in range(dimensions[level])]
        return [nested_list(dimensions, value, level + 1) for _ in range(dimensions[level])]

    # helper function to get the value at the given coordinates
    def get_value(game, coords):
        current = game["board"]
        for coord in coords[:-1]:
            current = current[coord]
        return current[coords[-1]]

    # helper function to check if a square is visible
    def is_visible(game, coords):
        current = game["visible"]
        for coord in coords[:-1]:
            current = current[coord]
        return current[coords[-1]]

    # helper function to render the board
    def render_board(game, dimensions, level=0, coords=[]):
        if level == len(dimensions) - 1:
            return [render_square(game, coords + [i]) for i in range(dimensions[level])]
        return [render_board(game, dimensions, level + 1, coords + [i]) for i in range(dimensions[level])]

    # helper function to render a single square
    def render_square(game, coords):
        if all_visible or is_visible(game, coords):
            value = get_value(game, coords)
            return "." if value == "." else " " if value == 0 else str(value)
        else:
            return "_"

    # render the board
    return render_board(game, game["dimensions"])


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
    
    # test for dig_nd(game, coordinates):
    g = {'dimensions': (2, 4, 2),
        'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        'visible': [[[False, False], [False, True], [False, False],
                    [False, False]],
                    [[False, False], [False, False], [False, False],
                    [False, False]]],
        'state': 'ongoing'}
    print(dig_nd(g, (0, 3, 0)))  # Should reveal 8 squares and game state remains 'ongoing'
    print(dig_nd(g, (0, 0, 1)))  # Should reveal 1 square and game state changes to 'defeat'