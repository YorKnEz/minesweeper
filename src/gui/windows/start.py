import pygame
from constants import GAME_START
from gui import Input
from gui import Button
from gui.windows.window_base import WindowBase
from theme import Theme
from utils import draw_border


class StartWindow(WindowBase):
    def __init__(self, width, height, font: pygame.font.Font, context):
        """Initializes the game window."""
        self.font = font
        self.context = context

        input_bounds = pygame.Rect(0, 0, 200, 32)
        input_bounds.center = (width / 2, height / 2 - 80)
        self.input = Input(input_bounds, self.font, 3)

        button_bounds = pygame.Rect(0, 0, 200, 64)
        button_bounds.center = (width / 2, height / 2)
        self.button = Button(button_bounds, Theme.BG_COLOR, "Start game", Theme.TEXT_COLOR, self.font, GAME_START)

    def handle_event(self, event: pygame.event.Event) -> "WindowBase":
        """Event handler."""
        self.input.handle_event(event)
        self.button.handle_event(event)

        if event.type == GAME_START:
            return self.context.game_window

        return self

    def draw(self, screen: pygame.Surface):
        """Draw game on the screen."""
        self.input.draw(screen)
        self.button.draw(screen)

        draw_border(screen, screen.get_rect(), pygame.Color(Theme.BG_COLOR), width=8, depth="up", inner=True)
