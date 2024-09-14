Connect Four Game
Introduction
Connect Four is a classic two-player connection game in which the players first choose a color and then take turns dropping colored discs from the top into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the next available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs.

In this project, we approach Connect Four as an AI problem, implementing several agents that use different strategies and learning algorithms to play the game. These include:

Minimax Agent: Utilizes the Minimax algorithm with alpha-beta pruning to calculate the best moves.
Q-learning Agent: Employs Q-learning, a model-free reinforcement learning algorithm to learn the strategy of the game from experiences.
Deep Q-Network (DQN) Agent: Implements a DQN, which uses deep neural networks to estimate Q-values and update policies accordingly.
Random Agent: Makes moves based on random selections for comparative purposes.
Repository Structure
The entire codebase is hosted within the src directory of the Git repository. Here's how to navigate and use the components:

Key Components
agents.py: Contains the implementations of the various agents (Minimax, Q-learning, DQN, Random).
game_state.py: Manages the state of the game board and checks for the winning condition.
game.py: Handles the game logic and interaction between the two agents.
four_in_a_row.py: The main executable script that sets up matches between agents and reports results.
Installation
Before running the game, ensure you have Python installed on your system. You can download it from python.org.

Running the Game
To run the game simulation, navigate to the src directory in your terminal or command prompt and execute the following command:

php
Copy code
python four_in_a_row.py <number_of_games> <agent_tag> <opponent_tag>
<number_of_games>: Replace this with the number of games you want the agents to play against each other.
<agent_tag> and <opponent_tag>: These should be replaced with the tags of the agents you wish to compete. Valid tags include deepq, q-learning, minimax, and random.
Example command:

Copy code
python four_in_a_row.py 100 deepq minimax
This command simulates 100 games between a Deep Q-Network agent and a Minimax agent.

Viewing Results
The game simulation will output the win rates and number of draws. Additionally, the win rates over time will be plotted if matplotlib is installed.

Conclusion
This project provides a comprehensive framework to explore various AI techniques in the classic Connect Four game, making it a valuable resource for understanding and developing AI game strategies.
