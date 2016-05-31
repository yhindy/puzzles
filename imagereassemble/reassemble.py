#!/usr/bin/env python3 -tt
"""
File: reassemble.py
-------------------
Assignment 2: Quest for the Holy Grail
Course: CS 41
Name: <Yousef Hindy>
SUNet: <yhindy>

This program reassembles a shredded image by using 
a comparison of the extreme columns of two image strips.
It merges the best fits together until the final image is 
created.
"""
import imageutils as iu
import collections 
import sys
import os

PATH_NAME = 'shredded/destination/'

def findCurrScore(image1, image2):
	"""
	This function finds the lowest score of two shredded 
	images.

	It does so by finding the score by aligning them one way 
	and then the other. The lowest one is then returned as a tuple
	with the score, orientation, and image
	"""
	scoreleft = Score(calculateScore(image1, image2), True, image2)
	scoreright = Score(calculateScore(image2, image1), False, image2)

	currminscore = None
	if (scoreleft.score < scoreright.score):
		currminscore = scoreleft
	else:
		currminscore = scoreright

	return currminscore

def calculateScore(image1, image2):
	"""
	This function calculates the score of putting
	image1 on the left of image 2.

	It does so by going pixel by pixel in the farthest
	column and summing the differences of each pixels.

	It returns the score.
	"""
	image1col = image1[-1]
	image2col = image2[0]

	tuples = zip(image1col, image2col)

	score = 0
	for pixel1, pixel2 in tuples:
		score += comparePixels(pixel1, pixel2)

	return score

def comparePixels(pixel1, pixel2):
	"""
	This function calculates the difference between two
	pixels by summing the squares of the differences
	of the different components, R,G,B, and A.

	It returns the total difference.
	"""
	total = 0
	total += (pixel1.red - pixel2.red)**2
	total += (pixel1.green - pixel2.green)**2
	total += (pixel1.blue - pixel2.blue)**2
	total += (pixel1.alpha - pixel2.alpha)**2
	return total

def merge(image1, image2, onleft):
	"""
	This function takes two images and an orientation
	and returns the two images put together.

	It does so by manually manipulating the data and appending
	the data from the right image to the one on the left.

	Returns the final merged image.
	"""
	if not onleft:
		return merge(image2, image1, True)

	finalimage = image1

	for col in image2:
		finalimage.append(col)
	return finalimage

if __name__ == '__main__':
	images = [] #the holder for image data
	for file in [doc for doc in os.listdir(PATH_NAME)]: #importing all images into images
		images.append(iu.load_image(PATH_NAME + file))

	""" Named tuple that contains score information, orientation, and an image """
	Score = collections.namedtuple('Score', ['score','onleft', 'image'])

	""" Iterates until there is only one image left and merges most similar images """
	while (len(images) > 1):
		for image in images:
			images.remove(image)
			bestScore = Score(-1, True, None) #True for image on left
			for otherimage in images:
				if otherimage == None:
					break
				currminscore = findCurrScore(image, otherimage)

				if (bestScore.score == -1 or currminscore.score < bestScore.score): 
					bestScore = currminscore

			images.remove(bestScore.image)
			newimage = merge(image, bestScore.image, bestScore.onleft)
			images.append(newimage)

	for image in images:
		iu.show_image(image)
	print(len(images))

