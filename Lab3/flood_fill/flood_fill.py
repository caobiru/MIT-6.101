def flood_fill(image, location, new_color):
    """
    Given an image, replace the same-colored region around a given location
    with a given color.  Returns None but mutates the original image to
    reflect the change.

    Parameters:
      * image: the image to operate on
      * location: an (row, col) tuple representing the starting location of the
                  flood-fill process
      * new_color: the replacement color, as an (r, g, b) tuple where all values
                   are between 0 and 255, inclusive
    """
    print(f"You clicked at row {location[0]} col {location[1]}")
    
    # store the original color of the click
    original_color = get_pixel(image, *location)
    
    # helper function to get the four neighbors of a given row, col coordinate
    def get_neighbors(cell):
        row, col = cell
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        valid_neighbors = [(row, col) 
                           for row, col in neighbors 
                           if 0 <= row < get_height(image) and 0 <= col < get_width(image)]
        return valid_neighbors
    
    # agenda: all the colors wee need to color in 
    to_color = [location]
    
    # all pixels ever added to the agenda
    visited = {location}
    
    # while there are still cells to color in
    while to_color:
        # remove a single tuple from the to_color list and call it this_cell
        this_cell = to_color.pop(0)
        
        #replace this cell with the given color
        set_pixel(image, *this_cell, new_color)
        
        # add each neighbor to to_color
        # to_color += [neighbor 
        #                 for neighbor in get_neighbors(this_cell) 
        #                     if neighbor not in visited 
        #                         and get_pixel(image, *neighbor) == original_color]
        
        for neighbor in get_neighbors(this_cell):
            if(neighbor not in visited and get_pixel(image, *neighbor) == original_color):
                to_color.append(neighbor)
                visited.add(neighbor)
            

def find_path(image, start_location, goal_color):
    """
    Finding path in a maze
    """
    safe_color = get_pixel(image, *start_location)
    
    def get_neighbors(cell):
        row, col = cell
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        valid_neighbors = [(row, col) 
                           for row, col in neighbors 
                           if 0 <= row < get_height(image) and 0 <= col < get_width(image)]
        return valid_neighbors

    # agenda: path we know about but haven't tried to extend
    possible_path = [(start_location,)]
    
    # all locations to which we've already found a path, i.e., all locations that have ever been the last location in a path
    visited = {start_location}
    
    # while there are still path in the agenda
    while possible_path:
        
        # remove one path from the agenda
        this_path = possible_path.pop(0)
        
        # get the last location in the path
        end_cell = this_path[-1]
        
        # get the last location's neighbors
        end_neighbors = get_neighbors(end_cell)
        
        # for each of the neighbor of the last location in the path:
        for neighbor in end_neighbors:
            if neighbor in visited:
                pass
            else:            
                if  get_pixel(image, *neighbor) == goal_color:
                    path =  list(this_path) + [neighbor]
                    # draw the path
                    for location in path:
                        set_pixel(image, *location, (0,255,0))
                    return path
                elif get_pixel(image, *neighbor) == safe_color:
                    visited.add(neighbor)
                    new_path = list(this_path) + [neighbor]
                    possible_path.append(new_path)

##### IMAGE REPRESENTATION WITH SIMILAR ABSTRACTIONS TO LAB 1 AND 2


def get_width(image):
    return image.get_width() // SCALE


def get_height(image):
    return image.get_height() // SCALE


def get_pixel(image, row, col):
    color = image.get_at((col * SCALE, row * SCALE))
    return (color.r, color.g, color.b)


def set_pixel(image, row, col, color):
    loc = row * SCALE, col * SCALE
    c = pygame.Color(*color)
    for i in range(SCALE):
        for j in range(SCALE):
            image.set_at((loc[1] + i, loc[0] + j), c)
    ## comment out the two lines below to avoid redrawing the image every time
    ## we set a pixel
    # screen.blit(image, (0, 0))
    # pygame.display.flip()


##### USER INTERFACE CODE
##### DISPLAY AN IMAGE AND CALL flood_fill WHEN THE IMAGE IS CLICKED

import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from pygame.locals import *

COLORS = {
    pygame.K_r: (255, 0, 0),
    pygame.K_w: (255, 255, 255),
    pygame.K_k: (0, 0, 0),
    pygame.K_g: (0, 255, 0),
    pygame.K_b: (0, 0, 255),
    pygame.K_c: (0, 255, 255),
    pygame.K_y: (255, 230, 0),
    pygame.K_p: (179, 0, 199),
    pygame.K_o: (255, 77, 0),
    pygame.K_n: (66, 52, 0),
    pygame.K_e: (152, 152, 152),
}

COLOR_NAMES = {
    pygame.K_r: "red",
    pygame.K_w: "white",
    pygame.K_k: "black",
    pygame.K_g: "green",
    pygame.K_b: "blue",
    pygame.K_c: "cyan",
    pygame.K_y: "yellow",
    pygame.K_p: "purple",
    pygame.K_o: "orange",
    pygame.K_n: "brown",
    pygame.K_e: "grey",
}

SCALE = 7
#IMAGE = "flood_input.png"

IMAGE = "large_maze.png"
pygame.init()
image = pygame.image.load(IMAGE)
dims = (image.get_width() * SCALE, image.get_height() * SCALE)
screen = pygame.display.set_mode(dims)
image = pygame.transform.scale(image, dims)
screen.blit(image, (0, 0))
pygame.display.flip()
initial_color = pygame.K_p
cur_color = COLORS[initial_color]
print("current color:", COLOR_NAMES[initial_color])
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key in COLORS:
                cur_color = COLORS[event.key]
                print("current color:", COLOR_NAMES[event.key])
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #flood_fill(image, (event.pos[1] // SCALE, event.pos[0] // SCALE), cur_color)
            find_path(image, (event.pos[1] // SCALE, event.pos[0] // SCALE), (0,255,0))
            screen.blit(image, (0, 0))
            pygame.display.flip()
