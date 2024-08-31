import numpy as np

DEFAULT_BOARD_LENGTH = 6
DEFAULT_BOARD_WIDTH = 7
DEFAULT_NUM_COLORS = 2
DEFAULT_STRIKE_SIZE = 3


class Board:
    def __init__(self, strike_size=DEFAULT_STRIKE_SIZE, number_of_rows=DEFAULT_BOARD_LENGTH,
                 number_of_cols=DEFAULT_BOARD_WIDTH, num_of_colors=DEFAULT_NUM_COLORS):
        self.strike_size = strike_size
        self.num_of_colors = num_of_colors
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self.board = np.zeros((self.number_of_rows, self.number_of_cols), dtype=int)
        self.last_move = None

    def is_valid_move(self, col):
        """Check if the top row in the column is empty, i.e., a piece can be placed."""
        return self.board[0, col] == 0

    def get_valid_moves(self):
        """Return a list of columns where a move can be made."""
        return [col for col in range(self.number_of_cols) if self.is_valid_move(col)]

    def make_move(self, col, player):
        """Place a piece for the player in the specified column."""
        if not self.is_valid_move(col):
            raise ValueError(f"Column {col} is full")

        for row in range(self.number_of_rows - 1, -1, -1):
            if self.board[row, col] == 0:  # empty place
                self.board[row, col] = player
                self.last_move = (row, col)
                return row

    def get_number_of_rows(self):
        return self.number_of_rows

    def get_number_of_cols(self):
        return self.number_of_cols

    def get_strike(self):
        return self.strike_size

    def copy(self):
        """Return a deep copy of the board."""
        new_board = Board(self.strike_size, self.number_of_rows, self.number_of_cols, self.num_of_colors)
        new_board.board = np.copy(self.board)
        new_board.last_move = self.last_move
        return new_board

    def count_consecutive_pieces(self, row, col, dr, dc, player):
        """Count consecutive pieces of the same player in a given direction."""
        count = 0

        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < self.number_of_rows and 0 <= c < self.number_of_cols and self.board[r, c] == player:
            count += 1
            r += dr
            c += dc

        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < self.number_of_rows and 0 <= c < self.number_of_cols and self.board[r, c] == player:
            count += 1
            r -= dr
            c -= dc

        return count

    def is_full(self):
        """Check if the board is full (no more valid moves)."""
        return all(self.board[0, col] != 0 for col in range(self.cols))

    def reset(self):
        """Reset the board for a new game."""
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.last_move = None

    def __str__(self):
        """Return a string representation of the board."""
        str_to_print = ''
        for row in self.board:
            str_row = ' '.join(str(cell) for cell in row)
            str_to_print += str_row + '\n'
        str_to_print += '-' * (self.number_of_cols * 2 - 1)  # Print a separator line
        return str_to_print
















    # def check_winner(self):
    #     """Check the board to see if there's a winner after the last move."""
    #     if self.last_move is None:
    #         return None
    #
    #     row, col = self.last_move
    #     player = self.board[row, col]
    #
    #     # Directions to check: horizontal, vertical, and both diagonals
    #     directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    #     for dr, dc in directions:
    #         if self.count_consecutive_pieces(row, col, dr, dc, player) >= self.strike_size:
    #             return player
    #
    #     return None
    #
    # def count_consecutive_pieces(self, row, col, dr, dc, player):
    #     """Count consecutive pieces of the same player in a given direction."""
    #     count = 1
    #
    #     # Check one direction
    #     r, c = row + dr, col + dc
    #     while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r, c] == player:
    #         count += 1
    #         r += dr
    #         c += dc
    #
    #     # Check the opposite direction
    #     r, c = row - dr, col - dc
    #     while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r, c] == player:
    #         count += 1
    #         r -= dr
    #         c -= dc
    #
    #     return count
# Example usage:
# if _name_ == "_main_":
#     board = Board()
#     board.make_move(3, 1)
#     board.make_move(3, 2)
#     board.make_move(3, 1)
#     board.make_move(3, 2)
#     board.make_move(3, 1)
#     board.make_move(3, 2)
#     board.make_move(3, 1)
#     print(board)
#     print("Winner:", board.check_winner())