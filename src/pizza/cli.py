"""Module with CLI for ordering pizza."""
import os
import sys

import click

from pizza.business import Client, Restaurant
from pizza.pizza_menu import full_menu_str, pizza_menu, validate_pizza

os.environ[
    "LATENCY_ENABLED"
] = "1"  # enable latency only in cli mode and this doesn't look good


@click.group()
def cli():
    """Look at the menu and order your favourite pizzas\n
    Deliver or pick up - you choose!
    """


@cli.command()
def menu():
    """Print available food."""
    print(full_menu_str)


@cli.command()
@click.option("--delivery", default=False, is_flag=True)
@click.option("--size", default="L")
@click.argument("pizza", nargs=1)
def order(pizza: str, *, delivery: bool, size: str):
    """Order a pizza from the menu. Choose pizza name and size."""
    is_success, message = validate_pizza(pizza_name=pizza, size=size)
    if not is_success:
        print(message)
        sys.exit()

    restaurant = Restaurant(pizza_menu)
    client = Client(restaurant=restaurant, is_delivery=delivery)
    print("You want to order", message)
    client.order(pizza)


if __name__ == "__main__":
    cli()
