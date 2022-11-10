import pygame


class Button:
    def __init__(self, screen, color, pos, size, text="") -> None:
        super().__init__()
        self.color = color
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.text = text
        self.screen = screen
        self.draw()

    def draw(self):
        pygame.draw.rect(
            self.screen, self.color, [self.pos_x, self.pos_y, self.width, self.height]
        )

        if self.text != "":
            font = pygame.font.SysFont("comicsans", 12)
            text = font.render(self.text, True, (0, 0, 0))
            self.screen.blit(
                text,
                (
                    self.pos_x + (self.width / 2 - text.get_width() / 2),
                    self.pos_x + (self.width / 2 - text.get_width() / 2),
                ),
            )

    def is_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (
            self.pos_x < mouse_x < self.pos_x + self.width
            and self.pos_y < mouse_y < self.pos_y + self.height
        )
