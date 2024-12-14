import pygame

from constants import (BOARD_DOWN, BOARD_FLAG, BOARD_LEFT, BOARD_REVEAL,
                       BOARD_RIGHT, BOARD_UP, GAME_HOME, GAME_OVER, GAME_RESTART,
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
        super().__init__()
        self.home_icon_pos = None
        self.home_icon = None
        self.home_button = None
        self.controls_icons_pos = None
        self.controls_icons = None
        self.controls = None
        self.restart_icon_pos = None
        self.restart_icon = None
        self.win_icon = None
        self.lose_icon = None
        self.reset_icon = None
        self.restart_button = None
        self.bomb_cnt = None
        self.timer = None
        self.board = None
        self.state = None
        self.width, self.height = width, height
        self.font = font
        self.context = context

        self.enter()

    def enter(self):
        """Reinitialize the game window.

        Upon entering this window again, the state must be restarted and the UI elements redrawn, in order to reflect
        the new state of the game."""
        # init the game using context params
        self.state = GameState(
            size=(self.context.x, self.context.y),
            max_bombs=self.context.bombs,
            time=self.context.time,
        )

        board_bounds = pygame.Rect((self.width - 512) / 2, (self.height - 512) / 2, 512, 512)
        self.board = Board(board_bounds, self.state, self.font)

        timer_bounds = pygame.Rect(board_bounds.left, board_bounds.top - 96, 100, 64)
        self.timer = Timer(timer_bounds, self.state)

        bomb_cnt_bounds = pygame.Rect(board_bounds.right - 100, board_bounds.top - 96, 100, 64)
        self.bomb_cnt = BombCounter(bomb_cnt_bounds, self.state)

        restart_button_bounds = pygame.Rect((self.width - 64) / 2, board_bounds.top - 96, 64, 64)
        self.restart_button = Button(
            restart_button_bounds, Theme.BG_COLOR, "", Theme.TEXT_COLOR, self.font, GAME_RESTART
        )

        self.reset_icon = pygame.transform.scale(pygame.image.load("assets/reset.png").convert_alpha(), (48, 48))
        self.lose_icon = pygame.transform.scale(pygame.image.load("assets/lose.png").convert_alpha(), (48, 48))
        self.win_icon = pygame.transform.scale(pygame.image.load("assets/win.png").convert_alpha(), (48, 48))
        self.restart_icon = self.reset_icon
        self.restart_icon_pos = (restart_button_bounds.x + 8, restart_button_bounds.y + 8)

        pos = [
            (board_bounds.left, board_bounds.bottom + 32),
            (board_bounds.left + 64 + 16, board_bounds.bottom + 32),
            (board_bounds.right - 2 * 64 - 16, board_bounds.bottom + 32),
            (board_bounds.right - 64, board_bounds.bottom + 32),
        ]
        dirs = [("up", BOARD_UP), ("down", BOARD_DOWN), ("left", BOARD_LEFT), ("right", BOARD_RIGHT)]

        self.controls = []
        self.controls_icons = []
        self.controls_icons_pos = []

        for (x, y), (d, ev) in zip(pos, dirs):
            button = Button(pygame.Rect(x, y, 64, 64), Theme.BG_COLOR, "", Theme.TEXT_COLOR, self.font, ev)

            self.controls.append(button)
            self.controls_icons.append(
                pygame.transform.scale(pygame.image.load(f"assets/{d}.png").convert_alpha(), (48, 48))
            )
            self.controls_icons_pos.append((button.bounds.x + 8, button.bounds.y + 8))

        home_button_bounds = pygame.Rect((self.width - 64) / 2, board_bounds.bottom + 32, 64, 64)
        self.home_button = Button(
            home_button_bounds, Theme.BG_COLOR, "", Theme.TEXT_COLOR, self.font, GAME_HOME
        )
        self.home_icon = pygame.transform.scale(pygame.image.load("assets/home.png").convert_alpha(), (48, 48))
        self.home_icon_pos = (home_button_bounds.x + 8, home_button_bounds.y + 8)

    def handle_event(self, event: pygame.event.Event):
        """Event handler."""
        self.board.handle_event(event)
        self.timer.handle_event(event)
        self.bomb_cnt.handle_event(event)
        self.restart_button.handle_event(event)
        self.home_button.handle_event(event)

        for button in self.controls:
            button.handle_event(event)

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
            if self.state.is_win():
                self.restart_icon = self.win_icon
            else:
                self.restart_icon = self.lose_icon
        elif event.type == GAME_RESTART:
            # restart game
            self.context.set_window(self.context.game_window)
        elif event.type == GAME_HOME:
            # go to the home window
            self.context.set_window(self.context.start_window)

    def draw(self, screen: pygame.Surface):
        """Draw game on the screen."""
        self.board.draw(screen)
        self.timer.draw(screen)
        self.bomb_cnt.draw(screen)

        self.restart_button.draw(screen)
        screen.blit(self.restart_icon, self.restart_icon_pos)

        self.home_button.draw(screen)
        screen.blit(self.home_icon, self.home_icon_pos)

        for c, i, p in zip(self.controls, self.controls_icons, self.controls_icons_pos):
            c.draw(screen)
            draw_border(screen, c.bounds, pygame.Color(Theme.BG_COLOR), width=8, depth="up", inner=False)
            screen.blit(i, p)

        draw_border(screen, screen.get_rect(), pygame.Color(Theme.BG_COLOR), width=8, depth="up", inner=True)
