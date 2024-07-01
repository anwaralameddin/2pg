from __future__ import annotations

from functools import partial

from two_player_games.common import Turn
from two_player_games.model import Action, Change, Model, State

from . import MaxiMin


# TODO pylint: disable=too-many-locals
# TODO Refactor to avoid code duplication among the different maximin variants
class MaxiMinDefensive(MaxiMin[Action, State, Change]):
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
        # Utiliying d alongside f ensures the agent does not disregard
        # tactical actions in losing situations. This behavior is more
        # intuitive than that of `MaxiMinNaive`, but only useful if the
        # opponent is not playing optimally.
        # TODO Explain in more detail why this is the case

        # TODO This is OK for tic-tac-toe, but others might require different
        # depth(s).

        # Defensive: Looking for moves that maximise the opponent's reward to
        # block them if the agent is in a losing state.
        # TODO Instead, instantiate a new MaxiMinNaive for the opponent
        maximin_d = partial(self.maximin, depth=1, turn=-turn)

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
            if maximin_reward >= 0:
                maximin_actions = [
                    action
                    for reward, action in rewards_and_actions
                    if reward == maximin_reward
                ]
                maximin_action = (
                    maximin_actions[0] if maximin_actions else None
                )
                return maximin_reward, maximin_action

            # TODO Refactor this repeated code
            rewards_and_actions_d = [
                # Returns the reward of the opponent's actions
                model.peek_then_eval(action, maximin_d)
                for action in model.possible_actions
            ]
            # Determines the best action for the opponent to block it
            maximin_reward_d = (
                min(reward for reward, _ in rewards_and_actions_d)
                if rewards_and_actions_d
                else float("inf")
            )
            maximin_actions_d = [
                action
                for reward, action in rewards_and_actions_d
                if reward == maximin_reward_d
            ]
            maximin_action_d = (
                maximin_actions_d[0] if maximin_actions_d else None
            )
            return maximin_reward_d, maximin_action_d

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
        minimax_action = minimax_actions[0] if minimax_actions else None
        return minimax_reward, minimax_action
