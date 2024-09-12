import math
import abc
import random


class Agent(object):
    """
    This class provides some common elements to all of our agents. Any methods defined here will be available
    to the MinmaxAgent and AlphaBetaAgent.

    This is an abstract class that should not be instantiated directly.
    """

    def __init__(self, player_id, evaluation_function=None, depth=0):
        self.player_id = player_id
        self.depth = depth
        self.evaluation_function = evaluation_function

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class RandomAgent(Agent):
    def __init__(self, player_id):
        super().__init__(player_id, evaluation_function=None, depth=0)

    def get_action(self, game_state):
        return random.choice(game_state.board.get_valid_moves())


def minimax_evaluation_function(game_state, player_id):
    if game_state.done:
        if game_state.winner == player_id:
            return 1000000
        else:
            return -1000000
    max_consecutive_range = calculate_player_max_consecutive_range(game_state, game_state.player_about_to_play)
    winning_combination = approximate_number_of_future_winning_combinations(game_state)
    return 0.5*winning_combination + max_consecutive_range


def calculate_player_max_consecutive_range(game_state, player):
    max_consecutive_range = 0
    for row in range(game_state.num_of_rows):
        for col in range(game_state.num_of_columns):
            directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
            for dr, dc in directions:
                max_consecutive_range = max(max_consecutive_range,
                                            game_state.board.count_consecutive_pieces(row, col, dr, dc,
                                                                                      player))
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
        if game_state.board.get_player(row, col) == game_state.player_about_to_play:
            return 1
        elif game_state.board.get_player(row, col) == 0:
            return 0
        else:
            return -1

    res = 0
    lines = []
    get_winning_lines_starting_indexes(game_state)
    for line in lines:
        line_value = sum(evaluate_spot(row, col) for row, col in line)
        res += line_value

    return res


class MinmaxAgentWithPruning(Agent):
    def __init__(self, player_id):
        super().__init__(player_id, evaluation_function=minimax_evaluation_function, depth=2)

    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """

        def helper(game_state, agent, depth, alpha, beta):
            if depth == 0 or game_state.done:
                return self.evaluation_function(game_state, self.player_id), None
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


def calculate_reward(game_state):
    """
    Calculate the reward after an action has been applied.
    """
    if game_state.check_winner() == 1:
        return 1  # Reward for winning
    elif game_state.is_done():
        return -1  # Penalty for losing or draw
    else:
        return 0


def encode_board_into_one_dimension_array(game_state):
    state = tuple(tuple(row) for row in game_state.board.board)
    return state


class QLearningAgent(Agent):
    def __init__(self, player_id, learning_rate=0.5, discount_factor=0.9, epsilon=1, epsilon_decay=0.95,
                 epsilon_min=0.1):
        super().__init__(player_id)
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def get_q_value(self, game_state, action):
        return self.q_table.get((game_state, action), 0)

    def get_action(self, game_state):
        # gets an action according to the policy
        if random.random() < self.epsilon:
            return random.choice(game_state.get_legal_actions())
        else:
            encoded_state = encode_board_into_one_dimension_array(game_state)
            legal_actions = game_state.get_legal_actions()
            q_values = {action: self.get_q_value(encoded_state, action) for action in legal_actions}
            return max(q_values) if q_values else 0

    def update_q_table(self, game_state, action, new_game_state):
        # this function calculated the value according to the RL formula
        encoded_game_state = encode_board_into_one_dimension_array(game_state)
        encoded_new_game_state = encode_board_into_one_dimension_array(new_game_state)

        old_value = (1 - self.learning_rate) * self.get_q_value(encoded_game_state, action)
        future_values = [self.get_q_value(encoded_new_game_state, a) for a in new_game_state.get_legal_actions()]
        best_future_value = max(future_values)if future_values else 0
        learned_value = calculate_reward(game_state) + self.discount_factor * self.get_q_value(encoded_new_game_state,
                                                                                               best_future_value)
        new_value = old_value + self.learning_rate * learned_value
        self.q_table[(game_state, action)] = new_value

    def update_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
