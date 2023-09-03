from dataclasses import dataclass

import click


@click.group()
def cli():
    pass


@dataclass
class PizzaRecipe:
    # size: str
    recipe: dict

    def __init__(self):
        pass

    def __eq__(self, other):
        pass

    def dict(self):
        print(self.recipe)


assortment = {}


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


def bake(pizza):
    print('baked')


def deliver(pizza):
    pass


if __name__ == '__main__':
    cli()
