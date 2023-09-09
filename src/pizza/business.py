"""Business logic of order and delivery.
Classes:
    Client
    Restaurant"""
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
    "bake": MsgForParam(
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
    """Entity that bakes pizza, delivers food to a client and allows to pickup food
    Methods:
        bake: bake pizza. Returns a baked pizza
        _add_to_stock: adds FoodItem to _stock linked to a specific client
        _retrieve_from_stock: takes items from _stock
            and gives items as list to a customer
        pickup: interface for clients to pick up their food
        make_order: interface for clients to make an order.
            Delivery choice will be inferred from Client
        _deliver: deliver baked food from a restaurant's _stock
            to a customer's _stock
    """

    def __init__(self, menu: "LowerKeyMenu") -> None:
        """menu: available food to clients
        _stock: _stock of the restaurant with food waiting for pickup,
            where key - Client, value - list of FoodItem
        """
        self.menu = menu
        self._stock: defaultdict[Client, list[FoodItem]] = defaultdict(list)

    def bake(self, pizza: Pizza) -> Pizza:
        """Takes pizza and makes it baked.
        If it was already baked, return as it is"""
        if not pizza.is_baked:
            pizza.is_baked = True
        return pizza

    def _add_to_stock(self, client: "Client", item: FoodItem) -> None:
        """Add baked food to a _stock (list) where key=client who ordered it"""
        self._stock[client].append(item)

    def _retrieve_from_stock(self, client: "Client") -> list[FoodItem]:
        """Take all food from _stock for this client"""
        items = self._stock[client]
        del self._stock[client]
        return items

    def pickup(self, client: "Client") -> list[FoodItem]:
        """Give food to client who wants to pick up by himself"""
        food = self._retrieve_from_stock(client)
        return food

    def make_order(self, pizza_name, client: "Client", is_delivery=False) -> None:
        """Process order of food by a client"""
        pizza = self.menu[pizza_name]()
        pizza = self.bake(pizza)
        self._add_to_stock(client, pizza)
        if is_delivery:
            self._deliver(client)

    def _deliver(self, client: "Client") -> None:
        """Deliver food to a client and put it in his _stock"""
        client.add_to_stock(self._retrieve_from_stock(client))


@trace_heavy_tasks(params_for_heavy_tasks_client)
class Client:
    """Client orders food from the restaurant. Each client linked to the restaurant
    Methods:
        add_to_stock: adds food to client's stock
        order: orders food from the restaurant
        _pickup: client picks up his food from the restaurant
    """

    def __init__(
        self,
        restaurant: Restaurant,
        is_delivery: bool,
        name: str = "Pavel",
        phone_number: str = "+1337",
    ) -> None:
        """Initialization of Restaurant
        Attributes:
            name: name of customer for identification
            phone_number: phone number of customer for identification
            restaurant: instance of restaurant to which the client is linked
            is_delivery (bool): if True restaurant will deliver food,
                if False - food needs to be picked up by yourself
        Added attributes:
            _stock: list which contains and collects food items for this client
        """
        self.name = name
        self.phone_number = phone_number
        self.restaurant = restaurant
        self.is_delivery = is_delivery
        self._stock: list[FoodItem] = []

    def __hash__(self):
        """Uniquely identify a client"""
        return hash((self.name, self.phone_number))

    def add_to_stock(self, items: list[FoodItem]) -> None:
        """Add food items to a client's stock"""
        for item in items:
            self._stock.append(item)

    def order(self, pizza_name: str) -> None:
        """Make an order for food in a restaurant.
        If is_delivery=True then wait for delivery
        If is_delivery=False then pick up by yourself"""
        self.restaurant.make_order(pizza_name, self, is_delivery=self.is_delivery)
        if not self.is_delivery:
            food = self._pickup()
            self.add_to_stock(food)

    def _pickup(self) -> list[FoodItem]:
        """Pickup all ordered food from a restaurant"""
        food = self.restaurant.pickup(self)
        return food


if __name__ == "__main__":
    restaurant = Restaurant(pizza_menu)
    a = Pepperoni()
    client = Client(restaurant=restaurant, is_delivery=False)
    client.order("Pepperoni")
    client.order("Pepperoni")
    print(client._stock)
    client = Client(restaurant=restaurant, is_delivery=True)
    client.order("Pepperoni")
    client.order("Pepperoni")
    # print(Restaurant.__wrapped__)
