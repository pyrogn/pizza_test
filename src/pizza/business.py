from collections import defaultdict
import functools
import time
import random
import os
from pizza.pizza_menu import DictAssortment, FoodItem, PizzaRecipe

from pizza.pizza_menu import assortment, Pepperoni

LATENCY_ENABLED = os.getenv(
    "LATENCY_ENABLED", "0"
)  # latency added only for cli app


def add_latency(fn):
    @functools.wraps(fn)  # not sure if it works with class methods
    def wrapper(self, *args, **kwargs):
        # global LATENCY_ENABLED
        time_sleep = 0
        if LATENCY_ENABLED == "1":
            time_sleep = random.randint(1, 3) / 5
        time.sleep(time_sleep)
        result = fn(self, *args, **kwargs)
        return result

    return wrapper


def log(str_template: str):
    def outer_wrapper(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            time_start = time.time()
            result = fn(self, *args, **kwargs)
            lapsed_time = time.time() - time_start
            print(str_template.format(lapsed_time))  # apply to placeholder
            return result

        return wrapper

    return outer_wrapper


class Restaurant:
    def __init__(self, menu: "DictAssortment") -> None:
        self.menu = menu
        self._stock = defaultdict(list)

    @log("Baking took {:.2f} seconds")
    @add_latency
    def bake(self, pizza: PizzaRecipe) -> PizzaRecipe:
        if not pizza.is_baked:
            print("👩‍🍳 baked", end=" ")
            pizza.is_baked = True
        return pizza

    def _add_to_stock(self, client: "Client", item: FoodItem) -> None:
        self._stock[client].append(item)

    def _retrieve_from_stock(self, client: "Client") -> list[FoodItem]:
        items = self._stock[client]
        del self._stock[client]
        return items

    def pickup(self, client: "Client") -> list[FoodItem]:
        food = self._retrieve_from_stock(client)
        return food

    def make_order(
        self, pizza_name, client: "Client", is_delivery=False
    ) -> None:
        pizza = self.menu[pizza_name]()
        pizza = self.bake(pizza)
        self._add_to_stock(client, pizza)
        if is_delivery:
            self.deliver(client)

    @log("Delivery took {:.2f} seconds")
    @add_latency
    def deliver(self, client: "Client") -> None:
        # do some work with timer
        print("🛵 delivered", end=" ")
        client.add_to_stock(self._retrieve_from_stock(client))


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
        """Uniquely identify a client"""
        return hash((self.name, self.phone_number))

    def add_to_stock(self, items: list[FoodItem]) -> None:
        for item in items:
            self.stock.append(item)

    def order(self, pizza_name: str) -> None:
        self.restaurant.make_order(
            pizza_name, self, is_delivery=self.is_delivery
        )
        if not self.is_delivery:
            food = self._pickup()
            self.add_to_stock(food)

    @log("Picking up took {:.2f} seconds")
    @add_latency
    def _pickup(self):
        print("🏎️  Picking up", end=" ")
        food = self.restaurant.pickup(self)
        return food


if __name__ == "__main__":
    restaurant = Restaurant(assortment)
    a = Pepperoni()
    client = Client(restaurant=restaurant, is_delivery=False)
    client.order("Pepperoni")
    client.order("Pepperoni")
    print(client.stock)
    # print(a)
