import copy
from game_state import GameState
from src.agents import calculate_reward


class Game(object):
    def __init__(self, agent, opponent_agent, state=None):
        super(Game, self).__init__()
        self.agent = agent
        self.opponent_agent = opponent_agent
        self.state = GameState() if state is None else state

    def game_loop_qlearn_first(self):
        while not self.state.is_done():
            if self.state.player_about_to_play == 1:
                action = self.agent.get_action(self.state)  # get the agent's chosen action for the current state
                old_state = self.state.deepcopy()
                self.state.apply_action(action)
                self.agent.update_q_table(old_state, action, self.state)
            else:
                opponent_action = self.opponent_agent.get_action(self.state)
                self.state.apply_action(opponent_action)
        self.agent.update_epsilon()
        return self.state.winner

    def game_loop_qlearn_second(self):
        while not self.state.is_done():
            if self.state.player_about_to_play == 1:
                action = self.agent.get_action(self.state)  # get the agent's chosen action for the current state
                self.state.apply_action(action)
            else:
                opponent_action = self.opponent_agent.get_action(self.state)
                old_state = self.state.deepcopy()
                self.state.apply_action(opponent_action)
                self.opponent_agent.update_q_table(old_state, opponent_action, self.state)

        self.opponent_agent.update_epsilon()
        return self.state.winner

    def game_loop_without_learning(self):
        while not self.state.is_done():
            if self.state.player_about_to_play == self.agent.player_id:
                action = self.agent.get_action(self.state)  # get the agent's chosen action for the current state
                self.state.apply_action(action)
            else:
                opponent_action = self.opponent_agent.get_action(self.state)
                self.state.apply_action(opponent_action)
        return self.state.winner

    def game_loop_DQN(self):
        while not self.state.is_done():
            current_player = self.state.player_about_to_play
            if current_player == 1:

                action = self.agent.get_action(self.state)  # get the agent's chosen action for the current state
                old_state = self.state.deepcopy()
                self.state.apply_action(action)

                # Store the transition in the DQN agent's replay buffer
                self.agent.store_transition(old_state, action,
                                            calculate_reward(self.state), self.state,
                                            self.state.is_done())

                # Perform a learning step if there are enough samples in the replay buffer
                if len(self.agent.replay_buffer.buffer) >= self.agent.batch_size:
                    self.agent.update_NN()

            else:
                opponent_action = self.opponent_agent.get_action(self.state)
                self.state.apply_action(opponent_action)

        # After the game ends, optionally update the exploration rate
        self.agent.update_epsilon()
        return self.state.winner