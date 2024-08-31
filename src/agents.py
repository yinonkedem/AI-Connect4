import math
import abc


def score_evaluation_function(game_state):
    if game_state.done:
        return 100
    return 0


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
