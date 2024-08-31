from board_display import NormalDisplay
from game import Game
from agents import MinmaxAgent
from game_state import GameState


def main():
    display = NormalDisplay()
    agent = MinmaxAgent()
    opponent_agent = MinmaxAgent()
    state = GameState()
    game_runner = Game(agent=agent, opponent_agent=opponent_agent, display=display, state=state)
    winning_player = game_runner.game_loop()
    print("the winner is :" + str(winning_player))


if __name__ == '__main__':
    main()
