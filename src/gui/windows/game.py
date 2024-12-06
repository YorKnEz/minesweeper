import pygame

from constants import BOARD_FLAG, BOARD_REVEAL, GAME_OVER, TIMER_TICK
from gui import Board, BombCounter, Timer
from gui.windows.window_base import WindowBase
from state import GameState
from theme import Theme
from utils import draw_border


class GameWindow(WindowBase):
    def __init__(self, width, height, font: pygame.font.Font, context):
        """Initializes the game window."""
        self.font = font
        self.context = context

        self.state = GameState(size=(16, 16), max_bombs=32, time=10)

        board_bounds = pygame.Rect((width - 512) / 2, 64 + (height - 512) / 2, 512, 512)
        self.board = Board(board_bounds, self.state, self.font)

        timer_bounds = pygame.Rect(board_bounds.left, board_bounds.top - 96, 100, 64)
        self.timer = Timer(timer_bounds, self.state)

        bomb_cnt_bounds = pygame.Rect(board_bounds.right - 100, board_bounds.top - 96, 100, 64)
        self.bomb_cnt = BombCounter(bomb_cnt_bounds, self.state)

    def handle_event(self, event: pygame.event.Event) -> "WindowBase":
        """Event handler."""
        if event.type == BOARD_REVEAL:
            l, c = event.dict.values()
            self.state = self.state.reveal_zone(l, c)
            self.board.update(self.state)
        elif event.type == BOARD_FLAG:
            l, c = event.dict.values()
            self.state = self.state.flag_zone(l, c)
            self.board.update(self.state)
        elif event.type == TIMER_TICK:
            self.state = self.state.timer_ticked()
        elif event.type == GAME_OVER:
            return self.context.start_window

        self.board.handle_event(event)
        self.timer.handle_event(event)
        self.bomb_cnt.handle_event(event)

        return self

    def draw(self, screen: pygame.Surface):
        """Draw game on the screen."""
        self.board.draw(screen)
        self.timer.draw(screen)
        self.bomb_cnt.draw(screen)

        draw_border(screen, screen.get_rect(), pygame.Color(Theme.BG_COLOR), width=8, depth="up", inner=True)
