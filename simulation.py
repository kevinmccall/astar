import pygame
from kevstar2 import Grid
import sys

# Colors
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
BLANK_COLOR = (128, 128, 128)
PATH_COLOR = (0, 0, 255)
WALL_COLOR = (60, 60, 60)
BACKGROUND_COLOR = (255, 255, 255)
CELL_SIZE = 25


class Simulation:
    def __init__(self) -> None:
        pygame.init()
        self.grid = Grid(10, 10)
        self.walls = []
        self.path = []
        self.current_mode = "set_start"
        self.start_cell = pygame.Rect(0, 0, 0, 0)
        self.end_cell = pygame.Rect(0, 0, 0, 0)
        self.running = True
        self.calculated = False
        self.mouse_grid_pos = (0, 0)

        # drawing vars
        self.screen_size = (600, 600)
        self.scale = 32
        self.margin = 0
        self.x_offset = 0
        self.y_offset = 0

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
        self.screen.fill(BACKGROUND_COLOR)
        for rect in self.walls:
            pygame.draw.rect(self.screen, WALL_COLOR, rect)
        for rect in self.path:
            pygame.draw.rect(self.screen, PATH_COLOR, rect)
        pygame.draw.rect(self.screen, START_COLOR, self.start_cell)
        pygame.draw.rect(self.screen, END_COLOR, self.end_cell)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.logic()

    def logic(self):
        if not self.calculated:
            start_pos = self.get_rect_grid_pos(self.start_cell)
            end_pos = self.get_rect_grid_pos(self.end_cell)
            new_path = self.grid.a_star(start_pos, end_pos)
            self.path = []
            for cell in new_path:
                self.path.append(self.create_rect(cell))

    def create_rect(self, grid_pos):
        world_pos = self._grid_to_global(grid_pos)
        rect = pygame.Rect(world_pos, self.scale, self.scale)
        return rect

    def get_rect_grid_pos(self, rect):
        return self._global_to_grid((rect.left, rect.top))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_mode = "set_start"
                elif event.key == pygame.K_2:
                    current_mode = "set_end"
                elif event.key == pygame.K_3:
                    current_mode = "set_wall"
                elif event.key == pygame.K_4:
                    current_mode = "remove_wall"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    0 <= self.mouse_grid_pos[0] < self.grid.x_size
                    and 0 <= self.mouse_grid_pos[1] < self.grid.y_size
                ):
                    if current_mode == "set_start":
                        self.start_cell = self.create_rect(self.mouse_grid_pos)
                    elif current_mode == "set_end":
                        self.end_cell = self.create_rect(self.mouse_grid_pos)
                    elif current_mode == "set_wall":
                        self.walls.append(self.create_rect(self.mouse_grid_pos))
                    elif current_mode == "remove_wall":
                        for wall in self.walls:
                            if (wall.left, wall.right) == self.mouse_grid_pos:
                                self.walls.remove(wall)
                                break


def main():
    sim = Simulation()
    sim.run()
