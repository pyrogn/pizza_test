from collections import defaultdict
from collections import UserDict
from typing import Self


class FoodItem:
    """Super class for all food items"""

    recipe: dict
    emoji: str
    type_of_food: str


class PizzaRecipe(FoodItem):
    """Specialization of food - pizza"""

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
        return cls.__mro__[0].__name__.capitalize()

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
    def __init__(self, menu: "DictAssortment") -> None:
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

    def make_order(self, pizza_name, client: "Client", is_delivery=False):
        print("was made a request for pizza")
        pizza = self.menu[pizza_name]()
        pizza = self.bake(pizza)
        self.add_to_stock(client, pizza)
        if is_delivery:
            self.deliver(client)

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


class DictAssortment(UserDict):
    def __init__(self):
        super().__init__()

    def __getitem__(self, item: str):
        """To accept pizza name indifferent of register"""
        return super().__getitem__(item.lower())

    def __setitem__(self, key, value):
        return super().__setitem__(key.lower(), value)

    def __contains__(self, item: str):
        return super().__contains__(item.lower())


# move it to different module maybe
assortment = DictAssortment()


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


menu_str = "\n".join(
    f"- {v.name} {v.emoji} : {v.clean_recipe}" for v in assortment.values()
)


if __name__ == "__main__":
    # cli()
    restaurant = Restaurant(assortment)
    a = Pepperoni()
    client = Client(restaurant=restaurant, is_delivery=True)
    client.order("Pepperoni")
    client.order("Pepperoni")
    print(client.stock)
    # print(a)
