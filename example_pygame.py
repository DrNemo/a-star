import sys, pygame, random, math
import astar as AStar
pygame.init()

size = width, height = 800, 800
map_size = [22, 22]
block_size = 32
point_cofice = xrange(10)

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

# generate random map
x, y = 0, 0
structure_maps = []
while(x < map_size[0]):
	structure_maps.append([])
	while(y < map_size[1]):
		cofice = random.choice(point_cofice) * .1
		structure_maps[x].append(cofice)
		y += 1
	x += 1
	y = 0
"""
# static map
structure_maps = [
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, .2, .2, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1],
	[1, 1, 1, .5, .2, 0, 0, .2, .5, 1, 1, 1]
]
#"""

map_size = [len(structure_maps), len(structure_maps[1])]

contener = pygame.Surface([map_size[0] * block_size, map_size[1] * block_size])
contener.fill((0, 0, 0))

font = pygame.font.SysFont("Verdana", 10)

# render map
x, y = 0, 0
while(x < len(structure_maps)):
	while(y < len(structure_maps[0])):
		cofice = structure_maps[x][y]

		if(cofice):
			color = (0, 255, 100 - int(100 * cofice))
		else:
			color = (0, 255, 255)

		block = pygame.Surface([block_size, block_size])
		block.fill(color)

		label = font.render(str(cofice), 1, (255,0,0))
		block.blit(label, (8, 5))
		label = font.render(AStar.AStar.getHashPoint([x, y]), 1, (255,0,0))
		block.blit(label, (1, 17))

		rect = block.get_rect()
		rect.x = x * block_size
		rect.y = y * block_size

		contener.blit(block, rect)
		y += 1
	x += 1
	y = 0

# default point
start = [1, 1]
finish = [11, 11]

clock = pygame.time.Clock()
rect = contener.get_rect()
offset_x = rect.x = int((width - (block_size * map_size[0])) / 2)
offset_y = rect.y = int((height - (block_size * map_size[1])) / 2)

# AStar init 
astar = AStar.AStar(structure_maps, False).start(start).stop(finish)

move_x, move_y = finish
temp_points = []
while 1:
	screen.fill((0, 0, 0))	
	screen.blit(contener, rect)	

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		# event move
		if event.type == pygame.MOUSEMOTION:
			mx, my = event.pos
			move_x = mx = math.ceil((mx - offset_x) / block_size)
			move_y = my = math.ceil((my - offset_y) / block_size)
			if mx >= 0 and my >= 0 and mx < map_size[0] and my < map_size[1]:
				finish = [mx, my]
				# AStar set stop
				astar.stop(finish)
			
		# event click	
		if event.type == pygame.MOUSEBUTTONDOWN:
			mx, my = event.pos
			mx = math.ceil((mx - offset_x) / block_size)
			my = math.ceil((my - offset_y) / block_size)
			if mx >= 0 and my >= 0 and mx < map_size[0] and my < map_size[1]:
				start = [mx, my]
				# AStar set start
				astar.start(start)

		# event any key, generate random let
		if event.type == pygame.KEYDOWN:
			temp_points = []
			# AStar clear let
			astar.clearLets()

			count = random.randrange(3, 10)
			while(count):
				cor = [random.randrange(0, map_size[0]), random.randrange(0, map_size[1])]
				# AStar set let
				astar.let(cor)

				temp_points.append(cor)
				count -= 1

	# render temp_point
	for temp_point in temp_points:
		
		point_block = pygame.Surface([block_size, block_size])
		point_block.fill((0, 0, 0))

		point_rect = point_block.get_rect()
		point_rect.x = offset_x + temp_point[0] * block_size
		point_rect.y = offset_y + temp_point[1] * block_size
		screen.blit(point_block, point_rect)

	# AStar search path
	path = astar.search()
	
	if path:
		panel_path = pygame.Surface([100, len(path) * 11])
	else:
		panel_path = pygame.Surface([100, 20])
	panel_path.fill((225, 225, 225))

	# render path
	path_step = 0
	while path:
		point = path.pop(0)
		point_block = pygame.Surface([block_size, block_size])
		point_block.fill((255, 0, 0))
		point_block.set_alpha(100)

		point_rect = point_block.get_rect()
		point_rect.x = offset_x + point.x * block_size
		point_rect.y = offset_y + point.y * block_size

		label = font.render(AStar.AStar.getHashPoint([move_x, move_y]), 1, (255,0,0))
		screen.blit(point_block, point_rect)

		label = font.render("step %s: %s:%s" % (path_step, point.x, point.y) , 1, (255,0,0))
		panel_path.blit(label, (10, path_step * 10))

		path_step += 1

	#cor click and move
	panel_mouse = pygame.Surface([100, 30])
	panel_mouse.fill((225, 225, 225))
	label = font.render("click: %s:%s" % (start[0], start[1]) , 1, (255,0,0))
	panel_mouse.blit(label, (10, 3))
	label = font.render("move: %s:%s" % (finish[0], finish[1]) , 1, (255,0,0))
	panel_mouse.blit(label, (10, 15))

	screen.blit(panel_mouse, (10, 10))
	screen.blit(panel_path, (width - 110, 10))
			
	pygame.display.flip()

	clock.tick(30)
