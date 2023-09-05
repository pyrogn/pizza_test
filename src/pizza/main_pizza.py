import random
from collections import defaultdict
import sys
import time
from collections import UserDict
from typing import Self

import click  # but Typer is a bit cleaner


@click.group()
def cli():
    pass


class FoodItem:
    """Super class for all food items"""

    recipe: dict
    emoji: str
    type_of_food: str


class PizzaRecipe(FoodItem):
    type_of_food = "pizza"

    def __init__(self, size="L") -> None:
        self.size = size
        self.is_baked = False

    def bake(self):
        """Might be incorrect"""
        if not self.is_baked:
            self.is_baked = True

    @classmethod
    @property
    def name(cls) -> str:
        return cls.__class__.__name__.capitalize()

    @classmethod
    @property
    def clean_recipe(cls) -> str:
        """Dict of ingredients to a string"""
        return ", ".join([i for i in cls.recipe])

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__} {self.type_of_food}, "
            f"Size: {self.size}, Is baked: {self.is_baked}"
        )

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __eq__(self, other: Self) -> bool:
        return (
            (set(self.recipe) == set(other.recipe))
            & (self.name == other.name)
            & (self.size == other.size)
        )

    def dict(self):
        print(self.recipe)


class Restaurant:
    def __init__(self, menu: "CustomDict") -> None:
        self.menu = menu
        self.stock = defaultdict(list)

    @staticmethod
    def bake(pizza: PizzaRecipe) -> PizzaRecipe:
        if not pizza.is_baked:
            # add time sleep
            print("baked")
            pizza.is_baked = True
        return pizza

    def add_to_stock(self, client: "Client", item: FoodItem) -> None:
        self.stock[client].append(item)

    def retrieve_from_stock(self, client: "Client") -> list[FoodItem]:
        items = self.stock[client]
        del self.stock[client]
        return items

    def pickup(self, client):
        food = self.retrieve_from_stock(client)
        print("picked up from restaurant")
        return food
        # client.add_to_stock(food)

    def make_order(self, pizza_name, client: "Client", is_delivery=False):
        print("was made a request for pizza")
        pizza = self.menu[pizza_name]()
        pizza = self.bake(pizza)
        self.add_to_stock(client, pizza)
        if is_delivery:
            self.deliver(client)
        # return pizza

    def deliver(self, client: "Client") -> None:
        # do some work with timer
        print("delivered")
        client.add_to_stock(self.retrieve_from_stock(client))


class Client:
    def __init__(
        self,
        restaurant: Restaurant,
        is_delivery: bool,
        name: str = "Pavel",
        phone_number: str = "+1337",
    ) -> None:
        self.name = name
        self.phone_number = phone_number
        self.restaurant = restaurant
        self.is_delivery = is_delivery
        self.stock = []

    def __hash__(self):
        return hash((self.name, self.phone_number))

    def add_to_stock(self, items: list[FoodItem]) -> None:
        print("added to clients stock")
        for item in items:
            self.stock.append(item)

    def order(self, pizza_name: str) -> None:
        self.restaurant.make_order(
            pizza_name, self, is_delivery=self.is_delivery
        )
        if not self.is_delivery:
            food = self.pickup()
            self.add_to_stock(food)

    def pickup(self):
        food = self.restaurant.pickup(self)
        return food


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
        return super().__contains__(item.lower())


assortment = CustomDict()


def pizza_to_assortment(cls):
    assortment[cls.__name__] = cls
    return cls


@pizza_to_assortment
class Margherita(PizzaRecipe):
    recipe = ["tomato sauce", "mozzarella", "tomatoes"]
    emoji = "🧀"


@pizza_to_assortment
class Pepperoni(PizzaRecipe):
    recipe = ["tomato sauce", "mozzarella", "pepperoni"]
    emoji = "🍕"


@pizza_to_assortment
class Hawaiian(PizzaRecipe):
    recipe = ["tomato sauce", "mozzarella", "chicken", "pineapples"]
    emoji = "🍍"


# menu_str = ""
# for k, v in assortment.items():
#     menu_str += f"- {k} {v.emoji} : {v.clean_recipe}\n"
menu_str = "\n".join(
    f"- {v.name} {v.emoji} : {v.clean_recipe}" for v in assortment.values()
)


@cli.command()
def menu():
    print(menu_str)


class EmojiSelector:
    # select emoji by name from list
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


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


if __name__ == "__main__":
    # cli()
    restaurant = Restaurant(assortment)
    a = Pepperoni()
    client = Client(restaurant=restaurant, is_delivery=True)
    client.order("Pepperoni")
    client.order("Pepperoni")
    print(client.stock)
    # print(a)
