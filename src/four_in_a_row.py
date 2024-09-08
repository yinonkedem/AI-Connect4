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
    win_rates = []  # List to store win rate after each game

    for i in range(num_games):
        game_state = GameState()
        new_game = Game(agent, opponent_agent, game_state)
        winner = new_game.game_loop()
        if winner == 1:
            wins['Q-Learning'] += 1
        elif winner == 2:
            wins['Random'] += 1
        else:
            wins['Draw'] += 1

        # Calculate win rate and store it
        win_rates.append(wins['Q-Learning'] / (i + 1))

        if (i + 1) % display_games == 0:
            print(
                f"Games {i + 1}: Q-Learning Wins: {wins['Q-Learning']}, Random Wins: {wins['Random']}, Draws: {wins['Draw']}")

    return win_rates


def plot_results(results):
    plt.figure(figsize=(12, 6))
    adjusted_results = results[50:]  # Start plotting from game 11

    # Calculate moving average
    window_size = 50
    moving_average = np.convolve(adjusted_results, np.ones(window_size) / window_size, mode='valid')

    plt.plot(range(50, len(results)), adjusted_results, label='Win Rate of QLearning Agent', alpha=0.5, linestyle='-',
             color='dodgerblue')
    plt.plot(range(50 + window_size // 2, 50 + len(adjusted_results) - window_size // 2 + 1), moving_average,
             label='Moving Average', color='darkorange', linewidth=2)

    plt.xlabel('Number of Games')
    plt.ylabel('Win Rate')
    plt.title('Win Rate of QLearning Agent Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    num_games = 10000  # Number of games to simulate

    # Initialize agents
    q_learning_agent = QLearningAgent()
    random_agent = RandomAgent()

    # Simulate games between the trained Q-learning agent and the random agent
    print("Simulating games...")
    win_rates = simulate_games(num_games, q_learning_agent, random_agent, display_games=100)

    # Plot the results of the simulation
    print("Plotting results...")
    plot_results(win_rates)
