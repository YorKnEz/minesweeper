import pygame

from gui.windows.game import GameWindow
from gui.windows.start import StartWindow
from gui.windows.window_base import WindowBase


class Window:
    """Window manager.

    It contains a variable that stores the current window. Events on the windows may cause switches to other windows.
    """

    def __init__(self, width, height, font):
        self.width, self.height, self.font = width, height, font

        # pre-initialize the window states
        self.start_window = StartWindow(width, height, font, self)
        self.game_window = GameWindow(width, height, font, self)

        self.current_window: WindowBase = self.start_window

    def handle_event(self, event: pygame.event.Event):
        """Event handler."""
        self.current_window = self.current_window.handle_event(event)

    def draw(self, screen: pygame.Surface):
        """Draw the window."""
        self.current_window.draw(screen)
