from __future__ import annotations

from enum import StrEnum

from two_player_games.common import Category


class AgentArg(StrEnum):
    # GENEROUS = "generous"
    # GREEDY = "greedy"
    HUMAN = "human"
    MAXIMIN_NAIVE = "maximin-naive"
    MAXIMIN_DEFENSIVE = "maximin-defensive"
    MAXIMIN_STOCHASTIC = "maximin-stochastic"
    MAXIMIN_ALPHA_BETA_PRUNING = "maximin-alpha-beta"
    RANDOM = "random"

    # pylint: disable=import-outside-toplevel,too-many-return-statements
    def get_agent(self, category: Category) -> type:
        match self:
            case AgentArg.HUMAN:
                match category:
                    case Category.HORIZONTAL_BOARD:
                        from .human.board.horizontal import (
                            HorizontalBoardHuman,
                        )

                        return HorizontalBoardHuman
                    case Category.VERTICAL_BOARD:
                        from .human.board.vertical import VerticalBoardHuman

                        return VerticalBoardHuman
                    case _:
                        raise NotImplementedError(
                            f"Human-agent is not implemented for {category}",
                        )
            # TODO Move all MAXIMIN variants to a separate module, e.g.
            # two_player_games/agent/minimax/args.py
            case AgentArg.MAXIMIN_NAIVE:
                from .minimax.naive import MaxiMinNaive

                return MaxiMinNaive

            case AgentArg.MAXIMIN_DEFENSIVE:
                from .minimax.defensive import MaxiMinDefensive

                return MaxiMinDefensive

            case AgentArg.MAXIMIN_STOCHASTIC:
                from .minimax.stochastic import MaxiMinStochastic

                return MaxiMinStochastic

            case AgentArg.MAXIMIN_ALPHA_BETA_PRUNING:
                from .minimax.alpha_beta_pruning import AlphaBetaPruning

                return AlphaBetaPruning
            case AgentArg.RANDOM:
                from .random import Random

                return Random
