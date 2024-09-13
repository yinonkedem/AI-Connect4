import copy
from game_state import GameState
from src.agents import calculate_reward


class Game(object):
    def __init__(self, agent, opponent_agent, state=None):
        super(Game, self).__init__()
        self.agent = agent
        self.opponent_agent = opponent_agent
        self.state = GameState() if state is None else state

    def mainLoop(self):
        while not self.state.is_done():
            if self.state.player_about_to_play == 1:
                self.agentAction(self.agent)
            else:
                self.agentAction(self.opponent_agent)
        self.check_if_update_eps()
        return self.state.winner

    def check_if_update_eps(self):
        if self.agent.tag == 'q-Learning' or self.agent.tag == 'DeepQ-Learning':
            self.agent.update_epsilon()
        if self.opponent_agent.tag == 'q-Learning' or \
                self.opponent_agent.tag == 'DeepQ-Learning':
            self.opponent_agent.update_epsilon()

    def agentAction(self, agent):
        if agent.tag == 'q-Learning':
            action = self.agent.get_action(self.state)  # get the agent's chosen action for the current state
            old_state = self.state.deepcopy()
            self.state.apply_action(action)
            self.agent.update_q_table(old_state, action, self.state)

        elif agent.tag == 'DeepQ-Learning':
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