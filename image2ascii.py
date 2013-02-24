#!/usr/bin/env python
"""A module for converting an image to ASCII. Darker pixels are
represented by random letters while lighter pixels are represented by
the space character.

Good results are achieved by using an image that contains large,
low-contrast shapes. (e.g., a picture of a black square on a white
background produces really good result whereas a picture of a jungle
will produce an unrecognizable one.)

This module can be invoked directly like:

  ./image_to_ascii.py <path-to-image>

The above invocation will write the results to stdout.

Alternatively, you can import this module.

In order to use generate_ascii_from_image() or to invoke this module
directly, you will need the Python Imaging Library (PIL) installed on
your system:

    sudo pip install PIL

"""

import random
import Image
import ImageOps
import sys

__author__ = 'Aryan Naraghi (aryan.naraghi@gmail.com)'
__all__ = ['generate_ascii_from_data', 'generate_ascii_from_image']


DEFAULT_WIDTH = 80

NUM_LETTERS = 26
EMPTY_CHAR = ' '


def generate_char():
    """Returns a random character in the range ['a', 'z']."""
    return chr(ord('a') + random.randint(0, NUM_LETTERS - 1))


def output(value):
    """Returns EMPTY char for values >= 128, else a random lower-case letter."""
    return generate_char() if value < 128 else EMPTY_CHAR


def generate_ascii_from_data(image_data, width, fp=None):
    """Generates an ASCII representation of the given image data. The
    image data should be a row-major list of grayscale values (in the
    range [0, 255]). The results are written to a file-like object fp.
    If fp is not specified, the results are written to stdout."""
    fp = fp or sys.stdout
    for i in xrange(len(image_data)):
        if i % width == 0:
            fp.write('\n')
        fp.write(output(image_data[i]))
    fp.write('\n')


def generate_ascii_from_image(image_path, desired_width=DEFAULT_WIDTH, fp=None):
    """Generates an ASCII representation for the image pointed to by
    image_path. desired_width dictates the number of characters that
    should be used horizontally. The new height is chosen such that
    the ascpect ratio of the image is preserved. The results are
    written to a file-like object fp. If fp is not specified, the
    results are written to stdout."""
    img = Image.open(image_path)
    width, height = img.size
    new_height = int(float(height) * desired_width / width)
    img = ImageOps.grayscale(img.resize((desired_width, new_height)))
    generate_ascii_from_data(img.getdata(), desired_width, fp=fp)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError('You must specify a path to an image.')
    generate_ascii_from_image(sys.argv[1])
