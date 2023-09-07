"""Module with CLI for ordering pizza"""
import sys
import os

from pizza.pizza_menu import pizza_menu, full_menu_str
from pizza.business import Restaurant, Client
import click

os.environ[
    "LATENCY_ENABLED"
] = "1"  # enable latency only in cli mode and this doesn't look good


@click.group()
def cli():
    """Look at the menu and order your favourite pizzas\n
    Deliver or pick up - you choose!"""
    pass


@cli.command()
def menu():
    """Print available food"""
    print(full_menu_str)


@cli.command()
@click.option("--delivery", default=False, is_flag=True)
@click.argument("pizza", nargs=1)
def order(pizza: str, delivery: bool):
    """Order a pizza from the menu"""
    restaurant = Restaurant(pizza_menu)
    client = Client(restaurant=restaurant, is_delivery=delivery)

    if pizza not in pizza_menu:
        print("No such pizza on the menu, the available pizzas:")
        print(full_menu_str)
        sys.exit()

    ordered_pizza = pizza_menu[pizza]()  # Create pizza from a template
    print("You want to order", ordered_pizza.get_name(), ordered_pizza.emoji)
    # All logic with order and delivery is inside this method
    client.order(pizza)
