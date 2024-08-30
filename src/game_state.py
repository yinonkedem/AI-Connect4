import numpy as np
from board import Board
DEFAULT_BOARD_ROWS = 6
DEFAULT_BOARD_COLUMNS = 7


class GameState(object):
    def __init__(self, rows=DEFAULT_BOARD_ROWS, columns=DEFAULT_BOARD_COLUMNS, board=None, done=False,
                 player_about_to_play=1):
        self.done = done
        self.winner = None
        self.player_about_to_play = player_about_to_play
        if board is None:
            board = Board()
        self.board = board
        self.num_of_rows, self._num_of_columns = rows, columns

    def done(self):
        return self._done

    def current_player(self):
        return self.player_about_to_play

    def board(self):
        return self.board

    def get_legal_actions(self):
        # returns a list of all the cols where dropping a piece is possible
        return self.board.get_valid_moves()

    def apply_action(self, action):
        # drop the piece into the chosen column
        if not self.board.is_valid_move(action):
            raise Exception("Illegal action: Column is full.")
        the_row_placed = self.board.make_move(action, self.player_about_to_play)

        # Check for a win or draw
        if self.check_win(the_row_placed, action):
            self._done = True
            self.winner = self.player_about_to_play
        elif not self.get_legal_actions():
            self._done = True  # Draw
            self.winner = -1

        # Switch players
        if self.player_about_to_play == 1:
            self.player_about_to_play = 2
        else:
            self.player_about_to_play = 1

    def check_win(self, row, col):
        """Check the board to see if there's a winner after the last move."""

        # Directions to check: horizontal, vertical, and both diagonals
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            print(self.board.count_consecutive_pieces(row, col, dr, dc, self.player_about_to_play) )
            if self.board.count_consecutive_pieces(row, col, dr, dc, self.player_about_to_play) >= self.board.get_strike():
                return True

        return False



    # def check_win(self, row, col):
    #     # Check for 4 in a row in all directions
    #     def check_direction(delta_row, delta_col):
    #         count = 0
    #         for d in [-3, -2, -1, 0, 1, 2, 3]:
    #             r, c = row + d * delta_row, col + d * delta_col
    #             if 0 <= r < self._num_of_rows and 0 <= c < self._num_of_columns and self._board[
    #                 r, c] == self.player_about_to_play:
    #                 count += 1
    #                 if count == 4:
    #                     return True
    #             else:
    #                 count = 0
    #         return False
    #
    #     return (check_direction(1, 0) or  # Vertical
    #             check_direction(0, 1) or  # Horizontal
    #             check_direction(1, 1) or  # Diagonal /
    #             check_direction(1, -1))  # Diagonal \

    def generate_successor(self, action):
        successor = GameState(rows=self.num_of_rows, columns=self._num_of_columns, board=self.board.copy(),
                              done=self.done, player_about_to_play=self.player_about_to_play)
        successor.apply_action(action)
        return successor
