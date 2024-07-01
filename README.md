# Two-Player Game (2PG)

[![CI](https://github.com/anwaralameddin/2pg/actions/workflows/ci.yml/badge.svg)](https://github.com/anwaralameddin/2pg/actions/workflows/ci.yml)

A testbed for two-player game agents. It's currently under development and
is limited to three games: Connect Four, Othello, and Tic Tac Toe.


## Usage

In a <code>Python 3.11</code> environment, install the requirements
```
pip install -r requirements.txt
```
and run the package
```
python -m two_player_games -m <model> -v <view> -a1 <agent1> [-d1 <depth1>] -a2 <agent2> [-d2 <depth2>]
```
### Supported Games

- [Connect Four](https://en.wikipedia.org/wiki/Connect_Four) (<code>connect4</code>)
- [Othello](https://en.wikipedia.org/wiki/Reversi#Othello) (<code>othello</code>)
- [Tic Tac Toe](https://en.wikipedia.org/wiki/Tic-tac-toe) (<code>tictactoe</code>)

### Supported Views

- Hidden (<code>hidden</code>)
- [Pygame](https://www.pygame.org/news) (<code>pygame</code>)

### Supported Agents

- [X] Human (<code>human</code>)
- [X] Random (<code>random</code>)
- [ ] [Maximin](https://en.wikipedia.org/wiki/Minimax)
    - [X] Naive: (<code>maximin-naive</code>)
    - [X] Defensive: (<code>maximin-defensive</code>)
    - [X] Stochastic: (<code>maximin-stochastic</code>)
    - [ ] [Negamax](https://en.wikipedia.org/wiki/Negamax)
    - [ ] [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
- [ ] [Monte Carlo Tree Search (MCTS)](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
<!-- TODO Consider implementing the following agents -->
<!-- - [ ] [Deep Learning](https://en.wikipedia.org/wiki/Deep_learning) -->
<!-- - [ ] [Evolutionary Algorithm](https://en.wikipedia.org/wiki/Evolutionary_algorithm) -->
<!-- - [ ] [Genetic Algorithm (GA)](https://en.wikipedia.org/wiki/Genetic_algorithm) -->
<!-- - [ ] [Heuristic](https://en.wikipedia.org/wiki/Heuristic_(computer_science)) -->
<!-- - [ ] [Iterative Deepening](https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search) -->
<!-- - [ ] [Killer Heuristic](https://en.wikipedia.org/wiki/Killer_heuristic) -->
<!-- - [ ] [Late Move Reduction (LMR)](https://en.wikipedia.org/wiki/Late_move_reduction) -->
<!-- - [ ] [Null Move Heuristic](https://en.wikipedia.org/wiki/Null-move_heuristic) -->
<!-- - [ ] [Principal Variation Search (PVS)](https://en.wikipedia.org/wiki/Principal_variation_search) -->
<!-- - [ ] [Quiescence Search](https://en.wikipedia.org/wiki/Quiescence_search) -->
<!-- - [ ] [Reinforcement Learning (RL)](https://en.wikipedia.org/wiki/Reinforcement_learning) -->
<!-- - [ ] [Transposition Table](https://en.wikipedia.org/wiki/Transposition_table) -->


### Example

```
python -m two_player_games -m tictactoe -v pygame -a1 human -a2 maximin-naive -d2 6
```
