import pygame

from constants import BOARD_FLAG
from gui.counter import Counter
from state import GameState


class BombCounter(Counter):
    def __init__(self, bounds: pygame.Rect, state: GameState):
        super().__init__(bounds, state.max_bombs)

    def handle_event(self, event):
        if event.type == BOARD_FLAG:
            self.count -= 1
            self._update_text()
