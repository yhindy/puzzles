import itertools
import time

"""
It's Winter quarter of your Senior year and you have a few more Ws then you'd like.
In order for you to 'Camp Stanford' next quarter, you need to take as many classes as
possible. Lucky for you all classes meet MWF, so you dont have to worry about the
days of the week, just the times of the day. You need to make a schedule that has
no overlapping classes, however you dont need to take into account the time of
getting from one class to another. One last thing, you are fine with classes that
start at 9, but anything that is later than 6:30 is off the table
The list of possible classes will be listed like this:


Name start_time end_time piece

an example:
CS41 13.5 15 a

you'll notice that we use decimals for minutes and military time to avoid confusion

You probably can't do this problem with a naive brute force approach that will search all
possibilities, but there are ways to filter out classes that you would never take. If done
properly this may leave few enough classes that brute force will work.

Hints:

*   Consider creating a class for a course and reading in the file and creating a list
	of course objects.

*   Write the brute force method first (going through every possible permutations of classes),
	then try making it more efficent.

*   Would you ever choose CS110 instead of CS41?
	CS41 13.5 15 a
	CS110 13.5 16 b
"""

DATA_LOCATION = "courses.txt"


class Class:
	def __init__(self, name, start, end, piece):
		"""
		This function serves as the constructor for the Class class. 

		It contains a name, a start time, an end time, and a puzzle piece
		"""
		self.name = name
		self.start = float(start)
		self.end = float(end)
		self.piece = piece
		pass

	def __str__(self):
		"""
		This function returns a string representation of the Class object.

		E.g. "CS106A 13.5 16 p"
		"""
		return self.name + " " + str(self.start) + " " + str(self.end) + " " + self.piece

	def __lt__(self, other):
		"""
		Returns true if self class starts before other
		"""
		return self.start < other.start

	def endsearlier(self, other):
		"""
		Returns true if self ends before other
		"""
		return self.end < other.end

def brute_schedule(classes):
	"""
	Unfortunately this problem is not solvable by a greedy algorithm so we have to
	either do recursion or something a bit more aggressive. The easiest way to find
	the best schedule is to try to fit as many classes as possible in every
	conceivable order and then keep the best one.

	This function uses the permutations function to find all the
	permutations of the classes and then returns the longest one.
	"""
	perms = []
	currlist = []

	permutations(classes, perms, currlist)

	longest = perms[0]
	for perm in perms:
		if len(perm) > len(longest):
			longest = perm

	return perm 

def permutations(data, perms, currlist):
	"""
	This function recursively finds all of the permutations
	of a given data set. 

	@data the data given
	@perms the permutations
	@currlist the current permutation

	It uses depth-first search to find all of the permutations.

	It does not return anything, but instead modifies the perms list
	that is passed to it.
	"""
	if len(data) == 0:
		perms.append(currlist)
		return
	for piece in data:
		if class_fits(piece, currlist):
			data.remove(piece)
			currlist.append(piece)
			listtoadd = []
			for item in currlist:
				listtoadd.append(item)
			perms.append(listtoadd)
			permutations(data, perms, currlist)
			currlist.remove(piece)
			data.append(piece)
	
	pass

def class_fits(course, sched):
	"""
	This function returns true if the course fits in the schedule passed in
	"""
	for other in sched:
		if course.end > other.end and course.start < other.end:
			return False
		if course.start < other.start and course.end > other.start:
			return False
	return True

def sortclasses(classes): #selection sort
	"""
	This class sorts classes by start time for display.

	It implements selection sort.
	"""
	for i in range(len(classes)):
		minind = i
		for j in range(i+1, len(classes)):
			if (classes[j].start < classes[minind].start):
				minind = j

			if minind != i:
				temp = classes[i]
				classes[i] = classes[minind]
				classes[minind] = temp



def fast_schedule(classes):
	"""
	Takes the classes and keeps only one class per start time with the shortest duration

	For example, with these three classes:
	ClassA 9 12
	ClassB 9 11.5
	ClassC 9.5 12

	This will cut out ClassA becuase you would always prefer ClassB, This leaves:
	ClassB 9 11.5
	ClassC 9.5 12

	This *significantly* cuts down the number of permutations

	It also applies the 9am to 6:30pm time constraint
	"""
	prelimsched = {}
	for course in classes:
		if course.start < 9 or course.end > 18.5:
			classes.remove(course)
		elif prelimsched.get(course.start) == None: #if the dictionary doesnt contain a course at that time
			prelimsched[course.start] = course #add it as the first 
		elif course.endsearlier(prelimsched[course.start]):
			prelimsched[course.start] = course

	classes = list(prelimsched.values())
	
	return classes


if __name__ == '__main__':
	with open(DATA_LOCATION, 'r') as f:
		lines = f.readlines()

	class_strings = [line.strip() for line in lines]
	classes = [Class(*class_str.split()) for class_str in class_strings]
	
	smartclasses = fast_schedule(classes)
	finalsched = brute_schedule(smartclasses)
	finalsched.sort()
	for course in finalsched:
		print(course)
