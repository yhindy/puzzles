# Image Reassembly

You're almost there! After the previous quest, you finally unlocked the map to the Holy Grail! The journey is almost complete.

Unfortunately, during your post-quest celebration, Sir Belvedere accidently threw the map into the paper shredder! You really should fire that knight. And why did you bring a paper shredder on your travels anyway? Something about medieval taxes... Nonetheless, you will need to reconstruct the map to find your final destination.

## Overview

Your objective for this sub-puzzle is to reconstruct an image from a collection of vertically shredded images. Specifically, you will be given a directory of `k` (`m x n`) images, and will need to reconstruct them into one (`m x kn`) image. The vertical shredded images are mutually exclusive and collectively exhaustive - that is, they represent the entire image but they don't overlap.

## Helpful Utilities

We have provided a general utility library to interact with image files in `imageutils.py`, which exports some useful functions:

```
def load_image(filename):
    """
    Return a 2D array of pixels in column-major order
    from the image specified by filename.

    @param filename: absolute or relative name of the image file
    @return: 2D list of `Pixel`s from image in column-major order
    """
    
def save_image(data, filename):
    """Save a PNG of the image data to disk under the given filename.

    @param data2D: column-major order 2D list of Pixels in the image
    @param filename: name of the file to save
    """

def show_image(data):
    """Open a preview of the image data - useful for debugging.

    @param data2D: column-major order 2D list of Pixels in the image
    """

def show_all_images(slc, *rest, buffer_width=1):
    """
    Draw all vertical slices in one image with a black buffer line of pixels
    buffer_width pixels wide. Useful for debugging.

    @param slc, *rest: collection of vertical slices to display
    @param buffer_width: number of black pixels between consecutive slices.
    """
    
def files_in_directory(dirname):
    """Return a list of filenames in the given directory.

    @param dirname: name of directory from which to acquire files.
    @return: list of strings representing names of files in the given directory
    """
```

Note: We have adopted the convention that images will be represented in column major order - that is, the first element (at index 0) of the 2-dimensional array returned by `load_image` is a list representing the first column of the image, not the first row. Keep this in mind while writing your code.

Warning: The data you'll be working with in this problem represent very large lists, potentially on the order of 1000s x 1000s. As such, please don't try to print all of your image data to the console at once, or else your console might freeze. You can print out slices of the data (for example, the first ten pixels in a given column) for debugging purposes, but be aware that these data structures are very large. If you need to regain control from a runaway expression, you can send a KeyboardInterrupt in the interactive interpreter. If that fails, quit Python and relaunch.

Each pixel is represented as an instance of a `Pixel` class, built using `namedtuple` - that is, you can treat a given Pixel `p` like a 4-tuple  `p = (R, G, B, A)`, or you can access the pixel's fields using

```
p.red    # Get red component of Pixel
p.green  # Get green component of Pixel
p.blue   # Get blue component of Pixel
p.alpha  # Get alpha component of Pixel
```

Each value represents the intensity of red, green, blue, and alpha channels, respectively, and is guaranteed to be an integer between 0 and 255, inclusive.

### Installing Required Dependencies

**Our `imageutils.py` script is layered on top of the Python Image Library (PIL) - specifically, we rely on an actively maintained fork called `Pillow`. Before you can begin development, you must install the `Pillow` package into your environment. Luckily, we built virtual environments at the start of the year for this exact purpose!**

If you wish, you don't need to use our `imageutils` helper module if you don't want to. However, it will be *really* helpful, and if you *do* decide to utilize the functionality of `imageutils.py`, you'll need to install `Pillow` first. We can do this using the virtual environment that you created at the start of the quarter.

### (1) Activate your Virtual Environment.

If you installed your virtual environment using `pyvenv` or any equivalent (including a standalone `virtualenv`), you will need to run:

```
# If installed with pyvenv or virtualenv
$ source /path/to/my/virtualenv/for/cs41/bin/activate/
```

If you installed using `virtualenvwrapper` and `mkvirtualenv`, you will need to run:

```
$ workon cs41
```

If you don't remember which you installed, try both! Although you don't explicitly need a virtual environment for this project, it's good style to keep project-specific installations (like `Pillow`) away from global access.

You'll know this step is working when you see the parenthesized virtual environment name precede your command prompt. For me, this looks like:

```
(cs41)sredmond:stanfordpython $
```

### (2) Install `Pillow`

From there, just run `pip install Pillow`. You should see output similar to:

```
(cs41)sredmond:stanfordpython $ pip install Pillow
Collecting Pillow
  Downloading Pillow-3.2.0-cp34-cp34m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl (3.0MB)
    100% |████████████████████████████████| 3.0MB 229kB/s
Installing collected packages: Pillow
Successfully installed Pillow-3.2.0
```

That's it!

*Note: in the worst case, if you can't locate or activate your virtual environment from the start of the quarter, it's *okay*, although undesirable, to perform a global install. However, this usually causes more problems that it solves, and you need to be careful about Python 2/3 compatibility issues.*

### (3) Check the Installation

Once this library is installed, you should be set to develop. Just to be sure, you can run `python3 imageutils.py` from the command line, which will check to see if Pillow is installed correctly, and print out an error message if it is not.

*Note: You'll need to be inside an active virtual environment whenever you run your `reassemble` script, so that Python can find the `Pillow` package.*


## General Algorithmic Hints

A reasonable approach is to look at all pairs of shredded image slices, decide which pair matches up best, and glue those two slices together into a slightly bigger slice. Rinse and repeat until there is just one piece left - it's the reconstructed image!

How do we determine the similarity between two vertically shredded image slices? There are many different approaches, but one that seems to work is to look at the rightmost column of the left piece and the leftmost column of the right piece to see how well they match up.

How do we decide how well two columns match up? We can look at pixels componentwise. If that's not quite enough, we can look around a given pixel and incorporate the values of its neighbors. The details are up to you.

How similar are pixels? Again, there are many different ways to approach this problem, each of which yields varying degrees of success. One approach that works well is to sum the squares of the absolute difference between each color channel.

Consider the functional aspect to the above design. A `slice_similarity` function needs some `column_similarity` function to operate - perhaps it could be a parameter! Similarly, the `column_similarity` function needs a `pixel_similarity` function to work - instead of hardcoding in the pixel similarity code, you could write a few `pixel_similarity` functions, pass them into `column_similarity`, and see which one works best.

## Starter Files
	
```
imagereassemble/
├── completed-dna.txt
├── README.md
├── imageutils.py
├── reassemble.py
└── shredded
    ├── grail4/
    ├── grail20/
    └── destination/
```

Fill out the Google form linked in `completed-dna.txt` to get credit for finishing up the DNA puzzle.

In addition to the `imageutils.py` utility file, you will find a number of vertically shredded images in `shredded/`. The images in `grail4/` represent an image that has been shredded into four pieces, each of which is wide enough to reassemble by hand, so you can check your work. The images in `grail20/` represent the same image, sliced into 20 pieces.

If you want additional shredded images to play around with, consider building your own, or email us for another sample.

Your should implement your code to reassemble image slices in `reassemble.py`. You have total freedom to design and implement your solution to this problem - our algorithmic hints above are just suggestions, and you can deviate in any way you'd like. Due to this freedom, think about your general approach before starting. If you don't have a plan, this assignment can get complicated quickly, but if you know your goal, it's not too bad.

## Your Challenge

Ultimately, your goal (and success in this part) will be to reassemble the slices in the `shredded/destination/` folder. These image slices are a lot larger than those in `grail4/` or `grail20/`, and there are a lot more of them, so you will need to think about efficiency.

Once you reassemble the destination picture, **you need to find and go to that spot on campus in order to complete the quest!** In particular, we will hide a physical bag somewhere inside the frame of the reassembled destination, and inside the bag will be a slip of paper with a Google form link.

*If you have reassembled the destination image, but can't figure out where on campus it actually *is*, no worries. That's **definitely** not a Python problem. If you ask, we'll send you more geographic hints in the form of more shredded images.*

This is a hard problem, so please post questions on Piazza if you are stuck. Furthermore, we want to remind everyone that it's okay to not finish this problem if you're spending an exorbitant amount of time and effort. You can also come visit us during office hours for more help.

For reference, our solution is about 50 lines of code, not counting comments or whitespace.

> With <3 by "shredmond" ;)