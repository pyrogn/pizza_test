"""Module with CLI for ordering pizza"""
import os
import sys

import click

from pizza.business import Client, Restaurant
from pizza.pizza_menu import AVAILABLE_PIZZA_SIZES, full_menu_str, pizza_menu

os.environ[
    "LATENCY_ENABLED"
] = "1"  # enable latency only in cli mode and this doesn't look good


@click.group()
def cli():
    """Look at the menu and order your favourite pizzas\n
    Deliver or pick up - you choose!"""


@cli.command()
def menu():
    """Print available food"""
    print(full_menu_str)


@cli.command()
@click.option("--delivery", default=False, is_flag=True)
@click.option("--size", default="L")
@click.argument("pizza", nargs=1)
def order(pizza: str, delivery: bool, size: str):
    """Order a pizza from the menu. Choose pizza name and size"""
    size = size.upper()

    if pizza not in pizza_menu:
        print("No such pizza on the menu, the available pizzas:")
        print(full_menu_str)
        sys.exit()
    if size not in AVAILABLE_PIZZA_SIZES:
        print(
            f"size {size} is not available. Choose one from: {AVAILABLE_PIZZA_SIZES}"
        )
        sys.exit()

    restaurant = Restaurant(pizza_menu)
    client = Client(restaurant=restaurant, is_delivery=delivery)

    ordered_pizza = pizza_menu[pizza](size=size)

    print(
        "You want to order",
        ordered_pizza.get_name(),
        ordered_pizza.emoji,
        f"{size} size",
    )
    # All logic with order and delivery is inside this method
    client.order(pizza)


if __name__ == "__main__":
    cli()
