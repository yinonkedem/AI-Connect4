import math
import abc
import random


# def score_evaluation_function(game_state):
#     if game_state.done:
#         return 100
#     return 0
#
def score_evaluation_function(game_state):
    score = 0
    max_consecutive_range = calculate_current_player_max_consecutive_range(game_state)
    winning_combination = approximate_number_of_future_winning_combinations(game_state)
    if max_consecutive_range == 4:
        score = math.inf
    else:
        score = 10 ** max_consecutive_range
    return 0.5 * max_consecutive_range + 0.5 * winning_combination


def calculate_current_player_max_consecutive_range(game_state):
    max_consecutive_range = 0
    for row in range(game_state.num_of_rows):
        for col in range(game_state.num_of_columns):
            val = 0
            directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
            for dr, dc in directions:
                val = max(val, game_state.board.count_consecutive_pieces(row, col, dr, dc,
                                                                         game_state.player_about_to_play))
            max_consecutive_range = max(max_consecutive_range, val)
    return max_consecutive_range


def approximate_number_of_future_winning_combinations(game_state):
    def get_winning_lines_starting_indexes(game_State):
        # rows
        for row in range(game_State.num_of_rows):
            for col in range(game_State.num_of_columns - 3):
                lines.append([(row, col + i) for i in range(4)])
        # cols
        for row in range(game_State.num_of_rows - 3):
            for col in range(game_State.num_of_columns):
                lines.append([(row + i, col) for i in range(4)])
        # top right diagonals
        for row in range(3, game_State.num_of_rows):
            for col in range(game_State.num_of_columns - 3):
                lines.append([(row - i, col + i) for i in range(4)])
        # bottom left diagonals
        for row in range(game_State.num_of_rows - 3):
            for col in range(game_State.num_of_columns - 3):
                lines.append([(row + i, col + i) for i in range(4)])

    def evaluate_spot(row, col):
        if game_state.board.get_player(row, col) == 1:
            return 1
        elif game_state.board.get_player(row, col) == 2:
            return -1
        else:
            return 0

    res = 0
    lines = []
    get_winning_lines_starting_indexes(game_state)
    for line in lines:
        line_value = sum(evaluate_spot(row, col) for row, col in line)
        res += line_value

    return res

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


class RandomAgent(Agent):
    def get_action(self, game_state):
        return random.choice(game_state.board.get_valid_moves())


class MinmaxAgent(Agent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """

        def helper(game_state, agent, depth, alpha, beta):
            if depth == 0 or game_state.done:
                return self.evaluation_function(game_state), None

            if agent == 1:
                max_val = -math.inf
                best_action = None
                legal_actions = game_state.get_legal_actions()
                for action in legal_actions:
                    successor_per_action = game_state.generate_successor(action)
                    new_val, new_action = helper(successor_per_action, 2, depth, alpha, beta)
                    if new_val > max_val:
                        max_val = new_val
                        best_action = action
                    alpha = max(alpha, max_val)
                    if beta <= alpha:
                        break
                return max_val, best_action

            else:
                min_val = math.inf
                best_action = None
                legal_actions = game_state.get_legal_actions()
                for action in legal_actions:
                    successor_per_action = game_state.generate_successor(action)
                    new_val, new_action = helper(successor_per_action, 1, depth - 1, alpha, beta)
                    if new_val < min_val:
                        min_val = new_val
                        best_action = action
                    beta = min(beta, min_val)
                    if beta <= alpha:
                        break
                return min_val, best_action

        agent = 1
        return helper(game_state, agent, self.depth, -math.inf, math.inf)[1]


class AlphaBetaAgent(Agent):
    """
    Our minimax agent with alpha-beta pruning.
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction using alpha beta pruning.
        """
# RL is an agent?
