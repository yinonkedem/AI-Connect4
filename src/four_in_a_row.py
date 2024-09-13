import copy

from agents import *
from game_state import GameState

import matplotlib.pyplot as plt
from collections import defaultdict

from game import Game
import sys


def simulate_games(num_games, agent, opponent_agent, display_games=100):
    wins = defaultdict(int)
    win_rates = defaultdict(
        list)  # Dictionary to store win rate after each game for each agent

    for i in range(num_games):
        game_state = GameState()
        new_game = Game(agent, opponent_agent, game_state)
        winner = new_game.mainLoop()

        if winner == 1:
            wins[agent.tag] += 1
        elif winner == 2:
            wins[opponent_agent.tag] += 1
        else:
            wins['Draw'] += 1

        # Calculate win rate for each agent and store it
        win_rates[agent.tag].append(wins[agent.tag] / (i + 1))
        win_rates[opponent_agent.tag].append(
            wins[opponent_agent.tag] / (i + 1))

        if (i + 1) % display_games == 0:
            print(
                f"Games {i + 1}: {agent.tag} Wins: {wins[agent.tag]}, {opponent_agent.tag} Wins: {wins[opponent_agent.tag]}, Draws: {wins['Draw']}")

    return win_rates


def plot_results(win_rates):
    plt.figure(figsize=(12, 8))
    colors = ['blue', 'orange']  # Colors for the lines
    for idx, (tag, rates) in enumerate(win_rates.items()):
        x_values = list(range(len(rates)))
        plt.plot(x_values, rates, label=f'{tag} Win Rate', color=colors[idx])

    plt.title('Win Rates Over Time')
    plt.xlabel('Number of Games')
    plt.ylabel('Win Rate')
    plt.legend()
    plt.grid(True)
    plt.show()


def validate_tag(input_tag):
    valid_tags = ['deepq', 'q-learning', 'minimax', 'random']
    if input_tag.lower() in valid_tags:
        return input_tag.lower()
    else:
        print(f"Invalid tag. The valid options are: {', '.join(valid_tags)}")
        sys.exit(1)


def validate_number_of_games(input_number):
    try:
        number = int(input_number)
        if number > 0:
            return number
        else:
            raise ValueError
    except ValueError:
        print(
            "Please provide a valid positive integer for the number of games.")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python four_in_a_row.py <number_of_games> <agent_tag> "
              "<opponent_tag>")
        sys.exit(1)

    num_games = validate_number_of_games(sys.argv[1])
    agent_tag = validate_tag(sys.argv[2])
    opponent_tag = validate_tag(sys.argv[3])

    # Initialize agents with IDs based on input order
    agents = {
        'deepq': DQNAgent('DeepQ-Learning', 0),  # Placeholder for ID
        'q-learning': QLearningAgent('q-Learning', 0),  # Placeholder for ID
        'minimax': MinmaxAgentWithPruning('MiniMax', 0),  # Placeholder for ID
        'random': RandomAgent('Random', 0)  # Placeholder for ID
    }

    # Assign IDs based on the order in which they are specified
    agents[agent_tag].id = 1
    agents[opponent_tag].id = 2

    agent = agents[agent_tag]
    opponent = agents[opponent_tag]

    # Simulate games
    print("Simulating games...")
    win_rates = simulate_games(num_games, agent, opponent, num_games//10)

    # Plot the results of the simulation
    print("Plotting results...")
    plot_results(win_rates)
