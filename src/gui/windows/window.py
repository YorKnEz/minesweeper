import pygame

from gui.windows.game import GameWindow
from gui.windows.start import StartWindow
from gui.windows.window_base import WindowBase


class Window:
    """Window manager.

    It contains a variable that stores the current window. Events on the windows may cause switches to other windows.
    """

    def __init__(self, width, height, font):
        self.current_window = None
        self.width, self.height, self.font = width, height, font

        # default params for game
        self.x, self.y, self.time, self.bombs = 16, 16, 0, 32

        # pre-initialize the window states
        self.start_window = StartWindow(width, height, font, self)
        self.game_window = GameWindow(width, height, font, self)

        self.set_window(self.start_window)

    def set_window(self, window: WindowBase):
        """Change the current window of the Window Manager.

        Upon calling this method, the `enter` method of the window is called.
        """
        self.current_window: WindowBase = window
        self.current_window.enter()

    def set_params(self, x, y, time, bombs):
        """Set the parameters of the game.

        The provided params are all strings which are parsed and interpreted by this method.
        In case any of the values are invalid, the method automatically sets a favorable default.
        """
        # cap x and y to 4 on the lower end
        self.x = max(4, int(x) if len(x) > 0 else 16)
        self.y = max(4, int(y) if len(y) > 0 else 16)
        self.time = int(time) if len(time) > 0 else 0
        # bombs should be at most 999, the max displayable number
        # the default value is xy / 8
        # bombs = int(bombs) if len(bombs) > 0 else 999
        self.bombs = min(
            999,
            self.x * self.y - 9,
            int(bombs if len(bombs) > 0 else (self.x * self.y) / 8),
        )
        print(self.bombs)

    def handle_event(self, event: pygame.event.Event):
        """Event handler."""
        self.current_window.handle_event(event)

    def draw(self, screen: pygame.Surface):
        """Draw the window."""
        self.current_window.draw(screen)
