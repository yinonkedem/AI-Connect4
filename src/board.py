import numpy as np
#TODO this class will keep the state of the board

class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.last_move = None

    def is_valid_move(self, col):
        """Check if the top row in the column is empty, i.e., a piece can be placed."""
        return self.board[0, col] == 0

    def get_valid_moves(self):
        """Return a list of columns where a move can be made."""
        return [col for col in range(self.cols) if self.is_valid_move(col)]

    def make_move(self, col, player):
        """Place a piece for the player in the specified column."""
        if not self.is_valid_move(col):
            raise ValueError(f"Column {col} is full")

        for row in range(self.rows - 1, -1, -1):
            if self.board[row, col] == 0:
                self.board[row, col] = player
                self.last_move = (row, col)
                break

    def check_winner(self):
        """Check the board to see if there's a winner after the last move."""
        if self.last_move is None:
            return None

        row, col = self.last_move
        player = self.board[row, col]

        # Directions to check: horizontal, vertical, and both diagonals
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            if self.count_consecutive_pieces(row, col, dr, dc, player) >= 4:
                return player

        return None

    def count_consecutive_pieces(self, row, col, dr, dc, player):
        """Count consecutive pieces of the same player in a given direction."""
        count = 1

        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r, c] == player:
            count += 1
            r += dr
            c += dc

        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r, c] == player:
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
        return "\n".join(" ".join(str(int(cell)) for cell in row) for row in self.board)


# Example usage:
if __name__ == "__main__":
    board = Board()
    board.make_move(3, 1)
    board.make_move(3, 2)
    board.make_move(3, 1)
    board.make_move(3, 2)
    board.make_move(3, 1)
    board.make_move(3, 2)
    board.make_move(3, 1)
    print(board)
    print("Winner:", board.check_winner())
