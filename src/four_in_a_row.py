import copy

from agents import *
from game_state import GameState

import matplotlib.pyplot as plt
from collections import defaultdict

from src.board_display import SilentDisplay
from src.game import Game
import numpy as np

""""*** qlearning train ***"""

def train_q_learning_agent(num_episodes, agent, opponent_agent):
    for episode in range(num_episodes):
        game_state = GameState()  # Initialize a new game state
        while not game_state.is_done():
            current_state = copy.deepcopy(game_state)  # Make a deep copy of the current state before the action

            if game_state.player_about_to_play == agent.player_id:
                action = agent.get_action(current_state)
                game_state.apply_action(action)  # Apply the action to update the game state
                reward = game_state.calculate_reward()  # Calculate reward after applying the action
                next_state = copy.deepcopy(game_state)  # Capture the state after the action

                # Agent learns from the transition between states
                agent.learn(current_state, action, reward, next_state)

            else:  # Opponent's turn
                action = opponent_agent.get_action(game_state)
                game_state.apply_action(action)

            # Decay epsilon after each turn or game depending on learning strategy
            if game_state.is_done():
                agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)

        # Output the progress every 100 episodes
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}: Epsilon {agent.epsilon}")

    return agent


def simulate_games(num_games, agent, opponent_agent, display_games=100):
    wins = defaultdict(int)
    win_rates = []  # List to store win rate after each game

    for i in range(num_games):
        game_state = GameState()
        game_runner = Game(agent=agent, opponent_agent=opponent_agent, display=SilentDisplay(), state=game_state)
        winner = game_runner.game_loop()
        if winner == agent.player_id:
            wins['Q-Learning'] += 1
        elif winner == opponent_agent.player_id:
            wins['Random'] += 1
        else:
            wins['Draw'] += 1

        # Calculate win rate and store it
        win_rates.append(wins['Q-Learning'] / (i + 1))

        if (i + 1) % display_games == 0:
            print(f"Games {i + 1}: Q-Learning Wins: {wins['Q-Learning']}, Random Wins: {wins['Random']}, Draws: {wins['Draw']}")

    return win_rates

def plot_results(results):
    plt.figure(figsize=(12, 6))
    adjusted_results = results[50:]  # Start plotting from game 11

    # Calculate moving average
    window_size = 50
    moving_average = np.convolve(adjusted_results, np.ones(window_size)/window_size, mode='valid')

    plt.plot(range(50, len(results)), adjusted_results, label='Win Rate of QLearning Agent', alpha=0.5, linestyle='-', color='dodgerblue')
    plt.plot(range(50 + window_size//2, 50 + len(adjusted_results) - window_size//2 + 1), moving_average, label='Moving Average', color='darkorange', linewidth=2)

    plt.xlabel('Number of Games')
    plt.ylabel('Win Rate')
    plt.title('Win Rate of QLearning Agent Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    # Setup the number of episodes for training and games for simulation
    num_episodes = 1000  # Number of episodes to train the Q-learning agent
    num_games = 10000  # Number of games to simulate

    # Initialize agents
    q_learning_agent = QLearningAgent(player_id=1, learning_rate=0.1, discount_factor=0.9,
                                      epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01)
    random_agent = RandomAgent(player_id=2)

    # Train the Q-learning agent
    print("Training Q-Learning Agent...")
    trained_agent = train_q_learning_agent(num_episodes, q_learning_agent, random_agent)

    # Simulate games between the trained Q-learning agent and the random agent
    print("Simulating games...")
    win_rates = simulate_games(num_games, trained_agent, random_agent, display_games=100)

    # Plot the results of the simulation
    print("Plotting results...")
    plot_results(win_rates)


