import pygame
import math
from queue import PriorityQueue
pygame.init()

GRID_WIDTH = 800
WIN_WIDTH = 1200
ROWS = 50 # should divide GRID_WIDTH without reminder

WIN = pygame.display.set_mode((WIN_WIDTH, GRID_WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BAR = (250, 240, 230)
CAPTION = (255, 127, 80)
BARRIER = (139, 69, 19)

clock = pygame.time.Clock()

font26 = pygame.font.SysFont("gillsans", 26)
font18 = pygame.font.SysFont("arial.ttf", 18)
font42 = pygame.font.SysFont("arial.ttf", 42)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows
		self.be_updated = True

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BARRIER

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		if self.be_updated:
			self.color = WHITE
			return True
		return False

	def make_start(self):
		if self.be_updated:
			self.color = ORANGE
			return True
		return False

	def make_closed(self):
		if self.be_updated:
			self.color = RED
			return True
		return False

	def make_open(self):
		if self.be_updated:
			self.color = GREEN
			return True
		return False

	def make_border(self):
		self.color = BLACK

	def make_barrier(self):
		if self.be_updated:
			self.color = BARRIER
			return True
		return False

	def make_end(self):
		if self.be_updated:
			self.color = TURQUOISE
			return True
		return False

	def make_path(self):
		if self.be_updated:
			self.color = PURPLE
			return True
		return False

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end, start_time):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			update_timer(start_time)
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def update_timer(start_time):
	WIN.fill(BAR, (810, 280, 900, 320))
	passed_time = pygame.time.get_ticks() - start_time
	sec = str(passed_time // 1000)
	milisec = str(passed_time / 1000 - passed_time // 1000)
	milisec = milisec[2:4]
	time = sec + "." + milisec + " sec"
	t = font42.render(time, False, CAPTION)
	t_rect = t.get_rect()
	t_rect.centerx, t_rect.centery = 900, 300
	WIN.blit(t, t_rect)

def reset_timer():
	WIN.fill(BAR, (810, 280, 900, 320))

	time = "0.0sec"
	t = font42.render(time, False, CAPTION)
	t_rect = t.get_rect()
	t_rect.centerx, t_rect.centery = 900, 300
	WIN.blit(t, t_rect)

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			if i == 0:
				spot.make_border()
				spot.be_updated = False
			elif i == rows - 1:
				spot.make_border()
				spot.be_updated = False

			elif j == 0 or j == rows - 1:
				spot.make_border()
				spot.be_updated = False
			grid[i].append(spot)


	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE, (0, 0, GRID_WIDTH, GRID_WIDTH))

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	win.fill(BAR)
	grid = make_grid(ROWS, width)

	start = None
	end = None
	run = True

	t = font26.render("Python visualization of A* algorithm", False, CAPTION)
	t_rect = t.get_rect()
	t_rect.centerx, t_rect.centery = WIN_WIDTH - 200, 50

	WIN.blit(t, t_rect)

	t = font18.render("Finding the shortest path from one point to another", False, CAPTION)
	t_rect = t.get_rect()
	t_rect.centerx, t_rect.centery = WIN_WIDTH - 200, 80
	WIN.blit(t, t_rect)

	spot = Spot(0, 0,  GRID_WIDTH // ROWS, 0)
	spot.x = GRID_WIDTH + 30
	spot.y = 120
	spot.make_start()
	spot.draw(win)

	t = font18.render("- starting point", False, CAPTION)
	t_rect = t.get_rect()
	t_rect.centerx, t_rect.centery = GRID_WIDTH + 110, 125
	WIN.blit(t, t_rect)

	spot.draw(win)
	spot.x = GRID_WIDTH + 30
	spot.y = 150
	spot.make_end()
	spot.draw(win)

	t = font18.render("- ending point", False, CAPTION)
	t_rect = t.get_rect()
	t_rect.centerx, t_rect.centery = GRID_WIDTH + 110, 155
	WIN.blit(t, t_rect)

	spot.draw(win)
	spot.x = GRID_WIDTH + 30
	spot.y = 180
	spot.make_barrier()
	spot.draw(win)

	t = font18.render("- barrier", False, CAPTION)
	t_rect = t.get_rect()
	t_rect.centerx, t_rect.centery = GRID_WIDTH + 90, 185
	WIN.blit(t, t_rect)

	t = font18.render("Press Space to start after putting start,", False, CAPTION)
	t_rect = t.get_rect()
	t_rect.centerx, t_rect.centery = GRID_WIDTH + 145, 220
	WIN.blit(t, t_rect)

	t = font18.render("end and barriers", False, CAPTION)
	t_rect = t.get_rect()
	t_rect.centerx, t_rect.centery = GRID_WIDTH + 80, 250
	WIN.blit(t, t_rect)

	t = font42.render("0.00 sec", False, CAPTION)
	t_rect = t.get_rect()
	t_rect.centerx, t_rect.centery = GRID_WIDTH + 100, 300
	WIN.blit(t, t_rect)



	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] < GRID_WIDTH and pygame.mouse.get_pos()[1] < GRID_WIDTH: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if start is None and spot != end:
					if spot.make_start():
						start = spot

				elif end is None and spot != start:
					if spot.make_end():
						end = spot

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if spot.reset():
					if spot == start:
						start = None
					elif spot == end:
						end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					start_time = pygame.time.get_ticks()
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, start_time)


				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
					reset_timer()

	pygame.quit()

main(WIN, GRID_WIDTH)