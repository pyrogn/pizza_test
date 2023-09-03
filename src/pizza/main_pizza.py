import random
import time

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

    def __eq__(self, other: __class__):
        return set(self.recipe) == set(other.recipe)

    def dict(self):
        print(self.recipe)


assortment = {}


def add_latency(fn):
    time.sleep(random.randint(1, 3))
    return fn


def log(str_template: str):
    def outer_wrapper(fn):
        def wrapper(*args, **kwargs):
            time_start = time.time()
            # @wraps(fn) # apply wrapper from functools
            result = fn(*args, **kwargs)
            time_end = time.time()
            lapsed_time = time_end - time_start
            print(str_template.format(lapsed_time))  # apply to placeholder
            return result

        return wrapper

    return outer_wrapper


def pizza_to_assortment(cls):
    assortment[cls.__name__] = cls.recipe
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


@cli.command()
def menu():
    for k, v in assortment.items():
        print(f"- {k} 🧀: {', '.join([i for i in v])}")


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool):
    print('i want to order', pizza)
    bake(pizza)
    if delivery:
        deliver(pizza)


@add_latency
def bake(pizza):
    print('baked')


@add_latency
def deliver(pizza):
    pass


if __name__ == '__main__':
    cli()
