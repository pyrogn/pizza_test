import random
import sys
import time
from collections import UserDict
from typing import Self

import click


@click.group()
def cli():
    pass


# @dataclass
class PizzaRecipe:
    # size: str
    recipe: dict

    def __init__(self, size='L'):
        self.size = size
        self.name = self.__class__.__name__

    @classmethod
    @property
    def clean_recipe(cls):
        return ', '.join([i for i in cls.recipe])

    def __str__(self) -> str:
        return self.__class__.__name__

    def __eq__(self, other: Self) -> bool:
        return (set(self.recipe) == set(other.recipe)) & (self.name == other.name)

    def dict(self):
        print(self.recipe)


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


class CustomDict(UserDict):
    def __init__(self):
        super().__init__()

    def __getitem__(self, item: str):
        """To accept pizza name indifferent of register"""
        return super().__getitem__(item.lower())

    def __setitem__(self, key, value):
        return super().__setitem__(key.lower(), value)

    def __contains__(self, item: str):
        # think how to make it work
        return super().__contains__(item.lower())


assortment = CustomDict()


def pizza_to_assortment(cls):
    assortment[cls.__name__] = cls
    return cls


@pizza_to_assortment
class Margherita(PizzaRecipe):
    recipe = ["tomato sauce", 'mozzarella', 'tomatoes']


@pizza_to_assortment
class Pepperoni(PizzaRecipe):
    recipe = ["tomato sauce", "mozzarella", "pepperoni"]


@pizza_to_assortment
class Hawaiian(PizzaRecipe):
    recipe = ["tomato sauce", "mozzarella", "chicken", "pineapples"]


menu_str = ""
for k, v in assortment.items():
    menu_str += f"- {k} 🧀: {v.clean_recipe}\n"


@cli.command()
def menu():
    print(menu_str)


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool):
    print('i want to order', pizza)
    if pizza not in assortment:
        print("No such pizza in the assortment, here's the menu:")
        print(menu_str)
        sys.exit()
    ordered_pizza = assortment[pizza]()
    bake(ordered_pizza)
    if delivery:
        deliver(ordered_pizza)
    else:
        pick_up(ordered_pizza)


@log("Picking up took {:.2f} seconds")
@add_latency
def pick_up(pizza):
    print('picked up')


@log("Cooking took {:.2f} seconds")
@add_latency
def bake(pizza):
    print('baked')


@log("Delivery took {:.2f} seconds")
@add_latency
def deliver(pizza):
    print('delivered')


if __name__ == '__main__':
    # cli()
    a = Pepperoni()
    print(a)
