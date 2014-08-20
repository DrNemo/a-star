"""
* A-Star
*
* package A-Star
* @copyright 2014 DrNemo
* @license http://www.opensource.org/licenses/mit-license.html MIT License
* @author DrNemo <drnemo@bk.ru>
* @version 1.0 beta
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
	maps = {}
	maps_temp = {}
	w = 0
	h = 0
	diagonal = False
	_start = [0, 0]
	_stop = [0, 0]
	_path_save = []
	_re_search = True
	def __init__(self, maps, diagonal = False):
		self.diagonal = diagonal
		self.w = len(maps)
		self.h = len(maps[0])
		# generate hash map
		for x in xrange(0, self.w):
			for y in xrange(0, self.h):
				self.maps[prefix([x, y])] = maps[x][y]

	def let(self, cor, cofice = 0):
		self._re_search = True
		self.maps_temp[prefix(cor)] = cofice
		return self

	def clearLets(self):
		self._re_search = True
		self.maps_temp = {}
		return self

	def start(self, cor):
		self._re_search = True
		self._start = Point(cor)
		return self

	def stop(self, cor):
		self._re_search = True
		self._stop = Point(cor)
		return self

	def search(self):
		if not self._re_search:
			return self._path_save[::]

		if self._stop.prefix in self.maps and not self.maps[self._stop.prefix]:
			return []

		self._path_save = []
		open_point = [self._start]
		open_point_hash = {self._start.prefix : True}
		close_point = {}
		
		while open_point:
			open_point.sort(key=lambda x: x.f, reverse=False)
			point = open_point.pop(0)

			# map size
			if point.x >= self.w or point.y >= self.h or point.x < 0 or point.y < 0:
				continue

			# finish
			if point.x == self._stop.x and point.y == self._stop.y:
				self._path_save = self.reverse(point)
				self._re_search = False
				del open_point, open_point_hash, close_point
				return self.search()

			else:
				if point.prefix in open_point_hash:
					del open_point_hash[point.prefix]	
			
				new_points = [
					[point.x, point.y - 1, True],
					[point.x + 1, point.y, True],
					[point.x, point.y + 1, True],
					[point.x - 1, point.y, True]
				]
				if(self.diagonal):
					new_points_diagonal = [
						[point.x - 1, point.y - 1, False],
						[point.x + 1, point.y - 1, False],
						[point.x + 1, point.y + 1, False],
						[point.x - 1, point.y + 1, False]
					]
					new_points += new_points_diagonal

				while new_points:
					temp_point = new_points.pop(0)
					pref = prefix(temp_point)
					
					if pref not in self.maps:
						continue
					
					# patency
					cofice = self.maps[pref]
					if pref in self.maps_temp:
						cofice = self.maps_temp[pref]

					if cofice > 0 and pref not in close_point:
						g = point.g

						if temp_point[2]:
							g += 10 - 5 * cofice
						else:
							g += 14 - 5 * cofice
						g = int(g)

						h = 10 * (abs(temp_point[0] - self._stop.x) + abs(temp_point[1] - self._stop.y))
						f = int(g + h)
					
						p = Point(temp_point, g, h, f, point)
						if p.prefix not in open_point_hash:
							open_point.append(p)
							open_point_hash[p.prefix] = True

				close_point[point.prefix] = True
							

	def reverse(self, point):
		stek = [point]
		point = point.parent
		while(point):
			stek.append(point)
			if point.parent:
				point = point.parent
			else:
				point = False
		stek = stek[::-1]
		return stek

class Point:
	prefix = "0:0"
	g, x, y, h, f = 0, 0, 0, 0, 0
	parent = False
	def __init__(self, cor, g = 0, h = 0, f = 0, parent = False):
		self.x = int(cor[0])
		self.y = int(cor[1])
		self.prefix = prefix([self.x, self.y])
		self.parent = parent
		self.g = int(g)
		self.h = int(h)
		self.f = int(f)

def prefix(cor):
	return "%i:%i" % (cor[0], cor[1])