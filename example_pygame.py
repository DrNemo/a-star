import sys, pygame, random, math
import astar as AStar
pygame.init()

size = width, height = 800, 800
map_size = [22, 22]
block_size = 32
point_cofice = xrange(10)
black = (0, 0, 0)

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

contener = pygame.Surface([map_size[0] * block_size, map_size[1] * block_size])
contener.fill(black)

font = pygame.font.SysFont("Verdana", 10)

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
		block.blit(label, (12, 5))
		label = font.render(AStar.prefix([x, y]), 1, (255,0,0))
		block.blit(label, (7, 17))

		rect = block.get_rect()
		rect.x = x * block_size
		rect.y = y * block_size

		contener.blit(block, rect)
		y += 1
	x += 1
	y = 0



start = [1, 1]
finish = [11, 11]
astar = AStar.AStar(structure_maps, True).start(start).stop(finish)

clock = pygame.time.Clock()

rect = contener.get_rect()
offset_x = rect.x = int((width - (block_size * map_size[0])) / 2)
offset_y = rect.y = int((height - (block_size * map_size[1])) / 2)

move_x, move_y = 0, 0
while 1:
	screen.fill(black)	
	screen.blit(contener, rect)	

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.MOUSEMOTION:
			mx, my = event.pos
			move_x = mx = math.ceil((mx - offset_x) / block_size)
			move_y = my = math.ceil((my - offset_y) / block_size)
			if mx >= 0 and my >= 0:
				finish = [mx, my]
				astar.stop(finish)
				
		if event.type == pygame.MOUSEBUTTONDOWN:
			mx, my = event.pos
			mx = math.ceil((mx - offset_x) / block_size)
			my = math.ceil((my - offset_y) / block_size)
			if mx >= 0 and my >= 0:
				start = [mx, my]
				astar.start(start)

	path = astar.search()
	
	if path:
		panel_path = pygame.Surface([100, len(path) * 11])
	else:
		panel_path = pygame.Surface([100, 20])
	panel_path.fill((225, 225, 225))
	path_step = 0
	while path:
		point = path.pop(0)
		point_block = pygame.Surface([block_size, block_size])
		point_block.fill((255, 0, 0))
		point_block.set_alpha(50)

		point_rect = point_block.get_rect()
		point_rect.x = offset_x + point.x * block_size
		point_rect.y = offset_y + point.y * block_size

		label = font.render(AStar.prefix([move_x, move_y]), 1, (255,0,0))
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

	clock.tick(60)
