"""Generating a restaurant's menu and classes of Pizza
Classes:
    FoodItem
        Pizza
            Pepperoni
            Margherita
            Hawaiian
    LowerKeyMenu"""
from collections import UserDict
from typing import Type, TypeVar, Union


class FoodItem:
    """Super class for all food items
    Attrs:
        recipe: recipe of this food
        emoji: emoji, associated with this food
        type_of_food: general name of this food
        alt_name: alternative name of food if exists.
            By default, a class name will be used
    """

    recipe: list[str]
    emoji: str
    type_of_food: str
    alt_name: Union[
        str,
        None,
    ] = None  # make an option for _name != __class__.__name__
    is_baked: bool = False


AVAILABLE_PIZZA_SIZES = ["L", "XL"]


class Pizza(FoodItem):
    """Specialization of food - pizza
    Methods:
        bake: make yourself baked
        get_name: get name of the class or provided in alt_name
        get_clean_recipe: get recipe as a string. Ingredients separated by a comma
        dict: returns a recipe as dict
    Attributes:
        is_baked (bool): is pizza baked, or it is a template
        size: size of pizza (L or XL)
    Raises:
        ValueError: raised if size of pizza is not available
    """

    type_of_food = "pizza"

    def __init__(self, size="L") -> None:
        """Initialize Pizza
        Attributes:
            size: size of pizza
        Raises:
            ValueError: if size is not available"""
        if size.upper() not in AVAILABLE_PIZZA_SIZES:
            raise ValueError(f"{size} size not in {AVAILABLE_PIZZA_SIZES}")
        self.size = size

    def bake(self) -> None:
        """Make pizza bake itself
        Changes is_baked attr to True"""
        if not self.is_baked:
            self.is_baked = True

    # CONFUSION: can we make dynamic attribute (like property) for a class?
    @classmethod
    def get_name(cls) -> str:
        """Infer name from the class or get alt_name if provided"""
        if not cls.alt_name:
            return cls.__mro__[0].__name__.title()
        return cls.alt_name.title()

    @classmethod
    def get_clean_recipe(cls) -> str:
        """Return recipe of pizza as ingredients separated by comma"""
        return ", ".join(list(cls.recipe))

    def __str__(self) -> str:
        """Description of pizza instance"""
        return (
            f"{self.__class__.get_name()} {self.type_of_food}, "
            f"Size: {self.size}, Is baked: {self.is_baked}"
        )

    def __repr__(self) -> str:
        """Repr of pizza with original parameters. It will not be baked"""
        return f"{self.__class__.__name__}(size={self.size!r})"

    def __eq__(self, other: "Pizza") -> bool:  # type: ignore
        """Compare pizzas.
        They will be equal only with the same recipe, size and name"""
        if not isinstance(other, Pizza):
            return NotImplemented
        return (
            (set(self.recipe) == set(other.recipe))
            & (self.get_name == other.get_name)
            & (self.size == other.size)
        )

    def dict(self) -> dict[str, list[str]]:
        """Return dictionary with key=name of pizza, value=recipe of pizza"""
        return {self.get_name(): self.recipe}


class LowerKeyMenu(UserDict):
    """Dictionary that is indifferent of case of the key
    It makes lower every key"""

    def __init__(self):
        """Initialize UserDict"""
        super().__init__()

    def __getitem__(self, item: str):
        """Key should be string and it is converted to lower"""
        return super().__getitem__(item.lower())

    def __setitem__(self, key: str, value):
        """Key is str and will be lower"""
        return super().__setitem__(key.lower(), value)

    def __contains__(self, item: str):  # type: ignore
        """Item is converted to lower"""
        return super().__contains__(item.lower())


pizza_menu = LowerKeyMenu()

P = TypeVar("P", bound=Pizza)  # to match subclasses


def add_pizza_to_menu(cls: Type[P]) -> Type[P]:
    """Add pizza to a dict after every definition
    Alternative - using Pizza.__subclasses__()"""
    pizza_menu[cls.get_name()] = cls
    return cls


@add_pizza_to_menu
class Margherita(Pizza):
    """Margherita Pizza"""

    recipe = ["tomato sauce", "mozzarella", "tomatoes"]
    emoji = "🧀"


@add_pizza_to_menu
class Pepperoni(Pizza):
    """Pepperoni Pizza"""

    recipe = ["tomato sauce", "mozzarella", "pepperoni"]
    emoji = "🍕"


@add_pizza_to_menu
class Hawaiian(Pizza):
    """Hawaiian Special pizza"""

    recipe = ["tomato sauce", "mozzarella", "chicken", "pineapples"]
    emoji = "🍍"
    alt_name = "Hawaiian Special"  # Give a complex name for a test


# full menu as a single multiline string
full_menu_str = (
    "\n".join(
        f"- {v.get_name()} {v.emoji} : {v.get_clean_recipe()}"
        for v in pizza_menu.values()
    )
    + f"\nAvailable pizza sizes: {', '.join(AVAILABLE_PIZZA_SIZES)}"
)

if __name__ == "__main__":
    pizza = Hawaiian()
    print(pizza.__repr__())
    print(pizza)
    pizza.bake()
    print(pizza)
    print(pizza.dict())
    print(full_menu_str)
    try:
        print(Pepperoni(size="s"))
    except ValueError:
        print("error with wrong size escaped")
