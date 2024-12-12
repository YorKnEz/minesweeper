import random
from copy import deepcopy
from enum import Enum

import pygame

from constants import BOARD_FLAG_PLACED, BOARD_FLAG_REMOVED, GAME_OVER, TIMER_TICK


class BoardCell(Enum):
    BOMB_REVEALED = 17
    BOMB = 16
    UNSELECTED = -1
    FLAGGED = -2


class GameState:
    # offsets for neighbors
    DL = [-1, -1, 0, 1, 1, 1, 0, -1]
    DC = [0, 1, 1, 1, 0, -1, -1, -1]

    def __init__(self, *, size: tuple[int, int] = (16, 16), max_bombs=64, time=0):
        """Initialize game state.

        The `size` parameter determines the size of the grid.
        The `max_bombs` parameter determines the number of bombs to generate, it must be between 0 and `size`.
        The `time` parameter determines how much time the player has (if it is 0, then the timer is disabled).
        """
        self.height, self.width = self.size = size
        self.max_bombs = max_bombs
        self.flags = max_bombs
        self.time_left = time

        # board with all bombs and all cells marked with their score
        self.zones = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # the board of the player, each cell has one of the values:
        # - a positive value from 0 to 8 indicating the number of neighboring bombs
        # - BoardCell.BOMB.value indicating that the cell is a bomb
        # - BoardCell.UNSELECTED.value indicating that the player doesn't know yet the value of this cell
        # - BoardCell.FLAGGED.value indicating that the player flagged this cell
        #
        # initially, the board is set on all field with UNSELECTED
        self.board = [[BoardCell.UNSELECTED.value for _ in range(self.width)] for _ in range(self.height)]

        self.game_over = False
        self.init = False
        self.unrevealed_zones = self.width * self.height  # used for checking the win condition

    def __within_bounds(self, lin, col):
        """Check if point `(lin, col)` is found on the grid."""
        return 0 <= lin < self.height and 0 <= col < self.width

    def __around_cell(self, cell_lin, cell_col, lin, col):
        """Check if `(lin, col)` is a point around or precisely `(cell_lin, cell_col)`."""
        return (cell_lin == lin and cell_col == col) or any(
            (cell_lin == lin + dl) and (cell_col == col + dc)
            for dl, dc in zip(GameState.DL, GameState.DC)
            if self.__within_bounds(lin + dl, col + dc)
        )

    def __start_game(self, lin, col):
        """Initialize the game.

        This generates the board for the game after the first click has happened. The `(lin, col)` argument specifies
        the coordinates of the click.
        It also starts the counter if there is any.
        """
        bombs = self.max_bombs

        # generate the board such that no bomb is placed on (lin, col) or around it
        while bombs > 0:
            # randomly pick a place to place a bomb
            mine_col, mine_lin = random.randint(0, self.width - 1), random.randint(0, self.height - 1)

            # find a cell that is not a bomb and is not on around start
            while (self.zones[mine_lin][mine_col] == BoardCell.BOMB.value) or self.__around_cell(
                lin, col, mine_lin, mine_col
            ):
                mine_col, mine_lin = random.randint(0, self.width - 1), random.randint(0, self.height - 1)

            self.zones[mine_lin][mine_col] = BoardCell.BOMB.value

            bombs -= 1

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
                    for off_lin, off_col in zip(GameState.DL, GameState.DC)
                )

        # set a timer for the game
        # the timer will emit GAME_TIMER_TICK event once every 1s `time` times
        pygame.time.set_timer(TIMER_TICK, 1000, self.time_left)

        # mark game as started
        self.init = True

    def __end_game(self):
        """Sets the `game_over` flag to True and stops the timer (if it exists)."""
        self.game_over = True
        pygame.time.set_timer(TIMER_TICK, 0)
        pygame.event.post(pygame.event.Event(GAME_OVER))

    def __reveal_zone(self, lin, col):
        """Recursively reveal the current zone until a non-zero value is met."""
        # if the cell is already revealed or flagged, stop
        if self.board[lin][col] != BoardCell.UNSELECTED.value or self.board[lin][col] == BoardCell.FLAGGED.value:
            return

        # reveal zone
        self.board[lin][col] = self.zones[lin][col]
        self.unrevealed_zones -= 1

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
        """Upon losing the game, this method is called to reveal the bombs locations to the player."""
        for i in range(self.height):
            for j in range(self.width):
                if self.zones[i][j] == BoardCell.BOMB.value:
                    self.board[i][j] = self.zones[i][j]

    def reveal_zone(self, lin, col) -> "GameState":
        """Reveal the value of the selected zone.

        If the game has not been started yet, this method calls `__start_game` which initializes the board and starts
        the timer countdown.

        If the game is over or the given position is invalid, the move is ignored.

        It returns the new state of the game, thus keeping the state immutable.
        """
        # if the game hasn't been initialized, start it
        if not self.init:
            self.__start_game(lin, col)

        new_state = deepcopy(self)

        # don't allow moves if game is over or if the move is invalid
        if self.game_over or not self.__within_bounds(lin, col):
            return new_state

        # explore new cells
        new_state.__reveal_zone(lin, col)

        # if the number of unrevealed_zones is equal to the number of bombs, then the game is over
        if new_state.is_win():
            new_state.__end_game()

        return new_state

    def flag_zone(self, lin, col):
        """Flag/unflag the zone.

        If the game has not been started yet, or the game is over or the given position is invalid, the move is ignored.

        It returns the new state of the game, thus keeping the state immutable.
        """
        new_state = deepcopy(self)

        # don't allow moves if game is over or if the move is invalid or if the game hasn't been started
        if not self.init or self.game_over or not self.__within_bounds(lin, col):
            return new_state

        if new_state.board[lin][col] == BoardCell.UNSELECTED.value:
            # if the cell is unselected, flag it and flags left
            if new_state.flags > 0:
                new_state.board[lin][col] = BoardCell.FLAGGED.value
                new_state.flags -= 1
                pygame.event.post(pygame.event.Event(BOARD_FLAG_PLACED))
        elif new_state.board[lin][col] == BoardCell.FLAGGED.value:
            # if the cell is flagged, unflag it
            new_state.board[lin][col] = BoardCell.UNSELECTED.value
            new_state.flags += 1
            pygame.event.post(pygame.event.Event(BOARD_FLAG_REMOVED))

        # if the cell was neither of the above, just ignore the move

        return new_state

    def timer_ticked(self):
        """Update the state on timer tick.

        If the game has not started yet, the move is ignored.

        It returns the new state of the game, thus keeping the state immutable.
        """
        new_state = deepcopy(self)

        # if the game hasn't been initialized, ignore the move
        if not self.init:
            return new_state

        new_state.time_left -= 1

        # if the timer ran out, end the game
        if new_state.time_left == 0:
            new_state.__end_game()

        return new_state

    def is_over(self):
        """Check if the game has ended."""
        return self.game_over

    def is_win(self):
        """Check if the game was won or not."""
        # if the number of unrevealed_zones is equal to the number of bombs, then the game is over
        return self.unrevealed_zones == self.max_bombs
