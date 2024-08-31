import math
import abc


def score_evaluation_function(game_state):
    max_consecutive_range = 0
    for row in range(game_state.num_of_rows):
        for col in range(game_state.num_of_columns):
            if game_state.board.board[row][col] == game_state.player_about_to_play:
                val = 1  # we found one piece on the board in that color
                directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
                for dr, dc in directions:
                    val += game_state.board.count_consecutive_pieces(row, col, dr, dc,
                                                                     game_state.player_about_to_play)
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
    return max_consecutive_range


class Agent(object):
    """
    This class provides some common elements to all of our agents. Any methods defined here will be available
    to the MinmaxAgent and AlphaBetaAgent.

    This is an abstract class that should not be instantiated directly.
    """

    def __init__(self, evaluation_function=score_evaluation_function, depth=2):
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
