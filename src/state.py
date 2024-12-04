import random
from copy import deepcopy
from enum import Enum


class BoardCell(Enum):
    BOMB_REVEALED = 17
    BOMB = 16
    UNSELECTED = -1
    FLAGGED = -2


class GameState:
    def __init__(self, *, size: tuple[int, int] = (16, 16), max_bombs=64):
        """
        Initialize game state.
        """
        self.height, self.width = self.size = size

        # board with all bombs and all cells marked with their score
        self.zones = [[0 for _ in range(self.width)] for _ in range(self.height)]

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

    def __within_bounds(self, lin, col):
        """
        Check if point (l, c) is found on the grid.
        """
        return 0 <= lin < self.height and 0 <= col < self.width

    # offsets for neighbors
    DL = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]

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
            self.game_over = True
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
        # don't allow moves if game is over
        if self.game_over:
            raise ValueError("Game is over.")

        if not self.__within_bounds(lin, col):
            raise ValueError("Invalid board position.")

        new_state = deepcopy(self)

        if new_state.board[lin][col] == BoardCell.UNSELECTED.value:
            # if the cell is unselected, flag it
            new_state.board[lin][col] = BoardCell.FLAGGED.value
        elif new_state.board[lin][col] == BoardCell.FLAGGED.value:
            # if the cell is flagged, unflag it
            new_state.board[lin][col] = BoardCell.UNSELECTED.value

        # if the cell was neither of the above, just ignore the move

        return new_state

    def is_over(self):
        return self.game_over
