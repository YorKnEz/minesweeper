import pygame

from constants import (BOARD_FLAG, BOARD_REVEAL, GAME_OVER, GAME_RESTART,
                       TIMER_TICK)
from gui import Board, BombCounter, Timer
from gui.button import Button
from gui.windows.window_base import WindowBase
from state import GameState
from theme import Theme
from utils import draw_border


class GameWindow(WindowBase):
    def __init__(self, width, height, font: pygame.font.Font, context):
        """Initializes the game window."""
        self.width, self.height = width, height
        self.font = font
        self.context = context

        self.enter()

    def enter(self):
        # init the game using context params
        self.state = GameState(
            size=(self.context.x, self.context.y),
            max_bombs=self.context.bombs,
            time=self.context.time,
        )

        board_bounds = pygame.Rect((self.width - 512) / 2, 64 + (self.height - 512) / 2, 512, 512)
        self.board = Board(board_bounds, self.state, self.font)

        timer_bounds = pygame.Rect(board_bounds.left, board_bounds.top - 96, 100, 64)
        self.timer = Timer(timer_bounds, self.state)

        bomb_cnt_bounds = pygame.Rect(board_bounds.right - 100, board_bounds.top - 96, 100, 64)
        self.bomb_cnt = BombCounter(bomb_cnt_bounds, self.state)

        restart_button_bounds = pygame.Rect((self.width - 64) / 2, board_bounds.top - 96, 64, 64)
        self.restart_button = Button(
            restart_button_bounds, Theme.BG_COLOR, "", Theme.TEXT_COLOR, self.font, GAME_RESTART
        )

    def handle_event(self, event: pygame.event.Event):
        """Event handler."""
        self.board.handle_event(event)
        self.timer.handle_event(event)
        self.bomb_cnt.handle_event(event)
        self.restart_button.handle_event(event)

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
            pass
        elif event.type == GAME_RESTART:
            # restart game
            self.context.set_window(self.context.game_window)

    def draw(self, screen: pygame.Surface):
        """Draw game on the screen."""
        self.board.draw(screen)
        self.timer.draw(screen)
        self.restart_button.draw(screen)
        self.bomb_cnt.draw(screen)

        draw_border(screen, screen.get_rect(), pygame.Color(Theme.BG_COLOR), width=8, depth="up", inner=True)
