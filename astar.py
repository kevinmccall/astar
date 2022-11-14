import pygame
import math

from pygame import mouse


class Tile:
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.walkable = True
        self.fcost = None
        self.gcost = None
        self.hcost = None
        self.neighbor = None

    def set_walkable(self, val):
        self.walkable = val

    def get_pos(self):
        return (self.x, self.y)

    def set_costs(self, gcost, hcost):
        self.hcost = hcost
        self.gcost = gcost
        self.fcost = hcost + gcost

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return (x, y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return (x, y)


class Grid:
    def __init__(self, grid_size_x, grid_size_y) -> None:
        super().__init__()
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.tiles = []

    def generate_grid(self):
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                tile = Tile(x, y)
                self.tiles.append(tile)

    def get_shortest_path(self, start, end):
        path = end - start
        x = path[0]
        y = path[1]
        if x > y:
            return abs(y * 14) + abs((x - y) * 10)
        else:
            return abs(x * 14) + abs((y - x) * 10)

    def astar(self, start, end):
        need_evaluation = []
        evaluated = []
        path = []
        path_found = False
        target_cell = None

        def evaluate(cell):
            evaluated.append(cell)
            for n in self.get_neighbors(cell):
                if n not in evaluated and n.walkable:
                    need_evaluation.append(n)
                    gcost = self.get_shortest_path(start, n)
                    hcost = self.get_shortest_path(n, end)
                    if n.fcost != None:
                        if n.fcost > gcost + hcost:
                            n.set_costs(gcost, hcost)
                            n.neighbor = cell
                    else:
                        n.set_costs(gcost, hcost)
                        n.neighbor = cell

            return cell.get_pos() == end.get_pos()

        evaluate(start)
        while not path_found:
            low = 999999999999
            for cell in need_evaluation:
                if (
                    cell.fcost < low
                    and cell.walkable == True
                    and not (cell in evaluated)
                ):
                    low = cell.fcost
                    target_cell = cell

            path_found = evaluate(target_cell)

        previous_cell = target_cell.neighbor
        while previous_cell != None:
            path.insert(0, previous_cell)
            previous_cell = previous_cell.neighbor
        return path

    def get_tile(self, x, y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile
        else:
            return None

    def get_neighbors(self, tile):
        tiles = []
        for x in range(tile.x - 1, tile.x + 2):
            for y in range(tile.y - 1, tile.y + 2):
                test_tile = self.get_tile(x, y)
                if test_tile != None and not (x == tile.x and y == tile.y):
                    tiles.append(test_tile)
        return tiles


grid = Grid(10, 10)

# Simple pygame program

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
while running:

    start = None
    end = None

    scale = 32
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x, mouse_y = math.floor(mouse_x / scale), math.floor(mouse_y / scale)

    current_tile = grid.get_tile(mouse_x, mouse_y)
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and current_tile != None:
                start = current_tile
                if pos_to_rect != None:
                    pos_to_rect[(mouse_x, mouse_y)].color = (255, 255, 255)
            if event.button == 3 and current_tile != None:
                end = current_tile
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and current_tile != None:
                current_tile.walkable = False

    screen.fill((255, 255, 255))
    pos_to_rect = {}

    for x in range(grid.grid_size_x):
        for y in range(grid.grid_size_y):
            rect = pygame.draw.rect(
                screen, (128, 128, 128), [x * scale, y * scale, scale, scale]
            )
            pos_to_rect[(x, y)] = rect

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
