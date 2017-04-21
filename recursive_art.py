"""
Generates randomized art based on recursive functions.  Separate functions for the R, G,
and B pixel values vary based on the x position, y position, and frame of the pixel,
also allowing making of frames of a movie.

Uses the default functions plus two extra: x squared and x cubed.

@author: Matt Brucker

"""
import random
from PIL import Image
from math import cos, sin, pi
from random import randint
import pygame
import alsaaudio
import audioop
from os import listdir


def build_random_function(min_depth, max_depth, is_movie=False):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    # Returns either x, y, or t
    # Important to note: all randomness must not be in the lambas
    # Otherwise they will generate a different function for each pixel
    # Also, if is_movie is false, makes sure nothing is a function of t
    if is_movie:
        return_val = [lambda x, y, t: x, lambda x, y, t: y, lambda x, y, t: t][randint(0, 2)]
        # Build all functions with movie option enabled, so t is a parameter
        rand_funcs = [lambda x, y, t: x*y*t, lambda x, y, t: (x+y+t)/3, lambda x, y, t: sin(pi*x),
                      lambda x, y, t: cos(pi*x), lambda x, y, t: x**3, lambda x, y, t: x**2]
    else:
        return_val = [lambda x, y: x, lambda x, y: y][randint(0, 1)]
        # Build all functions with movie option disabled
        rand_funcs = [lambda x, y: x*y, lambda x, y: .5*(x+y), lambda x, y: sin(pi*x),
                      lambda x, y: cos(pi*x), lambda x, y: x**3, lambda x, y: x**2]

    # We have reached the max limit of recursion, stop
    if max_depth <= 0:
        return return_val  # Return either x, y, or t
    else:
        # If we've reached the minimum level of recursion, have a 50% chance to end there
        if min_depth <= 0 and randint(0, 1):
            return return_val
        cur_func = rand_funcs[randint(0, len(rand_funcs)-1)]  # Get random function
        # IMPORTANT: these must be evaluated outside of a lambda
        # otherwise a new function is generated with each labmda call (which is bad)
        if is_movie:
            # If we're making a movie, we need three functions
            func1 = build_random_function(min_depth-1, max_depth-1, is_movie=True)
            func2 = build_random_function(min_depth-1, max_depth-1, is_movie=True)
            func3 = build_random_function(min_depth-1, max_depth-1, is_movie=True)
            return lambda x, y, t: cur_func(func1(x, y, t), func2(x, y, t), func3(x, y, t))  # Combine the functions
        else:
            # We're not making a movie, so we only need two functions, x and y
            func1 = build_random_function(min_depth-1, max_depth-1)
            func2 = build_random_function(min_depth-1, max_depth-1)
            return lambda x, y: cur_func(func1(x, y), func2(x, y))


def remap_interval(val,
                   in_start,
                   in_end,
                   out_start,
                   out_end):
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
    # Returns the value remapped from the input interval to the output interval
    return (val-in_start)*((out_end-out_start)/(in_end-in_start)) + out_start


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


def generate_art(filename, x_size=350, y_size=350, frames=1):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # If the number of frames is greater than 1, this will be true, and build_random_function will make movie frames
    is_movie = (frames-1) > 0

    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(3, 5, is_movie)
    green_function = build_random_function(3, 5, is_movie)
    blue_function = build_random_function(3, 5, is_movie)

    print("Built functions.")
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    # Loop across all frames (allows for creation of a movie if frames > 1)
    for frame in range(0, frames):
        t = remap_interval(frame, 0, frames, -1, 1)
        # Loop across every pixel in the frame
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                if is_movie:
                    pixels[i, j] = (
                            # Evaluates our random lambdas for each pixel value
                            color_map(red_function(x, y, t)),
                            color_map(green_function(x, y, t)),
                            color_map(blue_function(x, y, t))
                            )
                else:
                    pixels[i, j] = (
                            # Evaluates our random lambdas for each pixel value
                            color_map(red_function(x, y)),
                            color_map(green_function(x, y)),
                            color_map(blue_function(x, y))
                            )
        im.save(filename + str(frame) + ".png")
        print("Frame" + str(frame) + " done.")


def get_img_surfaces(direc="frames"):
    """
    Converts all images in direc to pygame surfaces
    """
    files = sorted(listdir(direc))  # List all files in directory
    all_imgs = [pygame.image.load("frames/" + file_name) for file_name in files]  # Load the images using pygame
    return all_imgs


class AudioInput():

    def __init__(self):
        """
        Initializes a new AudioInput object.
        """
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, 0)
        self.inp.setchannels(1)
        self.inp.setrate(16000)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.inp.setperiodsize(160)

    def get_audio_level(self):
        """
        Returns the audio level at the current time.
        """
        l, data = self.inp.read()  # Read the input data
        if l:
            return audioop.rms(data, 2)  # Returns the current volume
        else:
            return 0


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # Create some computational art!
    num_frames = 50
    # Optionally, generate new frames
    # generate_art("frames/sound", x_size=500, y_size=500, frames=num_frames)
    screen = pygame.display.set_mode((500, 500))
    audio = AudioInput()  # New audioInput object
    imgs_list = get_img_surfaces()  # Gets all imagesseimagesse
    while True:
        level = int(audio.get_audio_level()/500)  # Get current level, approximately scaled 1 - 100
        cur_img = imgs_list[level % num_frames]  # Load the image corresponding to the current level
        screen.blit(cur_img, (0, 0))  # Display the current image
        pygame.display.flip()  # Updat the screen
