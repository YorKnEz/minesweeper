from copy import deepcopy

import pygame

from constants import (BOARD_DOWN, BOARD_FLAG, BOARD_LEFT, BOARD_REVEAL,
                       BOARD_RIGHT, BOARD_UP, MOUSEBUTTONLEFT,
                       MOUSEBUTTONRIGHT)
from state import BoardCell, GameState
from theme import Theme
from utils import clamp, draw_border


class Board:
    """Class for managing the board display of the game.

    It can display a board of any size, even if it doesn't fit the screen.
    """
    # default border width
    BORDER_WIDTH = 2
    # default cell size
    CELL_SIZE = 32
    # map board move events to directions
    BOARD_SHIFT = {
        pygame.K_LEFT: (-1, 0),
        pygame.K_UP: (0, -1),
        pygame.K_RIGHT: (1, 0),
        pygame.K_DOWN: (0, 1),
        BOARD_LEFT: (-1, 0),
        BOARD_UP: (0, -1),
        BOARD_RIGHT: (1, 0),
        BOARD_DOWN: (0, 1),
    }

    def __init__(self, bounds: pygame.Rect, state: GameState, font: pygame.font.Font):
        """Init the board based on the current state of the game."""
        self.bounds = bounds.copy()
        self.font = font

        # build surface to draw the game on
        self.height, self.width = state.size
        self.board = deepcopy(state.board)

        self.surface = pygame.Surface((self.width * Board.CELL_SIZE, self.height * Board.CELL_SIZE))

        # used for drawing only part of the surface
        self.surface_area = self.surface.get_rect()
        self.surface_area.size = self.bounds.size
        self.surface_bounds = self.surface.get_rect()

        self.__update_surface()

    def __get_click_pos(self, mouse_x, mouse_y):
        """Return cell coordinates of clicked cell."""
        # normalize mouse coords to surface coords
        mouse_x += self.surface_area.left - self.bounds.left
        mouse_y += self.surface_area.top - self.bounds.top
        return mouse_y // Board.CELL_SIZE, mouse_x // Board.CELL_SIZE

    def __cell_to_text(self, cell):
        """Converts a cell value to a text element to be rendered."""
        if cell == BoardCell.BOMB.value or cell == BoardCell.BOMB_REVEALED.value:
            text = "*"
            color = "black"
        elif cell == BoardCell.FLAGGED.value:
            text = "`"
            color = "red"
        else:
            text = str(cell)
            color = Theme.CELL_COLORS[(cell - 1) % len(Theme.CELL_COLORS)]

        return self.font.render(text, True, color)

    def __update_surface(self):
        """Create a surface on which the whole board is drawn.

        Borders are drawn over the cells, so they don't take space.
        A board of size `n x m` will have `w = Board.CELL_SIZE * n`, `h = Board.CELL_SIZE * m` pixels.
        """
        self.surface.fill(Theme.REVEALED_BG_COLOR)

        # draw cells' backgrounds
        for i in range(self.height):
            for j in range(self.width):
                # skip cells that don't need a different background
                if self.board[i][j] != BoardCell.BOMB_REVEALED.value and self.board[i][j] != BoardCell.BOMB.value:
                    continue

                cell_bounds = pygame.rect.Rect(
                    self.surface_bounds.left + j * Board.CELL_SIZE,
                    self.surface_bounds.top + i * Board.CELL_SIZE,
                    Board.CELL_SIZE,
                    Board.CELL_SIZE,
                )

                # draw revealed bomb in red background
                if self.board[i][j] == BoardCell.BOMB_REVEALED.value:
                    pygame.draw.rect(self.surface, Theme.REVEALED_BOMB_BG_COLOR, cell_bounds)
                # draw regular bombs in darker background
                elif self.board[i][j] == BoardCell.BOMB.value:
                    pygame.draw.rect(self.surface, Theme.UNREVEALED_BG_COLOR, cell_bounds)

                text = self.__cell_to_text(self.board[i][j])
                rect = text.get_rect()
                rect.center = cell_bounds.center
                self.surface.blit(text, rect)

        # draw vertical borders over top and left of cells
        for j in range(self.width):
            pygame.draw.line(
                self.surface,
                Theme.BG_COLOR,
                (self.surface_bounds.left + j * Board.CELL_SIZE, self.surface_bounds.top),
                (self.surface_bounds.left + j * Board.CELL_SIZE, self.surface_bounds.bottom),
                Board.BORDER_WIDTH,
            )

        # draw horizontal borders over top and left of cells
        for i in range(self.height):
            pygame.draw.line(
                self.surface,
                Theme.BG_COLOR,
                (self.surface_bounds.left, self.surface_bounds.top + i * Board.CELL_SIZE),
                (self.surface_bounds.right, self.surface_bounds.top + i * Board.CELL_SIZE),
                Board.BORDER_WIDTH,
            )

        # draw cells
        for i in range(self.height):
            for j in range(self.width):
                # skip values of 0, their cells should be left as is
                if self.board[i][j] == 0:
                    continue

                cell_bounds = pygame.rect.Rect(
                    self.surface_bounds.left + j * Board.CELL_SIZE,
                    self.surface_bounds.top + i * Board.CELL_SIZE,
                    Board.CELL_SIZE,
                    Board.CELL_SIZE,
                )

                # for unselected or flagged values (including bombs after the game is lost), draw them in a darker tone
                if self.board[i][j] == BoardCell.UNSELECTED.value:
                    pygame.draw.rect(self.surface, Theme.UNREVEALED_BG_COLOR, cell_bounds)
                    draw_border(
                        self.surface,
                        cell_bounds,
                        pygame.Color(Theme.UNREVEALED_BG_COLOR),
                        width=4,
                        depth="up",
                        inner=True,
                    )
                    # if the value was unselected, we can stop here
                    continue
                elif self.board[i][j] == BoardCell.FLAGGED.value:
                    pygame.draw.rect(self.surface, Theme.UNREVEALED_BG_COLOR, cell_bounds)
                    draw_border(
                        self.surface,
                        cell_bounds,
                        pygame.Color(Theme.UNREVEALED_BG_COLOR),
                        width=4,
                        depth="up",
                        inner=True,
                    )

                text = self.__cell_to_text(self.board[i][j])
                rect = text.get_rect()
                rect.center = cell_bounds.center
                self.surface.blit(text, rect)

    def __shift_board(self, direction, offset=2):
        """Move the board view by a given offset in a specified direction.

        If the movement causes the board to get outside the bounds of its surface area,
        the move will be clamped.
        """
        off_x, off_y = direction
        off_x *= offset * Board.CELL_SIZE
        off_y *= offset * Board.CELL_SIZE

        self.surface_area.x = clamp(self.surface_area.x + off_x, 0, self.surface_bounds.width - self.bounds.width)
        self.surface_area.y = clamp(self.surface_area.y + off_y, 0, self.surface_bounds.height - self.bounds.height)

    def handle_event(self, event):
        """Event handler."""
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            # ignore click if it's not on the board
            if not self.bounds.collidepoint(mouse_pos):
                return

            l, c = self.__get_click_pos(*mouse_pos)

            if event.button == MOUSEBUTTONLEFT:
                pygame.event.post(pygame.event.Event(BOARD_REVEAL, l=l, c=c))
            elif event.button == MOUSEBUTTONRIGHT:
                pygame.event.post(pygame.event.Event(BOARD_FLAG, l=l, c=c))
        elif event.type == pygame.KEYUP and event.key in Board.BOARD_SHIFT.keys():
            # move board by 2 cells in the specified direction if user pressed arrow keys
            self.__shift_board(Board.BOARD_SHIFT[event.key])
        elif event.type in Board.BOARD_SHIFT.keys():
            # move board by 2 cells if the move event has been fired
            self.__shift_board(Board.BOARD_SHIFT[event.type])

    def update(self, state: GameState):
        """Update the board with the given state."""
        self.height, self.width = state.size
        self.board = deepcopy(state.board)

        self.__update_surface()

    def draw(self, surface: pygame.Surface):
        """Draw the board onto the screen in the area given by `self.bounds`."""
        surface.blit(self.surface, self.bounds.topleft, self.surface_area)
        draw_border(surface, self.bounds, pygame.Color(Theme.BG_COLOR), width=8, depth="down", inner=False)
