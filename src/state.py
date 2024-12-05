import random
from copy import deepcopy
from enum import Enum

import pygame

from constants import BOARD_FLAG_PLACED, BOARD_FLAG_REMOVED, TIMER_TICK


class BoardCell(Enum):
    BOMB_REVEALED = 17
    BOMB = 16
    UNSELECTED = -1
    FLAGGED = -2


class GameState:
    def __init__(self, *, size: tuple[int, int] = (16, 16), max_bombs=64, time=0):
        """
        Initialize game state.
        """
        self.height, self.width = self.size = size

        # board with all bombs and all cells marked with their score
        self.zones = [[0 for _ in range(self.width)] for _ in range(self.height)]

        self.max_bombs = max_bombs
        bombs = max_bombs

        # generate the board
        while bombs > 0:
            # randomly pick a place to place a bomb
            mine_col, mine_lin = random.randint(0, self.width - 1), random.randint(0, self.height - 1)

            # find a cell that is not a bomb
            while self.zones[mine_lin][mine_col] == BoardCell.BOMB.value:
                mine_col, mine_lin = random.randint(0, self.width - 1), random.randint(0, self.height - 1)

            self.zones[mine_lin][mine_col] = BoardCell.BOMB.value

            bombs -= 1

        dl = [-1, -1, 0, 1, 1, 1, 0, -1]
        dc = [0, 1, 1, 1, 0, -1, -1, -1]

        # complete the board with numbers
        for lin in range(self.height):
            for col in range(self.width):
                # skip bombs
                if self.zones[lin][col] == BoardCell.BOMB.value:
                    continue

                # check neighbors of current cell and sum the bombs around it
                self.zones[lin][col] = sum(
                    self.__within_bounds(lin + off_lin, col + off_col)
                    and self.zones[lin + off_lin][col + off_col] == BoardCell.BOMB.value
                    for off_lin, off_col in zip(dl, dc)
                )

        # the board of the player, each cell has one of the values:
        # - a positive value from 0 to 8 indicating the number of neighboring bombs
        # - BoardCell.BOMB.value indicating that the cell is a bomb
        # - BoardCell.UNSELECTED.value indicating that the player doesn't know yet the value of this cell
        # - BoardCell.FLAGGED.value indicating that the player flagged this cell
        #
        # initially, the board is set on all field with UNSELECTED
        self.board = [[BoardCell.UNSELECTED.value for _ in range(self.width)] for _ in range(self.height)]

        self.game_over = False

        # set a timer for the game
        # the timer will emit GAME_TIMER_TICK event once every 1s `time` times
        self.time_left = time
        pygame.time.set_timer(TIMER_TICK, 1000, time)

    def __within_bounds(self, lin, col):
        """
        Check if point (l, c) is found on the grid.
        """
        return 0 <= lin < self.height and 0 <= col < self.width

    # offsets for neighbors
    DL = [-1, -1, 0, 1, 1, 1, 0, -1]
    DC = [0, 1, 1, 1, 0, -1, -1, -1]

    def __reveal_zone(self, lin, col):
        """
        Recursively reveal the current zone until a non-zero value is met.
        """
        # if the cell is already revealed or flagged, stop
        if self.board[lin][col] != BoardCell.UNSELECTED.value or self.board[lin][col] == BoardCell.FLAGGED.value:
            return

        # reveal zone
        self.board[lin][col] = self.zones[lin][col]

        # if the cell is a bomb, game over
        if self.board[lin][col] == BoardCell.BOMB.value:
            self.__end_game()
            self.__reveal_bombs()
            # assign a special type to this bomb so that the player knows which bomb caused the loss
            self.board[lin][col] = BoardCell.BOMB_REVEALED.value
            return

        # if the cell is zero, continue exploring
        if self.board[lin][col] == 0:
            for dl, dc in zip(GameState.DL, GameState.DC):
                if self.__within_bounds(lin + dl, col + dc):
                    self.__reveal_zone(lin + dl, col + dc)

    def __reveal_bombs(self):
        """
        Upon losing the game, this method is called to reveal the bombs locations to the player.
        """
        for i in range(self.height):
            for j in range(self.width):
                if self.zones[i][j] == BoardCell.BOMB.value:
                    self.board[i][j] = self.zones[i][j]

    def __end_game(self):
        """
        Sets the `game_over` flag to True and stops the timer (if it exists).
        """
        self.game_over = True
        pygame.time.set_timer(TIMER_TICK, 0)

    def reveal_zone(self, lin, col) -> "GameState":
        """
        Reveal the value of the selected zone.
        """
        new_state = deepcopy(self)

        # don't allow moves if game is over or if the move is invalid
        if self.game_over or not self.__within_bounds(lin, col):
            return new_state

        # explore new cells
        new_state.__reveal_zone(lin, col)

        return new_state

    def flag_zone(self, lin, col):
        """
        Flag/unflag the zone.
        """
        new_state = deepcopy(self)

        # don't allow moves if game is over or if the move is invalid
        if self.game_over or not self.__within_bounds(lin, col):
            return new_state

        if new_state.board[lin][col] == BoardCell.UNSELECTED.value:
            # if the cell is unselected, flag it
            new_state.board[lin][col] = BoardCell.FLAGGED.value
            pygame.event.post(pygame.event.Event(BOARD_FLAG_PLACED))
        elif new_state.board[lin][col] == BoardCell.FLAGGED.value:
            # if the cell is flagged, unflag it
            new_state.board[lin][col] = BoardCell.UNSELECTED.value
            pygame.event.post(pygame.event.Event(BOARD_FLAG_REMOVED))

        # if the cell was neither of the above, just ignore the move

        return new_state

    def timer_ticked(self):
        """
        Update the state on timer tick.
        """
        new_state = deepcopy(self)
        new_state.time_left -= 1

        # if the timer ran out, end the game
        if new_state.time_left == 0:
            new_state.__end_game()

        return new_state

    def is_over(self):
        return self.game_over
