import matplotlib.path as mpath

def getPuzzleInput():
	with open("/Users/abeen/Documents/repos/AdventOfCode/2025/Day 09/Day 9.txt") as file:
		return file.read()
	
def getPointCombinations(points):
	pointCombinations = []

	for i in range(len(points)):
		point1 = points[i]
		for j in range(len(points)):
			if i == j:
				continue
			point2 = points[j]
			pointCombinations.append((point1, point2, getArea(point1, point2)))
	pointCombinations.sort(key=lambda x: x[2], reverse=True)
	return pointCombinations

def getArea(point1, point2):
	if point1[0] == point2[0]:
		return abs(point1[1] - point2[1]) + 1
	elif point1[1] == point2[1]:
		return abs(point1[0] - point2[0]) + 1
	else:
		return (abs(point1[0] - point2[0]) + 1) * (abs(point1[1] - point2[1]) + 1)
	
def createBorders(points):
	outerBorderPoints = []
	for i in range(len(points)):
		x1, y1 = list(points[i%len(points)])
		x2, y2 = list(points[(i+1)%len(points)])

		# going up
		if x1 < x2:
			x1 += 1
			y2 += 1
			outerBorderPoints.extend([(x,y) for x in range(x1-2, x2+2) for y in range(y1-1, y2-1)])
		
		# going right
		elif y1 < y2:
			x2 += 1
			y1 += 1
			outerBorderPoints.extend([(x,y) for x in range(x1+1, x2+1) for y in range(y1-2, y2+2)])

		# going down
		elif x1 > x2:
			x2 += 1
			y2 += 1
			outerBorderPoints.extend([(x,y) for x in range(x2-2, x1+2) for y in range(y1+1, y2+1)])

		# going left
		elif y1 > y2:
			x2 += 1
			y2 += 1
			outerBorderPoints.extend([(x,y) for x in range(x1-1, x2-1) for y in range(y2-2, y1+2)])
	
	return outerBorderPoints

def dedupe(arr: list[tuple]) -> list:
	newArr = []
	for a in arr:
		if a not in newArr:
			newArr.append(a)
	return newArr

def getLargestArea(outerBorderPoints: list, pointCombinations: list[tuple]) -> int:
	# The outer corners of the shape if you expanded the perimeter by one
	corners = dedupe([c for c in outerBorderPoints if outerBorderPoints.count(c) > 1])
	corners.append(corners[0]) # to complete the path for mpath to use

	# create a path between the corners
	outerPath = mpath.Path(corners)

	# Go through all of the possible combinations of points around the shape
	for i in range(len(pointCombinations)):
		pc1, pc2 = pointCombinations[i][0:2]
		
		# Create a path from the rectangles opposite points
		rectPoints = [pc1, (pc1[0], pc2[1]), pc2, (pc2[0], pc1[1]), pc1]
		rectPath = mpath.Path(rectPoints)

		# If the path of the rectangle is completely contained within the path the corners make
		if outerPath.contains_path(rectPath):
			# And it's area is the largest we've seen
			if (a := getArea(pc1, pc2)) > largestArea:
				# Ladies and gentlemen, we got 'em.
				largestArea = a

	return largestArea


if __name__ == "__main__":
	points = [(int(x.split(",")[0]), int(x.split(",")[1])) for x in getPuzzleInput().split("\n")]
	pointCombinations = getPointCombinations(points)
	outerBorderPoints = createBorders(points)
	largestArea = getLargestArea(outerBorderPoints, pointCombinations)
	print(largestArea)
