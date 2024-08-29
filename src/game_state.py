import numpy as np

DEFAULT_BOARD_ROWS = 6
DEFAULT_BOARD_COLUMNS = 7


class GameState(object):
    def __init__(self, rows=DEFAULT_BOARD_ROWS, columns=DEFAULT_BOARD_COLUMNS, board=None, done=False,
                 player_about_to_play=1):
        self._done = done
        self.player_about_to_play = player_about_to_play
        if board is None:
            board = np.zeros(rows, columns)
        self._board = board
        self._num_of_rows, self._num_of_columns = rows, columns

    def done(self):
        return self._done

    def current_player(self):
        return self.player_about_to_play

    def board(self):
        return self._board

    def get_legal_actions(self):
        # returns a list of all the cols where dropping a piece is possible
        return [col for col in range(self._num_of_columns) if self._board[0, col] == 0]

    def apply_action(self, action):
        # drop the piece into the chosen column
        if self._board[0, action] != 0:
            raise Exception("Illegal action: Column is full.")
        for row in range(self._num_of_rows - 1, -1, -1):
            if self._board[row, action] == 0:
                self._board[row, action] = self.player_about_to_play
                break

        # Check for a win or draw
        if self.check_win(row, action):
            self._done = True
        elif not self.get_legal_actions():
            self._done = True  # Draw

        # Switch players
        if self.player_about_to_play ==1:
            self.player_about_to_play =2
        else:
            self.player_about_to_play = 1

    def check_win(self, row, col):
        # Check for 4 in a row in all directions
        def check_direction(delta_row, delta_col):
            count = 0
            for d in [-3, -2, -1, 0, 1, 2, 3]:
                r, c = row + d * delta_row, col + d * delta_col
                if 0 <= r < self._num_of_rows and 0 <= c < self._num_of_columns and self._board[
                    r, c] == self.player_about_to_play:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
            return False

        return (check_direction(1, 0) or  # Vertical
                check_direction(0, 1) or  # Horizontal
                check_direction(1, 1) or  # Diagonal /
                check_direction(1, -1))  # Diagonal \

    def generate_successor(self, action):
        successor = GameState(rows=self._num_of_rows, columns=self._num_of_columns, board=self._board.copy(),
                              done=self._done, current_player=self.player_about_to_play)
        successor.apply_action(action)
        return successor
