import copy


class Game(object):
    def __init__(self, agent, opponent_agent, state):
        super(Game, self).__init__()
        self.agent = agent
        self.opponent_agent = opponent_agent
        self.state = state

    def game_loop(self):
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
