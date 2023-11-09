"""
6.101 Lab 2:
Image Processing 2
"""

#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image



# FROM GREY TO COLOR FILTER-----------------------------------------------------------------------------------------------------#

def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def color_filter(image):
        # Split the given color image into its three components  
        three_channel = split_channel(image)
        
        three_channel_filtered = []
        
        for i in range(3):
            three_channel_filtered.append(filt(three_channel[i]))
            
        # Combine three filtered channels
        return combine_channel(three_channel_filtered)
    
    # Returns the funciton which is a color version of that filter
    return color_filter
    
    
# Split the given color image into its three components, the three_channel stores single channels as a list   
def split_channel(image):

    three_channel = []

    for i in range(3):
        
        single_channel = {
            "height": image["height"],
            "width": image["width"],
            "pixels": [0,] * (image["height"] * image["width"])
        }

        #print(image["pixels"])   
        for row in range(image["height"]):
            for col in range(image["width"]):
                set_pixel(single_channel, row, col, image["pixels"][row * image["width"] + col][i])
                    
        three_channel.append(single_channel)
                    
    return three_channel    


# recombining three greyscale images into a single new color image.
def combine_channel(three_channel):
    combined_image = {
        "height": three_channel[0]["height"],
        "width": three_channel[0]["width"],
        "pixels": [0] * (three_channel[0]["height"] * three_channel[0]["width"])
    }
    
    for row in range(three_channel[0]["height"]):
        for col in range(three_channel[0]["width"]):
            color = (get_pixel(three_channel[0], row, col, "extend"), get_pixel(three_channel[1], row, col, "extend"), get_pixel(three_channel[2], row, col, "extend"))
            set_pixel(combined_image, row, col, color)
            
    return combined_image



# VARIOUS FILTERS-----------------------------------------------------------------------------------------------------#
# INVERSION-----------------------------------------------------------------------------------------------------------#

# The inversion filter from Lab1
def inverted(image):
    return apply_per_pixel(image, lambda color: 255-color)
            
                        

# SHARPEN-------------------------------------------------------------------------------------------------------------#

# The sharpen filter from Lab1
def sharpened(image, n):
    """
    Return a new image representing the result of applying an unsharpen mask to the given input image.

    S = 2 * I - B
    """
    # first, create a representation for the appropriate n-by-n kernel
    kernel = blurred_kernel(n)
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0] * (image["width"] * image["height"])
    }
    
    # then compute the correlation of the input image with that kernel
    blurred = correlate(image, kernel, "extend")

    for row in range(image["height"]):
        for col in range(image["width"]):
            color = get_pixel(image, row, col, "extend") * 2 - get_pixel(blurred, row, col, "extend")    
            set_pixel(result, row, col, color)
    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    round_and_clip_image(result)
    
    return result
    
    
def make_sharpen_filter(kernel_size):
    
    def sharpen_filter(image):
        
        sharpened_img = sharpened(image, kernel_size)
        
        return sharpened_img
    
    return sharpen_filter



# BLUR---------------------------------------------------------------------------------------------------------------#

# The blur filter from Lab1
def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    kernel = blurred_kernel(kernel_size)

    # then compute the correlation of the input image with that kernel
    result = correlate(image, kernel, "extend")
    
    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    round_and_clip_image(result)
    
    return result


def make_blur_filter(kernel_size):
    
    def blur_filter(image):
        
        blurred_img = blurred(image, kernel_size)
        
        return blurred_img
    
    return blur_filter
    


# FILTER CASCADE-----------------------------------------------------------------------------------------------------#

def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def make_filters(image):
        filtered_img = image
        for filter in filters:
            filtered_img = filter(filtered_img)
        
        return filtered_img
    
    return make_filters
        
        
        
#HELPER FUNCTIONS FROM LAB1--------------------------------------------------------------------------------------------------#

# N-by-N kernel, identical values that sum to 1
def blurred_kernel(n):
    kernel = [[1/(n*n) for _ in range(n)] for _ in range(n)]

    return kernel


# get the color in specific row and col
def get_pixel(image, row, col, edge):
    # zero edge effect
    if edge == "zero":
        if row < 0 or row >= image["height"] or col < 0 or col >= image["width"]:
            pixel = 0
        else:
            pixel = image["pixels"][row * image["width"] + col]    
    
    # extend edge effect      
    elif edge == "extend":
        if row < 0:
            row = 0
        elif row >= image["height"]:
            row = image["height"] - 1
        
        if col < 0:
            col = 0
        elif col >= image["width"]:
            col = image["width"] - 1;
        
        pixel = image["pixels"][row * image["width"] + col]     
          
    # wrap edge effect              
    elif edge == "wrap":
        if row < 0 or row >= image["height"]:
            row = row % image["height"]         
            
        if col < 0 or col >= image["width"]:
            col = col % image["width"]
        
        pixel = image["pixels"][row * image["width"] + col]        

    return pixel


# change the color in specific row and col
def set_pixel(image, row, col, color):
    image["pixels"][row * image["width"] + col] = color
    
    
def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0] * (image["width"] * image["height"]),
    }
    
    for row in range(image["height"]):
        for col in range(image["width"]):
            color = get_pixel(image, row, col, "extend")
            new_color = func(color)
            set_pixel(result, row, col, new_color)
            
    return result  


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    for row in range(image["height"]):
        
        for col in range(image["width"]):
            color = get_pixel(image, row, col, "extend")
               
            if color > 255:
                set_pixel(image, row, col, 255)
            elif color < 0:
                set_pixel(image, row, col, 0)
            else :
                set_pixel(image, row, col, round(color)) 
                
    return image    


def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    
    kernels will always be square 
    every kernel will have an odd number of rows and columns.
    
    for example: the average kernel:
    [
        [0.0, 0.2, 0.0],
        [0.2, 0.2, 0.2],
        [0.0, 0.2, 0.0],
    ] 
    """

    if boundary_behavior != "zero" and  boundary_behavior != "extend" and boundary_behavior != "wrap":
        return None
    
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0] * (image["width"] * image["height"]),
    }
    
    kernel_size = len(kernel)
    half_size = int((kernel_size - 1) / 2)
    
    for row in range(image["height"]):
        for col in range(image["width"]):
            for krow in range(-half_size, half_size + 1):
                    for kcol in range(-half_size, half_size + 1):
                        result["pixels"][row * image["width"] + col] += get_pixel(image, row + krow, col + kcol, boundary_behavior) * kernel[krow + half_size][kcol + half_size]
    
    return result


def edges(image):
    """
    a Sobel operator, which is useful for detecting edges in images.
    
    K1:
    -1 -2 -1
    0  0  0
    1  2  1 
    
    K2:
    -1 0 1
    -2 0 2
    -1 0 1    
    
    O = round(sqrt(O1 * O1 + O2 * O2))
    """

    kernel1 = [
                [-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1]
            ]
    
    kernel2 = [
                [-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1],   
            ]
    
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0] * (image["width"] * image["height"])
    }
    
    # then compute the correlations of the input image with kernels
    edge1 = correlate(image, kernel1, "extend")
    edge2 = correlate(image, kernel2, "extend")
    
    for row in range(image["height"]):
        for col in range(image["width"]):
            pixel1 = get_pixel(edge1, row, col, "extend")
            pixel2 = get_pixel(edge2, row, col, "extend")        
            color = math.sqrt(pixel1 * pixel1 + pixel2 * pixel2)
            set_pixel(result, row, col, color)
            
    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    round_and_clip_image(result)
    
    return result



# SEAM CARVING----------------------------------------------------------------------------------------------------------#

# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image.
    """
    
    image_col_removed = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0] * (image["height"] * image["width"])
    }
    
    for row in range(image["height"]):
        for col in range(image["width"]):
            set_pixel(image_col_removed, row, col, get_pixel(image, row, col, "extend"))
    
    for col in range(ncols):
       image_col_removed = single_seam_carving(image_col_removed)
       print(col)

    return image_col_removed


# Optional Helper Functions for Seam Carving

def single_seam_carving(image):
    result = image_without_seam(image, minimum_energy_seam(cumulative_energy_map(compute_energy(greyscale_image_from_color_image(image)))))
    return result


def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    greyscale_image = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0] * (image["height"] * image["width"])
    }
    
    # calculating the greyscale of a color pixel:
    # v = round(0.299 * r + 0.587 * g + 0.114 * b)
    for row in range(image["height"]):
        for col in range(image["width"]):
            value = round(image["pixels"][row * image["width"] + col][0] * 0.299 + image["pixels"][row * image["width"] + col][1] * 0.587 + image["pixels"][row * image["width"] + col][2] * 0.114)
            set_pixel(greyscale_image, row, col, value )

    return greyscale_image


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    energy_map = {
        "height": energy["height"],
        "width": energy["width"],
        "pixels": [0] * (energy["height"] * energy["width"])
    }
    
    # set the top row equal to the top row from the energy map
    for first_col in range(energy["width"]):
        set_pixel(energy_map, 0, first_col, energy["pixels"][first_col])
        
    # the value of that location in the energy map, added to the
    # minimum of the cumulative energies from the "adjacent" pixels in the row above
    for row in range(1, energy["height"]):
        for col in range(energy["width"]):

            if col == 0:
                left_pixel = float('inf')
                mid_pixel = get_pixel(energy_map, row - 1, col, "extend")
                right_pixel = get_pixel(energy_map, row - 1, col + 1, "extend")
                
            elif col == (energy["width"] - 1):
                left_pixel = get_pixel(energy_map, row - 1, col - 1, "extend")
                mid_pixel = get_pixel(energy_map, row - 1, col, "extend")         
                right_pixel = float('inf')
                                
            else: 
                left_pixel = get_pixel(energy_map, row - 1, col - 1, "extend")
                mid_pixel = get_pixel(energy_map, row - 1, col, "extend")
                right_pixel = get_pixel(energy_map, row - 1, col + 1, "extend")
                            
            min_value = min(left_pixel, mid_pixel, right_pixel)
            cur_value = get_pixel(energy, row, col, "extend")
     
            set_pixel(energy_map, row, col, min_value + cur_value)

    return energy_map


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    seam = []

    min_value = get_pixel(cem, cem["height"] - 1, 0, "extend")

    min_col = 0
    
    # get the minimum value pixel in the bottom row
    for col in range(1, cem["width"]):
        if (get_pixel(cem, cem["height"] - 1, col, "extend") < min_value):
            min_value = get_pixel(cem, cem["height"] - 1, col, "extend")
            min_col = col

    seam.append((cem["height"] - 1) * cem["width"] + min_col)
                
    # get the minimum value pixel of the rest rows            
    for row in range(cem["height"] - 2, -1, -1):

        if min_col == 0:
            if get_pixel(cem, row, min_col, "extend") > get_pixel(cem, row, min_col + 1, "extend"):
                min_col += 1
                
        elif min_col == cem["width"] - 1: 
            if get_pixel(cem, row, min_col - 1, "extend") <= get_pixel(cem, row, min_col, "extend"):
                min_col -= 1
                
        else:
            left_pixel =  get_pixel(cem, row, min_col - 1, "extend")
            mid_pixel = get_pixel(cem, row, min_col, "extend")
            right_pixel = get_pixel(cem, row, min_col + 1, "extend")
            
            min_value = min(left_pixel, mid_pixel, right_pixel)
            
            # Ties should always be broken by preferring the left-most of the tied columns.
            if left_pixel == min_value:
                min_col -= 1
                
            elif mid_pixel == min_value:
                pass
                
            elif right_pixel == min_value:
                min_col += 1
            
        seam.append(row * cem["width"] + min_col)
        
    # reverse the seam list      
    return seam[::-1]
           
    
def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    seam.sort()
    
    image_removed = {
        "height": image["height"],
        "width": image["width"] - 1,
        "pixels": [0] * (image["height"] * (image["width"] - 1))
    }
    
    seam_index = 0
    image_removed_index = 0
        
    for image_index in range(len(image["pixels"])):
        if seam_index < len(seam) and image_index == seam[seam_index]:
            seam_index += 1 
        else:
            image_removed["pixels"][image_removed_index] = image["pixels"][image_index]
            image_removed_index += 1
                
    return image_removed
    
    
def custom_feature():
     pass
 
 
 
# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES


def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    
    # INVERSION
    # img = load_color_image("test_images/cat.png")
    # color_inverted = color_filter_from_greyscale_filter(inverted)
    # result = color_inverted(img)
    # save_color_image(result,"test_results/cat_inverted.png", mode="PNG")  
    
    # BLUR
    # img = load_color_image("test_images/python.png")
    # result = color_filter_from_greyscale_filter(make_blur_filter(9))(img)
    # save_color_image(result,"test_results/python_blurred.png", mode="PNG") 

    # SHARPEN
    # img = load_color_image("test_images/sparrowchick.png")
    # result = color_filter_from_greyscale_filter(make_sharpen_filter(7))(img)
    # save_color_image(result,"test_results/sparrowchick_sharpened.png", mode="PNG") 
    
    # CASCADE
    # img = load_color_image("test_images/frog.png")
    # filter1 = color_filter_from_greyscale_filter(edges)
    # filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))  
    
    # filt = filter_cascade([filter1, filter1, filter2, filter1])
    # result = filt(img)
    # save_color_image(result,"test_results/frog_cascaded.png", mode="PNG") 
    
    # SEAM CARVING
    img = load_color_image("test_images/twocats.png")
    result = seam_carving(img, 100)
    save_color_image(result,"test_results/twocats_seamcarved.png", mode="PNG")     
