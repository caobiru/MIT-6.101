"""
6.1010 Lab 4: 
Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}

def deep_copy_game(game):
    game_copy = {
        "height": game["height"],
        "width": game["width"],
        "player": game["player"],
        "computer": set(game["computer"]),
        "target": set(game["target"]),
        "wall": set(game["wall"])
    }
    return game_copy


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    
    player_pos = None
    computer_pos = set()
    target_pos = set()
    wall_pos = set()
    
    for row in range(len(level_description)):
        for col in range(len(level_description[0])):
            for id in level_description[row][col]:
                if id == "player": 
                    player_pos = (row, col)
                elif id == "computer":
                    computer_pos.add((row, col))
                elif id == "target":
                    target_pos.add((row, col))
                elif id == "wall":
                    wall_pos.add((row, col))
    
    new_rep = {
        "height":len(level_description),
        "width": len(level_description[0]),
        "player": player_pos,
        "computer": computer_pos,
        "target": target_pos,
        "wall": wall_pos,
    }
    
    return new_rep
    

def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """

    if game["computer"] and game["target"] and game["target"] == game["computer"]:
        return True
    else:
        return False
        

def move(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game= 
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    # check if the player can move
    # if the player can move, update its position and return a new game representation 
    game_copy = deep_copy_game(game)
    
    if is_movable(game_copy, direction):
        player_pos_updated = update_pos(game_copy["player"], direction)
        # check if the player moved a computer
        if player_pos_updated in game_copy["computer"]:
            # remove the old position and add the new position
            game_copy["computer"].remove(player_pos_updated)
            game_copy["computer"].add(update_pos(player_pos_updated, direction))
            
        game_updated = {
            "height": game_copy["height"],
            "width": game_copy["width"],
            "player": player_pos_updated,
            "computer": game_copy["computer"],
            "target": game_copy["target"],
            "wall": game_copy["wall"]
        }
        
        return game_updated
    
    # if the player can't move, return the original game representation
    else: 
        return game_copy     
    

def is_movable(game, direction):
    """
    Several situations that the player can't move:
    Situation 1: player is moving to a wall's position
    Situation 2: there are two neighboring computers and the player is moving to one of them's position
    Situation 3: the player is moving a computer to a wall
    """
    computer_y, computer_x = game["player"]
    dy, dx = direction
    height = game["height"]
    width = game["width"]
    
    # check Situation 1 and if player is within the boundary of the game
    if 0 < computer_x + dx < width - 1 and  0 < computer_y + dy < height - 1 and (computer_y + dy, computer_x + dx) not in game["wall"]:
        # check Situation 2 and Situation 3
        if (computer_y + dy, computer_x + dx) in game["computer"] and ((computer_y + dy + dy, computer_x + dx + dx) in game["computer"] or (computer_y + dy + dy, computer_x + dx + dx) in game["wall"] or (computer_y + dy + dy >= height - 1 or computer_y + dy + dy <= 0 or computer_x + dx + dx >= width - 1 or computer_x + dx + dx <= 0)):
            return False 
        else:
            return True
    else:
        return False       
    

def update_pos(player_pos, direction):
    """
    Given player's position and direction in tuples, return the updated player's position
    """
    return (player_pos[0] + direction[0], player_pos[1] + direction[1])            


def step_game(game, direction):
    global direction_vector
    return move(game, direction_vector[direction])
    
    
def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    canonical = [[[]for _ in range(game["width"])]for _ in range(game["height"])]

    player_x, player_y = game["player"]
    canonical[player_x][player_y].append('player')    
    for (row, col) in game["computer"]:
        canonical[row][col].append('computer')
    for (row, col) in game["target"]:
        canonical[row][col].append('target')    
    for (row, col) in game["wall"]:
        canonical[row][col].append('wall')    
        
    return canonical


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    # initialize a queue with the starting game state and an empty list of moves
    queue = [(game, [])]
    # initialize a set to keep track of all the visited states
    visited = set()
    
    while queue:
        current_game, moves = queue.pop(0)
        if(victory_check(current_game)):
            print(moves)
            return moves
        
        for direction in ["up", "down", "left", "right"]:
            # make a copy of the current state and make a move
            new_game = step_game(current_game.copy(), direction)
            # covert the game state to a frozenset so it can be added to a set
            new_game_state = frozenset((k, frozenset(v)) if isinstance(v, set) else (k, v) for k, v in new_game.items())
            
            # if the resulting state not in the visited set
            if new_game_state not in visited:
                # add it to the queue and the visited set
                queue.append((new_game, moves + [direction]))
                visited.add(new_game_state)
    
    # if the queue is empty and no victory state, then the puzzle can't be solved  
    return None


if __name__ == "__main__":
    # new = new_game("puzzles/m1_008.json")
    # solution = solve_puzzle(new)
    # print(solution)
    pass
