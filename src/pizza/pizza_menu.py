"""Generating a restaurant's menu and classes of Pizza"""
from collections import UserDict
from typing import Union


class UnifiedMenu(UserDict):
    """Dictionary that is indifferent of registry of the key
    It makes lower every key"""

    def __init__(self):
        super().__init__()

    def __getitem__(self, item: str):
        return super().__getitem__(item.lower())

    def __setitem__(self, key: str, value):
        return super().__setitem__(key.lower(), value)

    def __contains__(self, item: str):  # type: ignore
        return super().__contains__(item.lower())


pizza_menu = UnifiedMenu()


def pizza_to_assortment(cls):
    """Add pizza to a dict after every definition
    Alternative - using Pizza.__subclasses__()"""
    pizza_menu[cls.get_name()] = cls
    return cls


class FoodItem:
    """Super class for all food items
    Attrs:
        recipe: recipe of this food
        emoji: emoji, associated with this food
        type_of_food: general name of this food
        alt_name: alternative name of food if exists. By default, a class name will be used
    """

    recipe: list[str]
    emoji: str
    type_of_food: str
    alt_name: Union[
        str, None
    ] = None  # make an option for _name != __class__.__name__


class Pizza(FoodItem):
    """Specialization of food - pizza
    Methods:
        bake: make yourself baked
        get_name: get name of the class or provided in alt_name
        get_clean_recipe: get recipe as a string. Ingredients separated by a comma
        dict: returns a recipe as dict
    """

    type_of_food = "pizza"

    def __init__(self, size="L") -> None:
        self.size = size
        self.is_baked = False

    def bake(self) -> None:
        """Make pizza bake itself"""
        if not self.is_baked:
            self.is_baked = True

    # I wish I could use class properties for dynamic attributes
    @classmethod
    def get_name(cls) -> str:
        if not cls.alt_name:
            return cls.__mro__[0].__name__.title()
        return cls.alt_name.title()

    @classmethod
    def get_clean_recipe(cls) -> str:
        return ", ".join([i for i in cls.recipe])

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__} {self.type_of_food}, "
            f"Size: {self.size}, Is baked: {self.is_baked}"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(size={self.size!r})"

    def __eq__(self, other: "Pizza") -> bool:  # type: ignore
        """Compare pizzas. They will be equal only with the same recipe, size and name"""
        if not isinstance(other, Pizza):
            return NotImplemented
        return (
            (set(self.recipe) == set(other.recipe))
            & (self.get_name == other.get_name)
            & (self.size == other.size)
        )

    def dict(self):
        return self.recipe


@pizza_to_assortment
class Margherita(Pizza):
    recipe = ["tomato sauce", "mozzarella", "tomatoes"]
    emoji = "🧀"


@pizza_to_assortment
class Pepperoni(Pizza):
    recipe = ["tomato sauce", "mozzarella", "pepperoni"]
    emoji = "🍕"


@pizza_to_assortment
class Hawaiian(Pizza):
    recipe = ["tomato sauce", "mozzarella", "chicken", "pineapples"]
    emoji = "🍍"
    alt_name = "Hawaiian Special"  # Give a complex name for a test


# full menu as a string
full_menu_str = "\n".join(
    f"- {v.get_name()} {v.emoji} : {v.get_clean_recipe()}"
    for v in pizza_menu.values()
)

if __name__ == "__main__":
    pepperoni = Pepperoni()
    print(pepperoni.__repr__())
    print(pepperoni.dict())
