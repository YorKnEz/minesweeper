import pygame
from constants import START_GAME
from gui import Input
from gui import Button
from gui.windows.window_base import WindowBase


class StartWindow(WindowBase):
    def __init__(self, width, height, font: pygame.font.Font, context):
        """Initializes the game window."""
        self.font = font
        self.context = context

        self.input = Input(pygame.Rect(0, 0, 100, 32), self.font, 3)
        self.button = Button(pygame.Rect(0, 32, 100, 32), "grey40", "Test", "white", self.font, START_GAME)


    def handle_event(self, event: pygame.event.Event) -> "WindowBase":
        """Event handler."""
        self.input.handle_event(event)
        self.button.handle_event(event)

        if event.type == START_GAME:
            return self.context.game_window

        return self

    def draw(self, screen: pygame.Surface):
        """Draw game on the screen."""
        self.input.draw(screen)
        self.button.draw(screen)
