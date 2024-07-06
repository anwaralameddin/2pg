from __future__ import annotations

from functools import partial

from two_player_games.common import Turn
from two_player_games.model import Action, Change, Model, State

from . import MaxiMin


# TODO Benchmark and compare this agent with the naive maximin one
# TODO Refactor to avoid code duplication among the different maximin variants
class AlphaBetaPruning(MaxiMin[Action, State, Change]):
    # pylint: disable=too-many-arguments
    def maximin(
        self,
        model: Model[Action, State, Change],
        depth: int,
        turn: Turn,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
    ) -> tuple[float, Action | None]:
        # https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
        if model.is_over() or not model.possible_actions or depth <= 0:
            return model.reward(self.maximin_turn), None

        if turn == self.maximin_turn:
            maximin_reward, maximin_action = float("-inf"), None
            # TODO Consider refactoring and using np.argmax
            for action in model.possible_actions:
                maximin_f = partial(
                    self.maximin,
                    depth=depth - 1,
                    turn=-turn,
                    alpha=alpha,
                    beta=beta,
                )
                reward, _ = model.peek_then_eval(action, maximin_f)
                if reward > maximin_reward:
                    maximin_reward, maximin_action = reward, action
                if maximin_reward > beta:
                    break
                alpha = max(alpha, maximin_reward)
            return maximin_reward, maximin_action

        minimax_reward, minimax_action = float("inf"), None
        for action in model.possible_actions:
            maximin_f = partial(
                self.maximin,
                depth=depth - 1,
                turn=-turn,
                alpha=alpha,
                beta=beta,
            )
            reward, _ = model.peek_then_eval(action, maximin_f)
            if reward < minimax_reward:
                minimax_reward, minimax_action = reward, action
            if minimax_reward < alpha:
                break
            beta = min(beta, minimax_reward)
        return minimax_reward, minimax_action
