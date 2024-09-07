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

    def __init__(self, player_id, evaluation_function=None, depth=2):
        self.player_id = player_id
        self.depth = depth
        self.evaluation_function = evaluation_function

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class RandomAgent(Agent):
    def __init__(self, player_id):
        super().__init__(player_id=player_id, evaluation_function=None, depth=0)

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

# RL is an agent?
# class QLearningAgent(Agent):
#     def __init__(self, player_id, learning_rate=0.1, discount_factor=0.95,
#                  epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
#         super().__init__(player_id)
#         self.alpha = learning_rate  # Learning rate
#         self.gamma = discount_factor  # Discount factor
#         self.epsilon = epsilon  # Initial exploration rate
#         self.epsilon_min = epsilon_min
#         self.epsilon_decay = epsilon_decay
#         self.q_table = {}  # Q-values stored as a dictionary
#         self.player_id = player_id  # Player ID for identifying which player the agent is
#
#     def encode_state(self, board):
#         """
#         Encode the board state into a tuple which acts as a key for the Q-table.
#         Each cell's content is read row-wise to create a hashable state representation.
#         """
#         return tuple(tuple(row) for row in board.board)  # Convert board to a tuple of tuples
#
#     def get_legal_actions(self, board):
#         """
#         Extracts legal actions (column indices that are not full) using the board's method.
#         """
#         return board.get_valid_moves()  # Use the Board class's method to get valid moves
#
#     def get_action(self, state):
#         """
#         Choose an action using the epsilon-greedy strategy.
#         """
#         if random.random() < self.epsilon:
#             return random.choice(self.get_legal_actions(state.board))
#         else: # this is the evaluation function
#             state_encoded = self.encode_state(state.board)
#             q_values = {action: self.q_table.get((state_encoded, action), 0) for action in self.get_legal_actions(state.board)}
#             return max(q_values, key=q_values.get)  # Action with the highest Q-value
#
#     def learn(self, current_state, action, reward, next_state, done):
#         """
#         Updates the Q-table based on the agent's experience.
#         """
#         curr_state_encoded = self.encode_state(current_state.board)
#         next_state_encoded = self.encode_state(next_state.board)
#         best_future_action = max([self.q_table.get((next_state_encoded, a), 0) for a in self.get_legal_actions(next_state.board)], default=0)
#
#         current_q_value = self.q_table.get((curr_state_encoded, action), 0)
#         future_q_value = 0 if done else best_future_action
#         updated_q_value = current_q_value + self.alpha * (reward + self.gamma * future_q_value - current_q_value)
#
#         self.q_table[(curr_state_encoded, action)] = updated_q_value
#
#         # Epsilon decay
#         if done and self.epsilon > self.epsilon_min:
#             self.epsilon *= self.epsilon_decay


class QLearningAgent:
    def __init__(self, player_id, learning_rate=0.1, discount_factor=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.player_id = player_id
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def encode_state(self, board):
        state = tuple(tuple(row) for row in board.board)
        # Add more features to state representation here if needed
        return state

    def get_legal_actions(self, board):
        return board.get_valid_moves()

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.get_legal_actions(state.board))
        else:
            encoded_state = self.encode_state(state.board)
            legal_actions = self.get_legal_actions(state.board)
            q_values = {action: self.get_q_value(encoded_state, action) for action in legal_actions}
            return max(q_values, key=q_values.get) if q_values else None

    def learn(self, state, action, reward, next_state):
        current_state_encoded = self.encode_state(state.board)
        next_state_encoded = self.encode_state(next_state.board)
        future_rewards = [self.get_q_value(next_state_encoded, a) for a in next_state.get_legal_actions()]
        best_future_reward = max(future_rewards) if future_rewards else 0
        old_value = self.get_q_value(current_state_encoded, action)
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * best_future_reward - old_value)
        self.q_table[(current_state_encoded, action)] = new_value

        if state.is_done():
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def get_action(self, state):
        return self.choose_action(state)