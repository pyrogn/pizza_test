"""Tests for CLI application
Tests are very basic and might be improved by exact matching
"""
import functools
import os

import pytest
from click.testing import CliRunner

from pizza.cli import cli
from pizza.pizza_menu import pizza_menu

from .help_funcs import all_pizzas_parameters, all_types_delivery

os.environ["LATENCY_ENABLED"] = "0"


@pytest.fixture()
def runner():
    """Run CliRunner for pizza app with required args"""

    @functools.wraps(runner)
    def cli_run(args: list[str]) -> tuple[int, list[str]]:
        """args: args to run CliRunner
        Returns:
            exit_code: exit code of command. 0 is pass
            split_result: result of command splitted by rows
        """
        runner = CliRunner()
        result = runner.invoke(cli, args)
        exit_code = result.exit_code
        split_result = result.output.strip().split("\n")
        return exit_code, split_result

    return cli_run


pizza_sizes_lines = 1  # extra line under menu about pizza sizes available
info_lines = 1  # info back to user what he orders


def test_menu(runner):
    """Test that cli prints all pizzas from the menu"""
    # result = runner.invoke(cli, ["menu"])
    exit_code, split_result = runner(["menu"])
    assert exit_code == 0
    assert len(split_result) == pizza_sizes_lines + len(
        pizza_menu,
    )


@all_types_delivery
@all_pizzas_parameters
def test_pizza_order(is_delivery, pizza_class, runner):
    """Test that you can order pizzas and output matches target number of rows"""
    pizza_name = pizza_class.get_name()
    params_cli = (
        ["order", pizza_name, "--delivery"] if is_delivery else ["order", pizza_name]
    )
    exit_code, split_result = runner(params_cli)
    num_actions = 2  # bake + deliver/pick up
    assert exit_code == 0
    assert len(split_result) == info_lines + num_actions


@all_pizzas_parameters
def test_pizza_wrong_size(pizza_class, runner):
    """Test that program don't crash on unknown pizza size
    and has expected number of lines"""
    pizza_name = pizza_class.get_name()
    exit_code, split_result = runner(
        ["order", pizza_name, "--size", "definitely_unknown_size"],
    )
    lines_info_message_wrong_pizza = 1
    assert exit_code == 0
    assert len(split_result) == lines_info_message_wrong_pizza


@all_types_delivery
def test_pizza_incorrect_order(is_delivery, runner):
    """Test that you can order pizzas and output matches target number of rows"""
    pizza_name = "some_definitely_unknown_pizza"
    params_cli = (
        ["order", pizza_name, "--delivery"] if is_delivery else ["order", pizza_name]
    )
    exit_code, split_result = runner(params_cli)
    assert exit_code == 0
    assert len(split_result) == pizza_sizes_lines + info_lines + len(
        pizza_menu,
    )
