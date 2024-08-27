# TODO this is the hardest part. we need to reference from 2048
# the job of this class is to keep the state of the board. each board_state will hold a board in its fields
import numpy as np

DEFAULT_ROWS = 6
DEFAULT_COLUMNS = 7


class GameState(object):
    def __init__(self, rows=DEFAULT_ROWS, columns=DEFAULT_COLUMNS, board=None, done=False):
        super(GameState, self).__init__()
        self._done = done
        if board is None:
            board = np.zeros(rows, columns)
        self._board = board
        self._num_of_rows, self._num_of_columns = rows, columns

    def done(self):
        return self._done

    def board(self):
        return self._board
