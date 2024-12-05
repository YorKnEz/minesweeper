import pygame

from constants import TIMER_TICK
from gui.counter import Counter
from state import GameState


class Timer(Counter):
    def __init__(self, bounds: pygame.Rect, state: GameState):
        super().__init__(bounds, state.time_left)

    def handle_event(self, event):
        if event.type == TIMER_TICK:
            self.count -= 1
            self._update_text()
