#!/usr/bin/env python3 -tt
"""
Lightweight wrapper library around Pillow for CS41: hap.py code.

If you're a student reading this, you probably shouldn't modify this file.

@author sredmond
@date 2016-04-26
"""
import collections  # namedtuple
import itertools    # chain.from_iterable
import pathlib      # Path, is_dir, iterdir, is_file
import sys          # exit

# Try importing PIL
# When run as a script, print a message both on success and on failure
if __name__ == '__main__':
    print("Attempting to import required libraries...\n")
    try:
        from PIL import Image
    except ImportError:
        print("Oh no! The Python Image Library is not installed.")
        print("Did you `pip install Pillow` inside your virtual environment")
        print("and are you executing this script from inside your venv?")
        retcode = 1
    else:
        print("Everything looks OK!")
        print("PIL can be imported without error.")
        retcode = 0
    finally:
        sys.exit(retcode)

# When imported, only print a message on error.
try:
    from PIL import Image
except ImportError:
    print("Failed to import PIL. Are you sure it's installed?")
    sys.exit(1)

Pixel = collections.namedtuple('Pixel', ['red', 'green', 'blue', 'alpha'])


def load_image(filename):
    """
    Return a 2D array of pixels in column-major order
    from the image specified by filename.

    @param filename: absolute or relative name of the image file
    @return: 2D list of `Pixel`s from image in column-major order
    """
    with Image.open(filename, 'r') as image:
        image = image.convert('RGBA')
    pixels = map(Pixel._make, image.getdata())
    return _swap_major(_unflatten(pixels, image.width, image.height))


def save_image(data2D, filename):
    """Save a PNG of the image data to disk under the given filename.

    @param data2D: column-major order 2D list of Pixels in the image
    @param filename: name of the file to save
    """
    data2D = _swap_major(data2D)
    image = _to_image(data2D)
    image.save(filename, format='PNG')


def _swap_major(data2D):
    """Swap the major ordering of a 2D list"""
    width, height = len(data2D[0]), len(data2D)
    columns = []
    for i in range(width):
        columns.append([data2D[j][i] for j in range(height)])
    return columns


def _flatten(data2D):
    """Flatten a 2D list"""
    return list(itertools.chain.from_iterable(data2D))


def _unflatten(datagen, width, height):
    """Unflattens a 1D generator into a width x height 2D list"""
    buffered = list(datagen)
    assert len(buffered) == width * height
    length = len(buffered)
    # Not the best way to slice a list, but it'll do
    return [buffered[i:i+width] for i in range(0, length, width)]


def _to_image(data2D):
    """Converts 2D pixels to a PIL.Image"""
    size = len(data2D[0]), len(data2D)
    image = Image.new('RGBA', size)
    data1D = _flatten(data2D)
    image.putdata(data1D)
    return image


def show_image(data2D):
    """Open a preview of the image data - useful for debugging.

    @param data2D: column-major order 2D list of Pixels in the image
    """
    data2D = _swap_major(data2D)
    image = _to_image(data2D)
    image.show()


def show_all_images(slc, *rest, buffer_width=1):
    """
    Draw all vertical slices in one image with a black buffer line of pixels
    buffer_width pixels wide. Useful for debugging.

    @param slc, *rest: collection of vertical slices to display
    @param buffer_width: number of black pixels between consecutive slices.
    """
    width, height = len(slc), len(slc[0])
    slices = []
    slices += slc
    black = Pixel(0, 0, 0, 0)
    for chunk in rest:
        slices += [[black for _ in range(height)] for _ in range(buffer_width)]
        slices += chunk
    show_image(slices)


def files_in_directory(dirname):
    """Return a list of filenames in the given directory.

    @param dirname: name of directory from which to acquire files.
    @return: list of strings representing names of files in the given directory
    """
    p = pathlib.Path(dirname)
    if not p.is_dir():
        raise NotADirectoryError("`{d}` is not a directory".format(d=dirname))
    return [str(child) for child in p.iterdir() if child.is_file()]


# The __all__ variable, if defined, contains the symbols to import
# if using `from image import *`
__all__ = [
    'Pixel',
    'load_image', 'save_image',
    'show_image', 'show_all_images',
    'files_in_directory'
]
