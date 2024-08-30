class Game(object):
    def __init__(self, agent, opponent_agent, display, state):
        super(Game, self).__init__()
        self.agent = agent
        self.display = display
        self.opponent_agent = opponent_agent
        self._state = state

    def _game_loop(self):
        while not self._state.done:
            action = self.agent.get_action(self._state)  # get the agent's chosen action for the current state
            self._state.apply_action(action)
            opponent_action = self.opponent_agent.get_action(self._state)
            self._state.apply_opponent_action(opponent_action)
            self.display.update_state(self._state, action, opponent_action)
        return self._state.winner
