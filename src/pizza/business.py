"""Business logic of order and delivery.

Defines Client and Restaurant
"""
from collections import defaultdict

from pizza.decorators import MsgForParam, trace_heavy_tasks
from pizza.pizza_menu import (
    FoodItem,
    LowerKeyMenu,
    Pepperoni,
    Pizza,
    pizza_menu,
)

params_for_heavy_tasks_restaurant = {
    "_bake": MsgForParam(
        log_time_msg="Baking took {:.2f} seconds",
        start_msg="Baking",
        end_msg="👩‍🍳 Baked",
    ),
    "_deliver": MsgForParam(
        log_time_msg="Delivery took {:.2f} seconds",
        start_msg="Delivering",
        end_msg="🚲 Delivered",
    ),
}

params_for_heavy_tasks_client = {
    "_pickup": MsgForParam(
        log_time_msg="Picking up took {:.2f} seconds",
        start_msg="Picking up",
        end_msg="🏎️  Picked up",
    ),
}


@trace_heavy_tasks(params_for_heavy_tasks_restaurant)
class Restaurant:
    """Entity that bakes pizza, delivers food to a client and allows to pickup food.

    Attributes:
        menu: available food to clients
        _stock: _stock of the restaurant with food waiting for pickup,
            where key - Client, value - list of FoodItem.
    """

    def __init__(self, menu: "LowerKeyMenu") -> None:
        """Initialization of restaurant with the menu.

        menu: available food to clients
        _stock: _stock of the restaurant with food waiting for pickup,
            where key - Client, value - list of FoodItem.
        """
        self.menu = menu
        self._stock: defaultdict[Client, list[FoodItem]] = defaultdict(list)

    def _bake(self, pizza: Pizza) -> Pizza:
        """Bake pizza and return it.

        Takes pizza and makes it baked.
        If it was already baked, return as it is.
        """
        if not pizza.is_baked:
            pizza.bake()
        return pizza

    def _add_to_stock(self, client: "Client", item: FoodItem) -> None:
        """Add baked food to a _stock (list) where key=client who ordered it."""
        self._stock[client].append(item)

    def _retrieve_from_stock(self, client: "Client") -> list[FoodItem]:
        """Take all food from _stock for this client."""
        items = self._stock[client]
        del self._stock[client]
        return items

    def give_food(self, client: "Client") -> list[FoodItem]:
        """Give food to client who wants to pick up by himself."""
        return self._retrieve_from_stock(client)

    def process_order(
        self,
        pizza_name,
        client: "Client",
        *,
        is_delivery: bool = False,
    ) -> None:
        """Process order of food by a client and optionally deliver it"""
        pizza = self.menu[pizza_name]()
        pizza = self._bake(pizza)
        self._add_to_stock(client, pizza)
        if is_delivery:
            self._deliver(client)

    def _deliver(self, client: "Client") -> None:
        """Deliver food to a client and put it in his _stock."""
        client.add_to_stock(self._retrieve_from_stock(client))


@trace_heavy_tasks(params_for_heavy_tasks_client)
class Client:
    """Client who orders food from the restaurant.

    Each client linked to the restaurant
    Client has personal info: name and phone_number that identify him

    Attributes:
        restaurant
        is_delivery
        name
        phone_number
       _stock: list which contains and collects food items for this client.
    """

    def __init__(
        self,
        restaurant: Restaurant,
        *,
        is_delivery: bool,
        name: str = "Pavel",
        phone_number: str = "+1337",
    ) -> None:
        """Initializes Client with personal info and linked restaurant.

        Args:
            name: name of customer for identification
            phone_number: phone number of customer for identification
            restaurant: instance of restaurant to which the client is linked
            is_delivery (bool): if True restaurant will deliver food,
                if False - food needs to be picked up by yourself
        """
        self.name = name
        self.phone_number = phone_number
        self.restaurant = restaurant
        self.is_delivery = is_delivery
        self._stock: list[FoodItem] = []

    def __hash__(self):
        """Uniquely identify a client."""
        return hash((self.name, self.phone_number))

    def add_to_stock(self, items: list[FoodItem]) -> None:
        """Add food items to a client's stock."""
        for item in items:
            self._stock.append(item)

    def make_order(self, pizza_name: str) -> None:
        """Make an order for food in a restaurant. And get that food.

        If is_delivery=True then wait for delivery
        If is_delivery=False then pick up by yourself.
        """
        self.restaurant.process_order(pizza_name, self, is_delivery=self.is_delivery)
        if not self.is_delivery:
            food = self._pickup()
            self.add_to_stock(food)

    def _pickup(self) -> list[FoodItem]:
        """Pickup all ordered food from a restaurant."""
        return self.restaurant.give_food(self)


if __name__ == "__main__":
    restaurant = Restaurant(pizza_menu)
    a = Pepperoni()
    client = Client(restaurant=restaurant, is_delivery=False)
    client.make_order("Pepperoni")
    client.make_order("Pepperoni")
    print(client._stock)  # noqa
    client = Client(restaurant=restaurant, is_delivery=True)
    client.make_order("Pepperoni")
    client.make_order("Pepperoni")
    print(Restaurant.__mro__)
    print(Restaurant.__wrapped__.__mro__)  # type: ignore
