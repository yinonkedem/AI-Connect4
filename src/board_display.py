import time


class NormalDisplay(object):

    def update_state(self, new_state, game_over = False):
        if game_over:
            if new_state.winner == -1:
                print(f"the game ended in a draw")
            else:
                print(f"the winner is {new_state.winner} ")
        else:
            print(new_state.board._str_())

class SilentDisplay:
    def update_state(self, state, final=False):
        """
        Does nothing with the state, suitable for running simulations without output.

        Args:
        - state: The current game state object (not used).
        - final: Boolean indicating if the game has ended (not used).
        """
        pass

# TODO - this class will be in charge of printing the board after each player's move
# see mainloop_iteration function used in game py and implement it here
# should use the state, specifically board sate