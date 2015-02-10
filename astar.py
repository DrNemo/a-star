"""
* A-Star
*
* package A-Star
* @copyright 2014 DrNemo
* @license http://www.opensource.org/licenses/mit-license.html MIT License
* @author DrNemo <drnemo@bk.ru>
* @version 1.0
* 
* example:

import astar
structure_maps = [
	[1,1,1,0,.5,1],
	[1,1,.5,0,.5,1]
	[1,1,.5,.5,.5,1]
	[1,1,.5,0,1,.5]
	[1,1,.5,0,1,.5]
]
diagonal = False
# structure_maps - arrays map[x][y]
# diagonal - diagonal (True/False)

astar = astar.AStar(structure_maps, diagonal)

# set start [x, y]
astar.start([2, 1])

# set stop [x, y]
astar.stop([2, 1])

# add temp let
astar.let([3, 1], float 0-1)

# clear temp lets
astar.clearLets()

# search path
path = astar.search()
while(path):
	point = path.pop(0)
	print point.x, point.y

# example 2:
path = astar.start([2, 1]).stop([2, 1]).search()
"""

class AStar:
	maps_temp = {}

	H_CALCULAT_MANHETON = False

	point_start = False
	point_stop = False

	re_search = True

	path_save = []

	def __init__(self, maps, diagonal = False):
		self.diagonal = diagonal
		self.width = len(maps)
		self.height = len(maps[0])
		
		# generate hash map
		self.maps = {}
		for x in xrange(0, self.width):
			for y in xrange(0, self.height):
				self.maps[self.getHashPoint([x, y])] = maps[x][y]

	@staticmethod
	def getHashPoint(cor):
		return "%i:%i" % (cor[0], cor[1])

	def let(self, cor, cofice = 0):		
		self.maps_temp[self.getHashPoint(cor)] = cofice
		self.re_search = True
		return self

	def clearLets(self):
		self.re_search = True
		self.maps_temp = {}
		return self

	def start(self, cor):
		if not self.pointInMap(cor):			
			raise Exception('Coordinates outside the map area')

		self.re_search = True
		self.point_start = Point(cor)
		return self

	def stop(self, cor):
		if not self.pointInMap(cor):
			raise Exception('Coordinates outside the map area')

		self.re_search = True
		self.point_stop = Point(cor)
		return self

	def pointInMap(self, cor):
		if self.getHashPoint(cor) in self.maps:
			return True
		return False

	def search(self):
		if not self.point_start or not self.point_stop:
			raise Exception('No starting point or finish')
		if not self.re_search:
			return self.path_save[::]

		self.find()
		self.re_search = False

		return self.search()

	def find(self):
		self.path_save = []
		open_point = [self.point_start]
		open_point_hash = {self.point_start.prefix : True}
		close_point = {}
		
		while open_point:
			open_point.sort(key=lambda x: x.f, reverse=False)
			point = open_point.pop(0)

			if self.isFinish(point):
				self.path_save = self.reverse(point)
				break

			else:
				if point.prefix in open_point_hash:
					del open_point_hash[point.prefix]	
			
				new_points = self.getVariantPoint(point)

				while new_points:
					point_temp = new_points.pop(0)
					point_hash = self.getHashPoint(point_temp)

					cofice = self.getCofice(point_temp)
					
					if point_hash in close_point or point_hash in open_point_hash:
						continue

					if point_temp[2]:
						g = point.g + int(10 * cofice)
					else:
						g = point.g + int(14 * cofice)

					h = self.hFabric(point_temp)
					f = int(g + h)
				
					open_point.append( Point(point_temp, g, h, f, point) )
					open_point_hash[point_hash] = True

				close_point[point.prefix] = True

	def getCofice(self, point):
		point_hash = self.getHashPoint(point)
		cofice = self.maps[point_hash]
		if point_hash in self.maps_temp:
			cofice = self.maps_temp[point_hash]

		return cofice

	def isFinish(self, point):
		return point.x == self.point_stop.x and point.y == self.point_stop.y

	def hFabric(self, point):
		if self.H_CALCULAT_MANHETON:
			return self.hManhattan(point)
		else:
			return self.hShortcut(point)

	def hManhattan(self, point):
		return 10 * (abs(point[0] - self.point_stop.x) + abs(point[1] - self.point_stop.y))

	def hShortcut(self, point):
		x_distance = abs(point[0] - self.point_stop.x)
		y_distance = abs(point[1] - self.point_stop.y)
		if x_distance > y_distance:
			h = 14 * y_distance + 10 * (x_distance - y_distance)
		else:
			h = 14 * x_distance + 10 * (y_distance - x_distance)
		return h
	
	def getVariantPoint(self, point):
		new_points = [
			[point.x    , point.y - 1, True],
			[point.x + 1, point.y    , True],
			[point.x    , point.y + 1, True],
			[point.x - 1, point.y    , True]
		]
		if(self.diagonal):
			new_points += [
				[point.x - 1, point.y - 1, False],
				[point.x + 1, point.y - 1, False],
				[point.x + 1, point.y + 1, False],
				[point.x - 1, point.y + 1, False]
			]
		
		valide_point = []
		while new_points:
			point = new_points.pop(0)
			if self.pointInMap(point) and self.getCofice(point) > 0:
				valide_point.append(point)

		return valide_point

	def reverse(self, point):
		stek = [point]
		point = point.parent
		while point:
			stek.append(point)
			if point.parent:
				point = point.parent
			else:
				point = False
		
		return stek[::-1]

class Point:
	def __init__(self, cor, g = 0, h = 0, f = 0, parent = False):
		self.x = int(cor[0])
		self.y = int(cor[1])
		self.prefix = AStar.getHashPoint([self.x, self.y])
		self.parent = parent
		self.g = int(g)
		self.h = int(h)
		self.f = int(f)