import pygame
from kevstar2 import Grid
import sys

# Colors
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
BLANK_COLOR = (128, 128, 128)
PATH_COLOR = (0, 0, 255)
WALL_COLOR = (60, 60, 60)
BACKGROUND_COLOR = pygame.Color("#2F3C7E")
GRID_BACKROUND_COLOR = pygame.Color("#FBEAEB")
CELL_SIZE = 25
INVALID_CELL_RECT = pygame.Rect(-1, -1, 0, 0)




class Simulation:
    def __init__(self) -> None:
        # drawing vars
        self.screen_size = (600, 600)
        self.scale = 32
        self.margin = 0
        self.x_offset = 0
        self.y_offset = 0

        self.grid = Grid(10, 10)
        self.walls = set()
        self.path = []
        self.current_mode = "set_start"
        self.start_cell = None
        self.end_cell = None
        self.running = True
        self.calculated = False
        self.mouse_grid_pos = (0, 0)


        self.screen = pygame.display.set_mode(self.screen_size)

    def _global_to_grid(self, position):
        x, y = position
        local_x = (x - self.x_offset) // (self.scale + self.margin)
        local_y = (y - self.y_offset) // (self.scale + self.margin)
        return (local_x, local_y)

    def _grid_to_global(self, position):
        x, y = position
        global_x = x * (self.scale + self.margin) + self.x_offset
        global_y = y * (self.scale + self.margin) + self.y_offset
        return (global_x, global_y)

    def draw(self):
        grid_rect = pygame.Rect(0,0, self.grid.x_size * self.scale, self.grid.y_size * self.scale)
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, GRID_BACKROUND_COLOR, grid_rect)
        for cell in self.walls:
            self.draw_cell(cell, WALL_COLOR)
        for cell in self.path:
            self.draw_cell(cell, PATH_COLOR)
        
        self.draw_cell(self.start_cell, START_COLOR)
        self.draw_cell(self.end_cell, END_COLOR)

        pygame.display.flip()

    def run(self):
        pygame.init()
        while self.running:
            self.handle_events()
            self.logic()
            if not self.calculated:
                print("drawing")
                self.draw()
                self.calculated = True

    def logic(self):
        if not self.calculated and self.start_cell is not None and self.end_cell is not None:
            new_path = self.grid.a_star(self.start_cell, self.end_cell)
            self.path = []
            for cell in new_path:
                self.path.append(cell)

    def create_rect(self, grid_pos):
        world_pos = self._grid_to_global(grid_pos)
        rect = pygame.Rect(world_pos, (self.scale, self.scale))
        return rect

    def draw_cell(self, cell_pos, color):
        if cell_pos is None:
            return
        rect = pygame.Rect(self._grid_to_global(cell_pos), (self.scale, self.scale))
        pygame.draw.rect(self.screen, color, rect)

    def delete_at_pos(self, grid_pos):
        if grid_pos == self.start_cell:
            self.start_cell = None
            self.path = []
            self.calculated = False
        elif grid_pos == self.end_cell:
            self.end_cell = None
            self.path = []
            self.calculated = False
        else:
            for wall in self.walls:
                if wall == self.mouse_grid_pos:
                    self.walls.remove(wall)
                    self.grid.remove_unwalkable_cell(wall)
                    break

    def get_rect_world_pos(self, rect : pygame.Rect):
        return rect.left, rect.top

    def handle_events(self):
        self.mouse_grid_pos = self._global_to_grid(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.current_mode = "set_start"
                elif event.key == pygame.K_2:
                    self.current_mode = "set_end"
                elif event.key == pygame.K_3:
                    self.current_mode = "set_wall"
                elif event.key == pygame.K_4:
                    self.current_mode = "remove_wall"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    0 <= self.mouse_grid_pos[0] < self.grid.x_size
                    and 0 <= self.mouse_grid_pos[1] < self.grid.y_size
                ):
                    if self.current_mode == "set_start":
                        self.start_cell = self.mouse_grid_pos
                    elif self.current_mode == "set_end":
                        self.end_cell = self.mouse_grid_pos
                    elif self.current_mode == "set_wall":
                        self.walls.add(self.mouse_grid_pos)
                        self.grid.add_unwalkable_cell(self.mouse_grid_pos)
                    elif self.current_mode == "remove_wall":
                        self.delete_at_pos(self.mouse_grid_pos)
                    self.calculated = False


def main():
    sim = Simulation()
    sim.run()

if __name__ == '__main__':
    main()