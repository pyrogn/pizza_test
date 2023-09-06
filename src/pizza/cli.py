import sys
import os

os.environ["LATENCY_ENABLED"] = "1"  # only in cli mode enable latency
from pizza.pizza_menu import assortment, menu_str, PizzaRecipe
from pizza.business import Restaurant, Client
import click  # but Typer is a bit cleaner


@click.group()
def cli():
    pass


@cli.command()
def menu():
    print(menu_str)


@cli.command()
@click.option("--delivery", default=False, is_flag=True)
@click.argument("pizza", nargs=1)
def order(pizza: str, delivery: bool):
    restaurant = Restaurant(assortment)
    client = Client(restaurant=restaurant, is_delivery=delivery)
    pizza = pizza.capitalize()
    if pizza not in assortment:
        print("No such pizza in the assortment, here's the menu:")
        print(menu_str)
        sys.exit()
    ordered_pizza = assortment[pizza]()
    print("I want to order", pizza, ordered_pizza.emoji)
    client.order(pizza)
