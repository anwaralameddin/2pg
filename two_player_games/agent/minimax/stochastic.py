from __future__ import annotations

import random
from functools import partial

from two_player_games.common import Turn
from two_player_games.model import Action, Change, Model, State

from . import MaxiMin


# TODO Refactor to avoid code duplication among the different maximin variants
class MaxiMinStochastic(MaxiMin[Action, State, Change]):
    def maximin(
        self,
        model: Model[Action, State, Change],
        depth: int,
        turn: Turn,
    ) -> tuple[float, Action | None]:
        # Note: In some games, like Othello, a player may not have any valid
        # actions and pass their turn to the opponent without the game ending.
        # TODO Amend model implementations to ensure that game_over implies
        # no possible actions. Then, simplify the condition below.
        if model.is_over() or not model.possible_actions or depth <= 0:
            return model.reward(self.maximin_turn), None

        maximin_f = partial(self.maximin, depth=depth - 1, turn=-turn)

        rewards_and_actions = [
            (model.peek_then_eval(action, maximin_f)[0], action)
            for action in model.possible_actions
        ]

        if turn == self.maximin_turn:
            maximin_reward = (
                max(reward for reward, _ in rewards_and_actions)
                if rewards_and_actions
                else float("-inf")
            )
            maximin_actions = [
                action
                for reward, action in rewards_and_actions
                if reward == maximin_reward
            ]
            maximin_action = (
                random.choice(maximin_actions) if maximin_actions else None
            )
            return maximin_reward, maximin_action

        minimax_reward = (
            min(reward for reward, _ in rewards_and_actions)
            if rewards_and_actions
            else float("inf")
        )
        minimax_actions = [
            action
            for reward, action in rewards_and_actions
            if reward == minimax_reward
        ]
        minimax_action = (
            random.choice(minimax_actions) if minimax_actions else None
        )
        return minimax_reward, minimax_action
