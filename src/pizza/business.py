"""Business logic of order and delivery.
Here's introduced classes Client, Restaurant"""
from collections import defaultdict
import functools
import time
import random
import os
from pizza.spinner import add_spinner
from pizza.pizza_menu import ResilientMenu, FoodItem, Pizza
from pizza.pizza_menu import pizza_menu, Pepperoni

LATENCY_ENABLED = os.getenv(
    "LATENCY_ENABLED", "0"
)  # if 1 - latency added (cli), if 0 - no latency (everything else)


def add_latency(fn):
    """Add random latency to a class method to simulate real work"""

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        time_sleep = 0
        if LATENCY_ENABLED == "1":
            multiply = 1000
            # imitate uniform distribution without numpy
            time_sleep = random.randint(1 * multiply, 30 * multiply) / (
                10 * multiply
            )  # max 3 seconds

        time.sleep(time_sleep)
        result = fn(self, *args, **kwargs)
        return result

    return wrapper


def log(str_template: str):
    """Log and print time spent in the function call"""

    def outer_wrapper(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            time_start = time.time()
            result = fn(self, *args, **kwargs)
            lapsed_time = time.time() - time_start
            print(
                str_template.format(lapsed_time)
            )  # put time into placeholder
            return result

        return wrapper

    return outer_wrapper


class Restaurant:
    """Entity that bakes pizza, delivers to a client and allows to pickup food
    Methods:
        bake: bake pizza. Returns a baked pizza
        _add_to_stock: adds FoodItem to stock linked to a specific client
        _retrieve_from_stock: takes items from stock and gives items as list to a customer
        pickup: interface for clients to pick up their food
        make_order: interface for clients to make an order. Delivery choice will be inferred from Client
        deliver: deliver baked food from a restaurant's stock to a customer's stock
    """

    def __init__(self, menu: "ResilientMenu") -> None:
        """menu: available food to clients
        _stock: stock of the restaurant with food waiting for pickup, where key - Client, value - list of FoodItem
        """
        self.menu = menu
        self._stock: defaultdict[Client, list[FoodItem]] = defaultdict(list)

    @log("Baking took {:.2f} seconds")
    @add_spinner("Baking", "👩‍🍳 Baked")
    @add_latency
    def bake(self, pizza: Pizza) -> Pizza:
        if not pizza.is_baked:
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
    @add_spinner("Delivering", "🚲 Delivered")
    @add_latency
    def deliver(self, client: "Client") -> None:
        client.add_to_stock(self._retrieve_from_stock(client))


class Client:
    """Entity that orders food from the restaurant. Each instance linked to a specific restaurant
    Methods:
        add_to_stock: adds food to client's stock
        order: orders food from the restaurant
        _pickup: client picks up his food from the restaurant
    Attributes:
        name: name of customer for identification
        phone_number: phone number of customer for identification
        restaurant: instance of restaurant to which the client is linked
        is_delivery (bool): if True restaurant will deliver food, if False - food needs to be picked up by yourself
        stock: list which contains and collects food items
    """

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
        self.stock: list[FoodItem] = []

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
            food = (
                self._pickup()
            )  # probably because of decorators it wants self as parameter
            self.add_to_stock(food)

    @log("Picking up took {:.2f} seconds")
    @add_spinner("Picking up", "🏎️  Picked up")
    @add_latency
    def _pickup(self):
        food = self.restaurant.pickup(self)
        return food


if __name__ == "__main__":
    restaurant = Restaurant(pizza_menu)
    a = Pepperoni()
    client = Client(restaurant=restaurant, is_delivery=False)
    client.order("Pepperoni")
    client.order("Pepperoni")
    print(client.stock)
    client = Client(restaurant=restaurant, is_delivery=True)
    client.order("Pepperoni")
    client.order("Pepperoni")
