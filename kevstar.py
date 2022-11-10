import sys
import pygame
from button import Button


class Tile:
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.gcost = None
        self.hcost = None
        self.fcost = None
        self.previous = None
        self.walkable = True

    def get_pos(self):
        return (self.x, self.y)

    def set_fcost(self, gcost, hcost):
        self.gcost = gcost
        self.hcost = hcost
        self.fcost = gcost + hcost

    def set_previous(self, tile):
        self.previous = tile

    def get_previous(self):
        return self.previous


class Grid:
    def __init__(self, grid_x, grid_y) -> None:
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tiles = []
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                self.tiles.append(Tile(x, y))

    def get_tile(self, x, y):
        for tile in self.tiles:
            if tile.get_pos() == (x, y):
                return tile
        else:
            return None

    def get_neighbors(self, tile):
        neighbors = []
        directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (-1, -1),
            (1, -1),
            (-1, 1),
            (1, 1),
        ]
        if tile != None:
            tx, ty = tile.get_pos()
            for dir in directions:
                neighbor_x, neighbor_y = tx + dir[0], ty + dir[1]
                neighbor = self.get_tile(neighbor_x, neighbor_y)
                if neighbor != None:
                    neighbors.append(neighbor)
            return neighbors
        else:
            print("non real tile")

    def get_dist(self, tile_a, tile_b):
        diff_x, diff_y = abs(tile_a.get_pos()[0] - tile_b.get_pos()[0]), abs(
            tile_a.get_pos()[1] - tile_b.get_pos()[1]
        )
        if diff_x > diff_y:
            return diff_y * 14 + (diff_x - diff_y) * 10
        else:
            return diff_x * 14 + (diff_y - diff_x) * 10

    def astar(self, start, end):
        need_evaluation = []
        exhausted = []
        found = False
        tiles = []

        exhausted.append(start)
        for t in self.tiles:
            t.fcost = None
            t.gcost = None
            t.hcost = None
        start.set_fcost(0, self.get_dist(start, end))
        need_evaluation.append(start)

        def evalutate(tile):
            exhausted.append(tile)
            for n in self.get_neighbors(tile):
                if n not in exhausted and n.walkable:
                    gcost = self.get_dist(n, tile) + tile.gcost
                    hcost = self.get_dist(tile, end)
                    fcost = gcost + hcost
                    if n.fcost == None or fcost < n.fcost and n not in exhausted:
                        n.set_fcost(gcost, hcost)
                        n.set_previous(tile)
                        need_evaluation.append(n)
            if tile.get_pos() == end.get_pos():
                return True

        def get_sort_value(e):
            return e.fcost

        while True:
            need_evaluation.sort(key=get_sort_value)
            curr_tile = need_evaluation.pop(0)

            found = evalutate(curr_tile)
            if found:
                prev_tile = curr_tile.get_previous()
                while prev_tile != None:
                    tiles.insert(0, prev_tile)
                    prev_tile = prev_tile.get_previous()
                return tiles


def main():
    # Colors
    START_COLOR = (0, 255, 0)
    END_COLOR = (255, 0, 0)
    BLANK_COLOR = (128, 128, 128)
    PATH_COLOR = (0, 0, 255)
    WALL_COLOR = (60, 60, 60)
    BACKGROUND_COLOR = (255, 255, 255)

    # Initialization
    pygame.init()
    grid = Grid(10, 10)
    walls = []
    path = []
    drawn_tiles = _create_2d_list(grid.grid_x, grid.grid_y)
    current_mode = None
    start_tile = None
    end_tile = None
    running = True
    calculated = False

    # drawing vars
    screen_size = (600, 600)
    scale = 32
    margin = 5
    x_offset = 100
    y_offset = 0

    screen = pygame.display.set_mode(screen_size)

    def _global_to_grid(position):
        x, y = position
        local_x = (x - x_offset) // (scale + margin)
        local_y = (y - y_offset) // (scale + margin)
        return (local_x, local_y)

    def _grid_to_global(position):
        x, y = position
        global_x = x * (scale + margin) + x_offset
        global_y = y * (scale + margin) + y_offset
        return (global_x, global_y)

    while running:

        screen.fill(BACKGROUND_COLOR)

        mouse_grid_pos = _global_to_grid(pygame.mouse.get_pos())
        start_button = Button(screen, END_COLOR, (20, 20), (60, 20), "start")
        end_button = Button(screen, END_COLOR, (20, 60), (60, 20), "end")
        wall_button = Button(screen, END_COLOR, (20, 100), (60, 20), "walls")
        delete_wall_button = Button(
            screen, END_COLOR, (20, 140), (60, 20), "delete_walls"
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_hovered():
                    current_mode = "set_start"
                elif end_button.is_hovered():
                    current_mode = "set_end"
                elif wall_button.is_hovered():
                    current_mode = "set_wall"
                elif delete_wall_button.is_hovered():
                    current_mode = "remove_wall"

                if (
                    0 <= mouse_grid_pos[0] < grid.grid_x
                    and 0 <= mouse_grid_pos[1] < grid.grid_y
                ):
                    tile = grid.get_tile(mouse_grid_pos[0], mouse_grid_pos[1])
                    calculated = False
                    if current_mode == "set_start":
                        start_tile = tile
                    elif current_mode == "set_end":
                        end_tile = tile
                    elif current_mode == "set_wall":
                        if tile not in walls:
                            walls.append(tile)
                            tile.walkable = False
                    elif current_mode == "remove_wall":
                        if tile in walls:
                            walls.remove(tile)
                            tile.walkable = True

        if start_tile != None and end_tile != None and not calculated:
            calculated = True
            path = grid.astar(start_tile, end_tile)

        for tx in range(grid.grid_x):
            for ty in range(grid.grid_y):
                global_pos = _grid_to_global((tx, ty))
                tile_color = BLANK_COLOR
                tile = grid.get_tile(tx, ty)
                if tile == start_tile:
                    tile_color = START_COLOR
                elif tile == end_tile:
                    tile_color = END_COLOR
                elif tile in walls:
                    tile_color = WALL_COLOR
                elif tile in path:
                    tile_color = PATH_COLOR

                drawn_tiles[tx][ty] = pygame.draw.rect(
                    screen, tile_color, [global_pos[0], global_pos[1], scale, scale]
                )
        pygame.display.flip()


def _create_2d_list(sx, sy):
    rows = []
    for x in range(sx):
        column = []
        for y in range(sy):
            column.append(0)
        rows.append(column)
    return rows

if __name__ == "__main__":
    main()
