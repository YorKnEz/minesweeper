import pygame

from constants import BOARD_FLAG, BOARD_FLAG_PLACED, BOARD_FLAG_REMOVED
from gui.counter import Counter
from state import GameState


class BombCounter(Counter):
    def __init__(self, bounds: pygame.Rect, state: GameState):
        super().__init__(bounds, state.max_bombs)

    def handle_event(self, event):
        """Event handler."""
        if event.type == BOARD_FLAG_PLACED:
            self.count -= 1
            self._update_text()
        elif event.type == BOARD_FLAG_REMOVED:
            self.count += 1
            self._update_text()
