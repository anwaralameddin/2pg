from __future__ import annotations

import logging
import sys
from argparse import ArgumentParser

from .agent.arg import AgentArg
from .common import Turn
from .model.arg import ModelArg
from .presenter import Presenter
from .view.arg import ViewArg

logger = logging.getLogger(__name__)

__version__ = "0.1.0"


def main() -> None:
    logging.basicConfig(
        stream=sys.stderr,
        encoding="utf-8",
        level=logging.DEBUG,
    )
    arg_parser = ArgumentParser(
        description="A testbed for two-player game agents.",
    )
    arg_parser.add_argument(
        "-m",
        "--model",
        dest="model",
        type=ModelArg,
        choices=ModelArg,
        required=True,
    )
    arg_parser.add_argument(
        "-v",
        "--view",
        dest="view",
        type=ViewArg,
        choices=ViewArg,
        required=True,
    )
    arg_parser.add_argument(
        "-a1",
        "--first-agent",
        dest="first_agent",
        type=AgentArg,
        choices=AgentArg,
        required=True,
    )
    arg_parser.add_argument(
        "-a2",
        "--second-agent",
        dest="second_agent",
        type=AgentArg,
        choices=AgentArg,
        required=True,
    )
    arg_parser.add_argument(
        "-d1",
        "--first-depth",
        dest="first_depth",
        type=int,
    )
    arg_parser.add_argument(
        "-d2",
        "--second-depth",
        dest="second_depth",
        type=int,
    )

    args = arg_parser.parse_args()
    # TODO Variable types are already specified in the `add_argument` method;
    # Why aren't `args` members typed accordingly?
    arg_model: ModelArg = args.model
    arg_view: ViewArg = args.view
    arg_first_agent: AgentArg = args.first_agent
    arg_second_agent: AgentArg = args.second_agent
    arg_first_depth: int = args.first_depth if args.first_depth else 0
    arg_second_depth: int = args.second_depth if args.second_depth else 0

    model = arg_model.get_model()
    config = arg_model.get_config()
    category = config.category
    view = arg_view.get_view()(config)

    # TODO move these match statements to agent/arg.py
    match arg_first_agent:
        case AgentArg.HUMAN:
            first_agent = arg_first_agent.get_agent(category)(view)
        case (
            AgentArg.MAXIMIN_NAIVE
            | AgentArg.MAXIMIN_DEFENSIVE
            | AgentArg.MAXIMIN_STOCHASTIC
        ):
            first_agent = arg_first_agent.get_agent(category)(
                arg_first_depth,
                Turn.FIRST,
            )
        case _:
            first_agent = arg_first_agent.get_agent(category)()

    match arg_second_agent:
        case AgentArg.HUMAN:
            second_agent = arg_second_agent.get_agent(category)(view)
        case (
            AgentArg.MAXIMIN_NAIVE
            | AgentArg.MAXIMIN_DEFENSIVE
            | AgentArg.MAXIMIN_STOCHASTIC
        ):
            second_agent = arg_second_agent.get_agent(category)(
                arg_second_depth,
                Turn.SECOND,
            )
        case _:
            second_agent = arg_second_agent.get_agent(category)()

    presenter = Presenter(
        model(),
        first_agent,
        second_agent,
        view,
    )
    presenter.main_loop()


if __name__ == "__main__":
    main()
