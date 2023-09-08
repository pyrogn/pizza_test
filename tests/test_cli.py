"""Tests for CLI application
Tests are very basic and might be improved by exact matching
"""
import os
import pytest
from click.testing import CliRunner

from pizza.cli import cli
from pizza.pizza_menu import pizza_menu

from .help_funcs import all_pizzas_parameters, all_types_delivery

os.environ["LATENCY_ENABLED"] = "0"


@pytest.fixture
def runner():
    """Create CliRunner for pizza app"""
    return CliRunner()


def test_menu(runner):
    """Test that cli prints all pizzas from the menu"""
    result = runner.invoke(cli, ["menu"])
    assert result.exit_code == 0
    assert len(result.output.split("\n")) == 1 + 1 + len(
        pizza_menu
    )  # 1 - header, 1 - pizza sizes


@all_types_delivery
@all_pizzas_parameters
def test_pizza_order(is_delivery, pizza_class, runner):
    """Test that you can order pizzas and output matches target number of rows"""
    pizza_name = (
        pizza_class.get_name()
    )  # maybe add tests for upper and lower pizza names
    params_cli = (
        ["order", pizza_name, "--delivery"] if is_delivery else ["order", pizza_name]
    )
    result = runner.invoke(cli, params_cli)
    assert result.exit_code == 0
    assert len(result.output.split("\n")) == 4


@all_pizzas_parameters
def test_pizza_wrong_size(pizza_class, runner):
    """Test that program don't crash on unknown pizza size
    and has expected number of lines"""
    pizza_name = pizza_class.get_name()
    result = runner.invoke(
        cli, ["order", pizza_name, "--size", "definitely_unknown_size"]
    )
    assert result.exit_code == 0
    assert len(result.output.split("\n")) == 2


@all_types_delivery
def test_pizza_incorrect_order(is_delivery, runner):
    """Test that you can order pizzas and output matches target number of rows"""
    pizza_name = "some_definitely_unknown_pizza"
    params_cli = (
        ["order", pizza_name, "--delivery"] if is_delivery else ["order", pizza_name]
    )
    result = runner.invoke(cli, params_cli)
    assert result.exit_code == 0
    assert len(result.output.split("\n")) == 1 + 1 + 1 + len(
        pizza_menu
    )  # header + msg + menu + pizza sizes
