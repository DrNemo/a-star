a-star
======

algorithm a-star python

example:

```python
import astar
#structure_maps - arrays map[x][y] = float 0-1
structure_maps = [
	[1,1,1,0,.5,1],
	[1,1,.5,0,.5,1]
	[1,1,.5,.5,.5,1]
	[1,1,.5,0,1,.5]
	[1,1,.5,0,1,.5]
]
#diagonal - diagonal (True/False)
diagonal = False

astar = astar.AStar(structure_maps, diagonal)

# set start [x, y]
astar.start([2, 1])

#set stop [x, y]
astar.stop([3, 4]) 

#search path
path = astar.search() 

while(path):
	point = path.pop(0)
	print point.x, point.y
```

example 2:
```
path = astar.start([2, 1]).stop([2, 1]).search()
```
