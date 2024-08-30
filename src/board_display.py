import time


class NormalDisplay(object):

    def update_state(self, new_state, action, opponent_action):
        if new_state.done:
            print(f"the winner is {new_state.winner} ")
        else:
            print(new_state.board)
# TODO - this class will be in charge of printing the board after each player's move
# see mainloop_iteration function used in game py and implement it here
# should use the state, specifically board sate