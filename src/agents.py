import math
import abc


def default_evaluation_function(game_state):
    max_consecutive_range = 0
    for row in range(game_state.num_of_rows):
        for col in range(game_state.num_of_columns):
            if game_state.board.board[row][col] == 1:
                directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
                for dr, dc in directions:
                    val = game_state.board.count_consecutive_pieces(row, col, dr, dc, 1)
                    if val > max_consecutive_range:
                        max_consecutive_range = val

    if max_consecutive_range == 0:  # there are no stones of the current player on the board
        flag = False
        for row in range(game_state.num_of_rows - 1, -1, -1):
            for col in range(game_state.num_of_columns):
                if game_state.board.board[row, col] == 0:  # empty
                    max_consecutive_range = row
                    flag = True
            if flag:
                break
    else:
        max_consecutive_range = 2 * max_consecutive_range

    winning_combination = amount_of_winning_combination(game_state)

    return 0.4 * max_consecutive_range + 0.6 * winning_combination


def amount_of_winning_combination(game_state):
    res = 0

    for row in range(game_state.num_of_rows):
        res += row_winning_combination(row, 0, 4, game_state)

    for col in range(game_state.num_of_columns):
        res += col_winning_combination(col, 0, 3, game_state)

    return res


def row_winning_combination(row, start, end,
                            game_state):  # start = first col to check , end = last col to start checking from
    res = 0
    for c in range(start, end):
        for addition in range(4):
            if game_state.board.board[row, c + addition] == 1:
                res += 1
            elif game_state.board.board[row, c + addition] == 2:  # min player stone
                res -= 1
    return res


def col_winning_combination(col, start, end, game_state):
    res = 0
    for r in range(start, end):
        for addition in range(4):
            if game_state.board.board[r + addition, col] == 1:
                res += 1
            elif game_state.board.board[r + addition, col] == 2:  # min player stone
                res -= 1
    return res


def diagonal_winning_combination(r_start, r_end, c_start, c_end, game_state, player):
    res = 0
    while 0 <= r_start < r_end and 0 <= c_start < c_end:
        if game_state.board.board[r_start, c_start] == 1:
            res += 1
        elif game_state.board.board[r_start, c_start] == 2:
            res -= 1
        r_start += 1
        c_start += 1
    return res


class Agent(object):
    """
    This class provides some common elements to all of our agents. Any methods defined here will be available
    to the MinmaxAgent and AlphaBetaAgent.

    This is an abstract class that should not be instantiated directly.
    """

    def __init__(self, evaluation_function=default_evaluation_function, depth=2):
        self.depth = depth
        self.evaluation_function = evaluation_function

    @abc.abstractmethod
    def get_action(self, game_state):
        return


# TODO add stupid agent
class MinmaxAgent(Agent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """

        def helper(game_state, agent, depth):
            if depth == 0 or game_state.done:
                return self.evaluation_function(game_state), None

            if agent == 1:
                max_val = -math.inf
                best_action = None
                legal_actions = game_state.get_legal_actions()
                for action in legal_actions:
                    successor_per_action = game_state.generate_successor(action)
                    new_val, new_action = helper(successor_per_action, 2, depth)
                    if new_val > max_val:
                        max_val = new_val
                        best_action = action
                return max_val, best_action

            else:
                min_val = math.inf
                best_action = None
                legal_actions = game_state.get_legal_actions()
                for action in legal_actions:
                    successor_per_action = game_state.generate_successor(action)
                    new_val, new_action = helper(successor_per_action, 1, depth - 1)
                    if new_val < min_val:
                        min_val = new_val
                        best_action = action
                return min_val, best_action

        agent = 1
        return helper(game_state, agent, self.depth)[1]


class AlphaBetaAgent(Agent):
    """
    Our minimax agent with alpha-beta pruning.
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction using alpha beta pruning.
        """
# RL is an agent?
