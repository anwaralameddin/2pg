from __future__ import annotations

from functools import partial

from two_player_games.common import Turn
from two_player_games.model import Action, Change, Model, State

from . import MaxiMin


# TODO Refactor to avoid code duplication among the different maximin variants
class MaxiMinNaive(MaxiMin[Action, State, Change]):
    def maximin(
        self,
        model: Model[Action, State, Change],
        depth: int,
        turn: Turn,
    ) -> tuple[float, Action | None]:
        # https://en.wikipedia.org/wiki/Minimax#Pseudocode
        # Note: In some games, like Othello, a player may not have any valid
        # actions and pass their turn to the opponent without the game ending.
        # TODO Amend model implementations to ensure that game_over implies
        # no possible actions. Then, simplify the condition below.
        if model.is_over() or not model.possible_actions or depth <= 0:
            return model.reward(self.maximin_turn), None

        maximin_f = partial(self.maximin, depth=depth - 1, turn=-turn)

        if turn == self.maximin_turn:
            maximin_reward, maximin_action = float("-inf"), None
            # TODO Consider refactoring and using np.argmax
            for action in model.possible_actions:
                reward, _ = model.peek_then_eval(action, maximin_f)
                if reward > maximin_reward:
                    maximin_reward, maximin_action = reward, action
            return maximin_reward, maximin_action

        minimax_reward, minimax_action = float("inf"), None
        for action in model.possible_actions:
            reward, _ = model.peek_then_eval(action, maximin_f)
            if reward < minimax_reward:
                minimax_reward, minimax_action = reward, action
        return minimax_reward, minimax_action
