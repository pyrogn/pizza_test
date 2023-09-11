"""Tests for CLI application.

Tests are very basic and might be improved by exact matching.
"""
import os

import pytest
from click.testing import CliRunner

from pizza.cli import cli
from pizza.constants import (
    INFO_LINES,
    INFO_MESSAGE_WRONG_PIZZA_LINES,
    NUM_ACTIONS_LINES,
    PIZZA_SIZES_LINES,
    TEST_LATENCY_S,
)
from pizza.decorators import LogTimeDecorator
from pizza.pizza_menu import pizza_menu

from .help_funcs import all_pizzas_parameters, all_types_delivery

os.environ["LATENCY_ENABLED"] = "0"


@pytest.fixture()
def runner():
    """Factory for a function to run CliRunner."""

    def cli_run(args: list[str]) -> tuple[int, list[str]]:
        """Run CliRunner for pizza app with required args.

        Args:
            args: args to run CliRunner

        Returns:
            exit_code: exit code of command. 0 is pass
            split_result: result of command splitted by rows.
        """
        runner = CliRunner()
        result = runner.invoke(cli, args)
        exit_code = result.exit_code
        split_result = result.output.strip().split("\n")
        return exit_code, split_result

    return cli_run


@pytest.fixture(name="enable_latency")
def _set_env_vars_for_latency():
    """Make latency smaller but still test that it exists"""
    os.environ["LATENCY_ENABLED"] = "1"
    os.environ["LATENCY_FOR_TEST"] = "1"


def test_menu(runner):
    """Test that cli prints all pizzas from the menu."""
    exit_code, split_result = runner(["menu"])
    assert exit_code == 0
    assert len(split_result) == PIZZA_SIZES_LINES + len(
        pizza_menu,
    )


@all_types_delivery
@all_pizzas_parameters
def test_pizza_order(is_delivery, pizza_class, runner):
    """Usual order of all pizzas and all types of delivery

    1. No latency added to actions
    2. Exit code = success
    3. Number of lines as expected
    """
    pizza_name = pizza_class.get_name()
    params_cli = (
        ["order", pizza_name, "--delivery"] if is_delivery else ["order", pizza_name]
    )
    (exit_code, split_result), execution_time = LogTimeDecorator()(runner)(
        args=params_cli,
    )

    assert execution_time < TEST_LATENCY_S  # without latency, it is about .5 ms
    assert exit_code == 0
    assert len(split_result) == INFO_LINES + NUM_ACTIONS_LINES


@all_pizzas_parameters
def test_pizza_wrong_size(pizza_class, runner):
    """Test that program don't crash on unknown pizza size."""
    pizza_name = pizza_class.get_name()
    exit_code, split_result = runner(
        ["order", pizza_name, "--size", "definitely_unknown_size"],
    )
    assert exit_code == 0
    assert len(split_result) == INFO_MESSAGE_WRONG_PIZZA_LINES


@all_types_delivery
def test_pizza_incorrect_order(is_delivery, runner):
    """Test that you can order pizzas and output matches target number of rows."""
    pizza_name = "some_definitely_unknown_pizza"
    params_cli = (
        ["order", pizza_name, "--delivery"] if is_delivery else ["order", pizza_name]
    )
    exit_code, split_result = runner(params_cli)
    assert exit_code == 0
    assert len(split_result) == PIZZA_SIZES_LINES + INFO_LINES + len(
        pizza_menu,
    )


# testing all combinations might be unnecessary
@all_pizzas_parameters
@all_types_delivery
@pytest.mark.usefixtures("enable_latency")
def test_latency_exists(pizza_class, is_delivery, runner):
    """Test that latency is applied to heavy tasks"""
    pizza_name = pizza_class.get_name()
    params_cli = (
        ["order", pizza_name, "--delivery"] if is_delivery else ["order", pizza_name]
    )
    _, execution_time = LogTimeDecorator()(runner)(args=params_cli)
    assert execution_time > TEST_LATENCY_S
