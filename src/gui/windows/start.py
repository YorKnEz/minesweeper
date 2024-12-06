import pygame
from gui import Input
from gui.windows.window_base import WindowBase


class StartWindow(WindowBase):
    def __init__(self, width, height, font: pygame.font.Font, context):
        """Initializes the game window."""
        self.font = font
        self.context = context

        self.input = Input(pygame.Rect(0, 0, 100, 32), self.font, 3)

    def handle_event(self, event: pygame.event.Event) -> "WindowBase":
        """Event handler."""
        self.input.handle_event(event)

        return self

    def draw(self, screen: pygame.Surface):
        """Draw game on the screen."""
        self.input.draw(screen)
