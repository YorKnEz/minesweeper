import pygame

from constants import BOARD_FLAG_PLACED, BOARD_FLAG_REMOVED
from gui.counter import Counter
from state import GameState


class BombCounter(Counter):
    """Bomb count display component.

    This class extends the Counter class.

    Instance variables: see Counter class definition.

    Methods:
        - __init__: Construct a Timer instance.
        - overrides handle_event: Handle BombCounter-related events.
    """

    def __init__(self, bounds: pygame.Rect, state: GameState):
        """Initialize bomb display.

        :param bounds: The bounds the timer will occupy on the screen.
        :param state: The game state.
        """
        super().__init__(bounds, state.max_bombs)

    def handle_event(self, event):
        """Event handler.

        It handles BOARD_FLAG_PLACED and BOARD_FLAG_REMOVED events.
        Unrecognized events are just ignored.

        :param event: The event to handle."""
        if event.type == BOARD_FLAG_PLACED:
            self.count -= 1
            self._update_text()
        elif event.type == BOARD_FLAG_REMOVED:
            self.count += 1
            self._update_text()
