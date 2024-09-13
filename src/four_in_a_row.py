import copy

from agents import *
from game_state import GameState

import matplotlib.pyplot as plt
from collections import defaultdict

from board_display import SilentDisplay
from game import Game
import numpy as np


def simulate_games(num_games, agent, opponent_agent, display_games=100):
    wins = defaultdict(int)
    win_rates = defaultdict(list)  # Dictionary to store win rate after each game for each agent

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
        win_rates[opponent_agent.tag].append(wins[opponent_agent.tag] / (i + 1))

        if (i + 1) % display_games == 0:
            print(f"Games {i + 1}: {agent.tag} Wins: {wins[agent.tag]}, {opponent_agent.tag} Wins: {wins[opponent_agent.tag]}, Draws: {wins['Draw']}")

    return win_rates


def plot_results(win_rates):
    plt.figure(figsize=(12, 8))
    colors = ['blue', 'orange']  # Colors for the lines
    for idx, (tag, rates) in enumerate(win_rates.items()):
        x_values = list(range(len(rates)))
        plt.plot(x_values, rates, label=f'{tag} Win Rate', color=colors[idx])

        # Adding numeric labels to each data point
        for i, rate in enumerate(rates):
            plt.annotate(f'{rate:.2f}', (x_values[i], rates[i]), textcoords="offset points", xytext=(0,10), ha='center', color=colors[idx])

    plt.title('Win Rates Over Time')
    plt.xlabel('Number of Games')
    plt.ylabel('Win Rate')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    num_games = 1000  # Number of games to simulate

    # Initialize agents
    q_learning_agent = QLearningAgent('q-Learning', 1)
    mini_max_agent = MinmaxAgentWithPruning('MiniMax', 2)
    deep_q_learning_agent = DQNAgent('DeepQ-Learning', 1, 42,7,20000)
    random_agent = RandomAgent('Random', 2)

    # Simulate games between the trained Q-learning agent and the random agent
    print("Simulating games...")
    win_rates = simulate_games(num_games, deep_q_learning_agent, mini_max_agent, display_games=100)

    # Plot the results of the simulation
    print("Plotting results...")
    plot_results(win_rates)
