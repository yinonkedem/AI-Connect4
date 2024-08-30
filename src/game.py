from enum import Enum


class Action(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3


class Game(object):
    def __init__(self, agent, opponent_agent, display, num_of_players,board, sleep_between_actions=False):
        super(Game, self).__init__()
        self.sleep_between_actions = sleep_between_actions
        self.agent = agent
        self.display = display
        self.board = board
        self.opponent_agent = opponent_agent
        self._state = None
        self._should_quit = False
        self.players_list = []
        self.num_of_players = num_of_players

    def run(self, initial_state):
        self._should_quit = False
        self._state = initial_state
        self.display.initialize(initial_state)
        for i in range(self.num_of_players):
            self.players_list.append(i+1)
        return self._game_loop()

    def quit(self):
        self._should_quit = True
        self.agent.stop_running()
        self.opponent_agent.stop_running()

    def _game_loop(self):
        while not self._state.done and not self._should_quit:
            #for player in self.players_list:
            self.display.mainloop_iteration()
            action = self.agent.get_action(self._state)  # get the possible actions for the current state
            self._state.apply_action(action)
            opponent_action = self.opponent_agent.get_action(self._state)
            self._state.apply_opponent_action(opponent_action)
            self.display.update_state(self._state, action, opponent_action)
        return self._state.score, self._state.max_tile
