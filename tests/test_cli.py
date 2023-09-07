"""Basic tests tha cli app is running"""
import os
from pizza.pizza_menu import pizza_menu
from pizza.cli import cli
from click.testing import CliRunner
from .help_funcs import all_pizzas_parameters, all_types_delivery


os.environ["LATENCY_ENABLED"] = "0"


def test_menu():
    """Test that there are 3 pizzas on the menu"""
    runner = CliRunner()
    result = runner.invoke(cli, ["menu"])
    assert result.exit_code == 0
    assert len(result.output.split("\n")) == 1 + len(
        pizza_menu
    )  # one extra for header


@all_types_delivery
@all_pizzas_parameters
def test_pizza_order(is_delivery, pizza_class):
    """Test that you can order pizzas and output matches target number of rows"""
    runner = CliRunner()
    pizza_name = (
        pizza_class.get_name()
    )  # maybe add tests for upper and lower pizza names
    params_cli = (
        ["order", pizza_name, "--delivery"]
        if is_delivery
        else ["order", pizza_name]
    )
    result = runner.invoke(cli, params_cli)
    assert result.exit_code == 0
    assert len(result.output.split("\n")) == 4


@all_types_delivery
def test_pizza_incorrect_order(is_delivery):
    """Test that you can order pizzas and output matches target number of rows"""
    runner = CliRunner()
    pizza_name = "some_definitely_unknown_pizza"
    params_cli = (
        ["order", pizza_name, "--delivery"]
        if is_delivery
        else ["order", pizza_name]
    )
    result = runner.invoke(cli, params_cli)
    assert len(result.output.split("\n")) == 1 + 1 + len(
        pizza_menu
    )  # header + msg + menu
