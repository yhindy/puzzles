''' 
										~INTRODUCTION~
	Welcome to Python Genetic Mutation Lab! For this part of the scavenger hunt, you will write a program
	to efficiently determine the fewest number of moves required to transform a strand of Python2 DNA 
	to Python3 DNA. A move is defined as either an insertion, deletion, or substitution, and the DNA strands
	are modeled as strings made exclusively from the character set {A, C, G, T}. The sequences of interest have been extracted 
	and places in .txt files in the res folder. Now it's your job to design a program to quickly count the minimum number of
	moves to get from one strand to another.
	Let's get started.
'''

'''
										~GENERAL ALGORITHM~
	The problem of efficiently transforming one string into another boils down to finding what's called the 
	"minimum edit distance" (AKA Levenshtein distance). A helpful way to break it down recursively is if you're trying to 
	find min edit distance between "caa" and "agt", use a brute force approach as follows:
		(1) calculate min distance assuming you delete last char ("caa" --> "ca")
		(2) calculate min distance assuming you insert a last char ("caa" --> "caat")
		(3) calculate min distance assuming you substitute the last char ("caa" --> "cat")
	The idea here is to recurse on substrings of the original strings until the base case is reached.
'''

'''
											~HINTS~
	- The best way to get from "" to any other string is to insert all the characters in the non-empty string.
	- If the last characters of 2 sequences are the same, then you can simply recurse on the start[:-1], end[:-1]
	- First get your program to work on the small sequences. Depending on how you solve the problem, you may or may not 
		need to utilize a technique called memoization to make your algorithm work for larger DNA strands. In my solution, the
		prototype for minDistance was minDistance(start, end, cache) because various operations might recursively lead to solving the 
		min edit distance between, say, "catca" and "agcta". If I cache these values (cache simply means to store in an accessible data structure),
		the program can quickly read the values from the data structure instead of performing the recursion many times. 

		Here's a helpful article explaining the usefulness of memoization (basically caching):
			http://stackoverflow.com/questions/1988804/what-is-memoization-and-how-can-i-use-it-in-python
'''

DNA = ['c', 'a', 'g', 't']

def minDistance(start, end, cache):
	"""
	This function returns the minimum distance (Levenshtein distance)
	between two words. It also stores the combinations and their lengths
	in a cache to speed up the process.

	It does so with recursion:

	base case: the word start is the empty string, in which case the distance
	is just the number of letters in the other word.

	"""
	if (start,end) in cache:
		return cache[(start,end)]
	if len(start) > len(end): # always want start to be shorter
		start, end = end, start
	if start == '': # base case: if start is empty, it takes len(end) steps to get to end
		return len(end)
	if start[-1] == end[-1]: # if last letters are the same, do mindistance on the rest
		dist = minDistance(start[:-1], end[:-1], cache)
		cache[(start[:-1], end[:-1])] = dist
		return dist
	if start[0] == end[0]: # if first letters are the same, do mindistance on the rest
		dist = minDistance(start[1:], end[1:], cache)
		cache[(start[1:], end[1:])] = dist
		return dist
	deleted = 1 + minDistance(start[:-1], end, cache)
	substitute = 1 + minDistance(start[:-1] + end[-1], end, cache)
	add = 1 + minDistance(start + end[-1], end, cache)

	return min([deleted, substitute, add])


if __name__ == '__main__':
	pairs = {}
	cache = {}
	with open('dna.txt', 'r') as f:
		lines = f.readlines()
		couples = [line.strip() for line in lines]
		pairs = {strings.split()[0]:strings.split()[1] for strings in couples}

	totalmoves = 0
	for start,end in pairs.items():
		dist = minDistance(start,end, cache)
		totalmoves = totalmoves + dist
		print(start, end, dist)

	print(totalmoves)

	pass