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


class Margherita(PizzaRecipe):
    recipe = {"tomato sauce", 'mozzarella', 'tomatoes'}


class Pepperoni(PizzaRecipe):
    pass


class Hawaiian(PizzaRecipe):
    pass


@cli.command()
@click.option(' =delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool):
    print('i want to order', pizza)


if __name__ == '__main__':
    p1 = Margherita()
    p1.dict()
