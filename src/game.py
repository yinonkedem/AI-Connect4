class Game(object):
    def __init__(self, agent, opponent_agent, display, state):
        super(Game, self).__init__()
        self.agent = agent
        self.display = display
        self.opponent_agent = opponent_agent
        self._state = state

    def game_loop(self):  # todo only one player each turn
        while not self._state.done:
            action = self.agent.get_action(self._state)  # get the agent's chosen action for the current state
            self._state.apply_action(action)
            opponent_action = self.opponent_agent.get_action(self._state)
            self._state.apply_action(opponent_action)
            self.display.update_state(self._state, action, opponent_action)
            print ("\n\n")
        return self._state.winner
