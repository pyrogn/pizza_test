from collections import UserDict
from typing import Self


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


assortment = DictAssortment()


def pizza_to_assortment(cls):
    assortment[cls.name] = cls
    return cls


class FoodItem:
    """Super class for all food items"""

    recipe: dict
    emoji: str
    type_of_food: str
    _name: [str, None] = None


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
        if not cls._name:
            return cls.__mro__[0].__name__.title()
        return cls._name.title()

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
    _name = "Hawaiian Special"


menu_str = "\n".join(
    f"- {v.name} {v.emoji} : {v.clean_recipe}" for v in assortment.values()
)
