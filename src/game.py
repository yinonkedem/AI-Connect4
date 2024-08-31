class Game(object):
    def __init__(self, agent, opponent_agent, display, state):
        super(Game, self).__init__()
        self.agent = agent
        self.display = display
        self.opponent_agent = opponent_agent
        self.state = state

    def game_loop(self):  # todo only one player each turn
        while not self.state.is_done():
            if self.state.player_about_to_play ==1:
                action = self.agent.get_action(self.state)  # get the agent's chosen action for the current state
                self.state.apply_action(action)
            else:
                opponent_action = self.opponent_agent.get_action(self.state)
                self.state.apply_action(opponent_action)
            self.display.update_state(self.state)
            print ("\n\n")
        self.display.update_state(self.state, True)
        return self.state.winner
