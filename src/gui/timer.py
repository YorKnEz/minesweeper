import pygame

from constants import TIMER_TICK
from gui.counter import Counter
from state import GameState


class Timer(Counter):
    """Timer display component.

    This class extends the Counter class.

    Instance variables: see Counter class definition.

    Methods:
        - __init__: Construct a Timer instance.
        - overrides handle_event: Handle Timer-related events.
    """

    def __init__(self, bounds: pygame.Rect, state: GameState):
        """Initialize timer display.

        If the game doesn't use a timer, the timer is rendered as disabled.

        :param bounds: The bounds the timer will occupy on the screen.
        :param state: The game state.
        """
        super().__init__(bounds, state.time_left)

    def handle_event(self, event):
        """Event handler.

        It handles TIMER_TICK event.
        Unrecognized events are just ignored.

        :param event: The event to handle."""
        if event.type == TIMER_TICK:
            self.count -= 1
            self._update_text()
