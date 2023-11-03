"""
6.101 Lab 1:
Image Processing
"""

#!/usr/bin/env python3

import math

from PIL import Image

# NO ADDITIONAL IMPORTS ALLOWED!


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


def inverted(image):
    return apply_per_pixel(image, lambda color: 255-color)


# HELPER FUNCTIONS

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


# N-by-N kernel, identical values that sum to 1
def blurred_kernel(n):
    kernel = [[1/(n*n) for _ in range(n)] for _ in range(n)]

    return kernel


# FILTERS

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


def sharpened(image, n):
    """
    Return a new image representing the result of applying an unsharpen mask to the given input image.

    S = 2 * I - B

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
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


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
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
    by the "mode" parameter.
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
    # img = load_greyscale_image("test_images/bluegill.png")
    # result = inverted(img)
    # save_greyscale_image(result,"test_results/inverted.png", mode="PNG")
    
    
    # CORRELATION
    # img = load_greyscale_image("test_images/pigbird.png")
    # kernel = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # ]
    # result_zero = correlate(img, kernel, "zero")
    # save_greyscale_image(result_zero,"test_results/correlated_zero.png", mode="PNG")
    
    # result_wrap = correlate(img, kernel, "wrap")
    # save_greyscale_image(result_wrap,"test_results/correlated_wrap.png", mode="PNG")

    # result_extend = correlate(img, kernel, "extend")
    # save_greyscale_image(result_extend,"test_results/correlated_extend.png", mode="PNG")
    
    
    # BLURRING
    # img = load_greyscale_image("test_images/cat.png")
    
    # result_blurred = blurred(img, 13)
    # save_greyscale_image(result_blurred,"test_results/correlated_blurred.png", mode="PNG")
    
    # img = load_greyscale_image("test_images/centered_pixel.png")
    # result_blurred = blurred(img, 2)
    
    
    #SHARPENING
    # img = load_greyscale_image("test_images/python.png")
    
    # result_sharpeded = sharpened(img, 11)
    # save_greyscale_image(result_sharpeded,"test_results/correlated_sharpened.png", mode="PNG")  
    
    
    #EDGE
    img = load_greyscale_image("test_images/centered_pixel.png")
    
    result_edge = edges(img)
    print(result_edge)
    save_greyscale_image(result_edge,"test_results/correlated_edge.png", mode="PNG")  
          
    # img = load_greyscale_image("test_images/construct.png")
    
    # result_edge = edges(img)
    # save_greyscale_image(result_edge,"test_results/correlated_edge_construct.png", mode="PNG")  