import math
import numpy as np
import abc
from game import Action


class Agent(object):
    """
    This class provides some common elements to all of our agents. Any methods defined here will be available
    to the MinmaxAgent and AlphaBetaAgent.

    This is an abstract class that should not be instantiated directly.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        # self.evaluation_function =  TODO write a default evaluation function, maybe in utils.py
        self.depth = depth

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

        def helper(game_sate, agent, depth):
            if depth == 0 or game_sate.done:
                return self.evaluation_function(game_sate), Action.STOP

            if agent == 0:
                max_val = -math.inf
                best_action = None
                player_legal_actions = game_sate.get_legal_actions(agent)
                for action in player_legal_actions:
                    successor_per_action = game_sate.generate_successor(agent, action)
                    new_val, new_action = helper(successor_per_action, 1, depth)
                    if new_val > max_val:
                        max_val = new_val
                        best_action = action
                return max_val, best_action

            else:
                min_val = math.inf
                best_action = None
                player_legal_actions = game_sate.get_legal_actions(agent)
                for action in player_legal_actions:
                    successor_per_action = game_sate.generate_successor(agent, action)
                    new_val, new_action = helper(successor_per_action, 0, depth - 1)
                    if new_val < min_val:
                        min_val = new_val
                        best_action = action
                return min_val, best_action

        agent = 0
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
