import random
import sys
import time
from .business import Client, Restaurant, PizzaRecipe, assortment, menu_str
import click  # but Typer is a bit cleaner


def add_latency(fn):
    def wrapper(*args, **kwargs):
        time.sleep(random.randint(1, 3) / 5)
        result = fn(*args, **kwargs)
        return result

    # time.sleep(0)
    return wrapper


def log(str_template: str):
    def outer_wrapper(fn):
        def wrapper(*args, **kwargs):
            time_start = time.time()
            # @wraps(fn) # apply wrapper from functools
            result = fn(*args, **kwargs)
            lapsed_time = time.time() - time_start
            print(str_template.format(lapsed_time))  # apply to placeholder
            return result

        return wrapper

    return outer_wrapper


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
    pizza = pizza.capitalize()
    if pizza not in assortment:
        print("No such pizza in the assortment, here's the menu:")
        print(menu_str)
        sys.exit()
    ordered_pizza = assortment[pizza]()
    print("I want to order", pizza, ordered_pizza.emoji)
    bake(ordered_pizza)
    if delivery:
        deliver(ordered_pizza)
    else:
        pick_up(ordered_pizza)


@log("Picking up took {:.2f} seconds")
@add_latency
def pick_up(pizza):
    print("🏎️ picked up ", end="")


@log("Cooking took {:.2f} seconds")
@add_latency
def bake(pizza):
    print("👩‍🍳baked ", end="")


@log("Delivery took {:.2f} seconds")
@add_latency
def deliver(pizza):
    print("🛵 delivered ", end="")
