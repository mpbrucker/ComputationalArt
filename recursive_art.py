""" TODO: Put your header comment here """

import random
from PIL import Image
from math import cos, sin, pi
from random import randint


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the randrom function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    rand_funcs = ['prod', 'avg', 'sin_pi', 'cos_pi', 'cube', 'square', 'x', 'y']
    if min_depth > 0:
        max_val = len(rand_funcs)-3
    else:
        max_val = len(rand_funcs)-1

    if max_depth > 0:
        cur_func = rand_funcs[randint(0, max_val)]
    else:
        cur_func = rand_funcs[randint(len(rand_funcs)-2,len(rand_funcs)-1)]
    if cur_func in ['x', 'y']:
        return [cur_func]
    else:
        # if cur_func in ['sin_pi','cos_pi']:
        #     return [cur_func, build_random_function(min_depth-1,max_depth-1)]
        # else:
        return [cur_func, build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    # print(f)
    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 'prod':
        return evaluate_random_function(f[1], x, y)*evaluate_random_function(f[2], x, y)
    elif f[0] == 'avg':
        return 0.5*(evaluate_random_function(f[1], x, y)+evaluate_random_function(f[2], x, y))
    elif f[0] == 'cos_pi':
        return cos(pi*evaluate_random_function(f[1], x, y))
    elif f[0] == 'sin_pi':
        return sin(pi*evaluate_random_function(f[1], x, y))
    elif f[0] == 'cube':
        return evaluate_random_function(f[1], x, y)**3
    elif f[0] == 'square':
        return evaluate_random_function(f[1], x, y)**2

    # case = {
    #     'x': x,
    #     'y': y,
    #     'prod': evaluate_random_function(f[1],x,y)*evaluate_random_function(f[2],x,y),
    #     'avg': 0.5*(evaluate_random_function(f[1], x, y)+evaluate_random_function(f[2],x,y)),
    #     'cos_pi': cos(pi*evaluate_random_function(f[1],x,y)),
    #     'sin_pi': sin(pi*evaluate_random_function(f[1],x,y)),
    # }
    # if f[0] == 'x' or f[0] == 'y':
    #     print('test')
    # return case[f[0]]


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # TODO: implement this
    return (val-input_interval_start)*((output_interval_end-output_interval_start)/(input_interval_end-input_interval_start)) + output_interval_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    # doctest.testmod()
    # rand_func = (build_random_function(5,7))


    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
