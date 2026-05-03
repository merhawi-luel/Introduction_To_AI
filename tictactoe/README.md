# Tic-Tac-Toe AI Game

A classic Tic-Tac-Toe game implemented in Python using Pygame, featuring an AI opponent that uses the Minimax algorithm with alpha-beta pruning.

## Features

- **Human vs AI Gameplay**: Play as X against an unbeatable AI opponent (O)
- **Graphical Interface**: Clean, modern UI built with Pygame
- **AI Intelligence**: Uses Minimax algorithm with alpha-beta pruning for optimal play
- **Game Statistics**: Tracks wins, losses, and draws
- **Smooth Animations**: Fade-in effects for moves and win line highlighting

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Make sure you have Python installed on your system
2. Install Pygame using pip:
   ```bash
   pip install pygame
   ```

## How to Run

1. Navigate to the tictactoe directory
2. Run the game:
   ```bash
   python tictactoe.py
   ```

## Gameplay

- You play as X (blue) and always go first
- Click on any empty cell to make your move
- The AI (O, red) will respond automatically
- The game ends when someone gets three in a row, column, or diagonal, or when the board is full (draw)

## AI Algorithm

The AI uses the Minimax algorithm with alpha-beta pruning to determine the optimal move. This makes the AI unbeatable - it will never lose and will win whenever possible.

## Controls

- **Mouse Click**: Make a move by clicking on an empty cell
- **Close Window**: Exit the game

## Game States

- **Your turn**: Human player's turn to move
- **AI thinking**: AI is calculating its move
- **Game Over**: Displays the winner or if it's a draw

Enjoy playing against the AI!