# TODO

## Performance

- [ ] <code>Maximin</code> can be simplified by replacing <code>model.peek_then_eval(action, f)</code> with <code>copy=model.deepcopy()</code>, <code>model.play(action)</code>, <code>f(model)</code> and <code>model=copy</code>. Benchmark the performance of the two approaches.
- [ ] The models are slow, especially for a simple game like tic-tac-toe. Consider looking for more efficient algorithms.

## Features

- [ ] Implement the following agents:
  - [ ] [Monte Carlo Tree Search (MCTS)](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
  - [ ] RL solvers

- [ ] Incorporate CPU and GPU acceleration.

- [ ] Improve the command line interface. In particular, allow the user to specify the agent and depth using the same option, e.g. <code>-a1 maximin-naive 6</code> instead of <code>-a1 maximin-naive -d1 6</code>.

- [ ] Add <code>batch</code> mode, allowing the possibility to provide and play a list of actions.

- [ ] Visualise the agent's strategies.

- [ ] Add a <code>gui</code> feature, which corresponds to enabling the <code>pygame</code> View

## Testing

- [ ] Add docstring tests
- [ ] Add unit tests and enable <code>pytest</code>'s GitHub Actions workflow
- [ ] Utilise docstring tests
- [ ] Enable <code>pylint</code> <code>FIXME</code> errors

## Documentation

- [ ] Document the design and characteristics of the different agents.
- [ ] Complete and generate documentation

## Refactor

- [ ] <code>peek_then_eval</code> is repeated in the three games and can be moved to the <code>Model</code> class.

## Appearance

- [ ] In the view module, aAccept functions to render pieces for different games. For example, X and O for Tic-Tac-Toe.
- [ ] Improve logs
