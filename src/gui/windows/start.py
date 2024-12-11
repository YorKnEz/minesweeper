import pygame

from constants import GAME_START
from gui import Button, Input
from gui.windows.window_base import WindowBase
from theme import Theme
from utils import draw_border


class StartWindow(WindowBase):
    def __init__(self, width, height, font: pygame.font.Font, context):
        """Initializes the game window."""
        self.font = font
        self.context = context

        comp_width = 200
        input_height = 32
        button_height = 64
        border_width = 8
        padding = 16

        x = (width - comp_width) / 2
        y = (height - 3 * input_height - border_width * 6 - button_height - border_width * 2 - 3 * padding) / 2

        self.lines_input = Input(pygame.Rect(x, y, 80, input_height), self.font, max_length=3, placeholder="X")
        self.cols_input = Input(
            pygame.Rect(x + comp_width - 80, y, 80, input_height), self.font, max_length=3, placeholder="Y"
        )
        y += input_height + 2 * border_width + padding
        self.time_input = Input(
            pygame.Rect(x, y, comp_width, input_height), self.font, max_length=3, placeholder="Time"
        )
        y += input_height + 2 * border_width + padding
        self.bombs_input = Input(
            pygame.Rect(x, y, comp_width, input_height), self.font, max_length=10, placeholder="Bombs"
        )
        y += input_height + 2 * border_width + padding

        self.inputs = [self.lines_input, self.cols_input, self.time_input, self.bombs_input]

        self.button = Button(
            pygame.Rect(x, y, comp_width, button_height),
            Theme.BG_COLOR,
            "Start game",
            Theme.TEXT_COLOR,
            self.font,
            GAME_START,
        )

    def enter(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        """Event handler."""
        for input in self.inputs:
            input.handle_event(event)
        self.button.handle_event(event)

        if event.type == GAME_START:
            # update params using data from the inputs
            self.context.set_params(
                self.lines_input.text,
                self.cols_input.text,
                self.time_input.text,
                self.bombs_input.text,
            )
            # start game
            self.context.set_window(self.context.game_window)
            return

    def draw(self, screen: pygame.Surface):
        """Draw window on the screen."""
        for input in self.inputs:
            input.draw(screen)

        self.button.draw(screen)

        draw_border(screen, screen.get_rect(), pygame.Color(Theme.BG_COLOR), width=8, depth="up", inner=True)
