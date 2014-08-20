a-star
======

algorithm a-star python

example:

import astar
structure_maps = [
	[1,1,1,0,.5,1],
	[1,1,.5,0,.5,1]
	[1,1,.5,.5,.5,1]
	[1,1,.5,0,1,.5]
	[1,1,.5,0,1,.5]
]
diagonal = False
# structure_maps - arrays map[x][y] = float 0-1
# diagonal - diagonal (True/False)

astar = astar.AStar(structure_maps, diagonal)

# set start [x, y]
astar.start([2, 1])

# set stop [x, y]
astar.stop([2, 1])

# search path
path = astar.search()
while(path):
	point = path.pop(0)
	print point.x, point.y

# example 2:
path = astar.start([2, 1]).stop([2, 1]).search()
