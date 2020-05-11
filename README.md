# Expendibots

A game-playing AI for the Expendibots board game, built as part of the University of Melbourne's COMP30024 (Artificial Intelligence) course. The project includes both a single-player puzzle solver and a competitive two-player AI agent.

## About the Game

Expendibots is a two-player strategy game played on an 8x8 grid. Each player controls 12 stackable pieces and can perform two types of actions:

- **Move** -- Slide pieces orthogonally across the board, optionally stacking with friendly pieces
- **Boom** -- Trigger a chain-reaction explosion that destroys all adjacent pieces (including your own)

A player wins by eliminating all of their opponent's pieces.

## Project Structure

The project is split into two parts:

### Part A -- Puzzle Solver

An A\* search algorithm that finds optimal sequences of moves and explosions to eliminate all opponent pieces from a given board state. Uses Manhattan distance as a heuristic for target prioritization.

### Part B -- Game AI (Frostbyte)

A competitive AI agent that plays full games against other bots. Key features:

- **Four-ply minimax search** -- Looks four moves ahead (two full turns) to evaluate positions
- **Positional heuristics** -- Uses weight tables derived from 10,000 simulated games to score board positions
- **Optimal stopping** -- Prunes the search space by evaluating ~37% of available moves at each depth level
- **Explosion evaluation** -- Only triggers boom actions when they result in an immediate win or improve the piece ratio

## Tech Stack

- **Language:** Python 3
- **Algorithms:** A\* search, minimax with pruning, heuristic evaluation

## Usage

Run the puzzle solver (Part A):

```bash
python -m search < input.json
```

Run a game between two AI players (Part B):

```bash
python -m referee frostbyte opponent_bot
```

## Authors

Connor Cates & Matthew Saliba
