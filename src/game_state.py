import numpy as np
from board import Board


class GameState(object):
    def __init__(self, board=None, done=False, player_about_to_play=1):
        self.player_about_to_play = player_about_to_play
        self.done = done
        self.winner = None
        self.board = Board() if board is None else board
        self.num_of_rows, self.num_of_columns = self.board.number_of_rows, self.board.number_of_cols
        self.reset()  # Use reset to initialize the game state

    def reset(self):
        """
        Reset the game state to the beginning.
        """
        self.board.reset()  # Assuming Board has a reset method to clear the board
        self.done = False
        self.winner = None
        self.player_about_to_play = 1  # Reset to the first player

    def is_done(self):
        return self.done

    def check_winner(self):
        # This is a simplified check for horizontal lines only
        for row in range(6):  # Assuming board height is 6
            for col in range(4):  # Only need to check starting columns 0 through 3 for horizontal win
                if (self.board.board[row, col] == self.board.board[row, col + 1] ==
                        self.board.board[row, col + 2] == self.board.board[row, col + 3] != 0):
                    return self.board.board[row, col]  # Return the player number that won

        # Add similar checks for vertical and diagonal wins here

        return 0  # Return 0 if no winner found

    def calculate_reward(self):
        """
        Calculate the reward after an action has been applied.
        """
        if self.check_winner() == 1:
            return 1  # Reward for winning
        elif self.is_done():
            return -1  # Penalty for losing or draw
        else:
            return 0  # No reward or penalty during ongoing game

    def current_player(self):
        return self.player_about_to_play

    def board(self):
        return self.board

    def get_legal_actions(self):
        # returns a list of all the cols where dropping a piece is possible
        return self.board.get_valid_moves()

    def apply_action(self, action):
        the_row_placed = self.board.make_move(action, self.player_about_to_play)

        # Check for a win or draw
        if self.check_win(the_row_placed, action):
            self.done = True
            self.winner = self.player_about_to_play
        elif not self.get_legal_actions():
            self.done = True  # Draw
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
            if self.board.count_consecutive_pieces(row, col, dr, dc, self.player_about_to_play) == self.board.get_strike():
                return True

        return False

    def generate_successor(self, action):
        successor = GameState(board=self.board.copy(),
                              done=self.done, player_about_to_play=self.player_about_to_play)
        successor.apply_action(action)
        return successor
