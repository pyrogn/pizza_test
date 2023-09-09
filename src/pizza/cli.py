"""Module with CLI for ordering pizza"""
import os
import sys

import click

from pizza.business import Client, Restaurant
from pizza.pizza_menu import Pizza, full_menu_str, pizza_menu

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
def order(pizza: str, *, delivery: bool, size: str):
    """Order a pizza from the menu. Choose pizza name and size"""
    ordered_pizza, is_success, message = Pizza.safe_init(pizza_name=pizza, size=size)
    if not is_success:
        print(message)
        sys.exit()

    restaurant = Restaurant(pizza_menu)
    client = Client(restaurant=restaurant, is_delivery=delivery)

    print("You want to order", message)
    # All logic with order and delivery is inside this method
    client.order(pizza)


if __name__ == "__main__":
    cli()
