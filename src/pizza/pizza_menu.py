"""Generating a restaurant's menu and classes of Pizza.

Module defines pizza classes and collects them into custom dict
"""
from collections import UserDict
from typing import TypeVar

from pizza.constants import AVAILABLE_PIZZA_SIZES


class FoodItem:
    """Super class for all food items.

    Attrs:
        recipe: recipe of this food
        emoji: emoji, associated with this food
        type_of_food: general name of this food
        alt_name: alternative name of food if exists.
            By default, a class name will be used.
    """

    recipe: tuple[str, ...]
    emoji: str
    type_of_food: str
    alt_name: str | None = None
    is_baked: bool = False


class Pizza(FoodItem):
    """Specialization of food - pizza.

    Attributes:
        is_baked (bool): is pizza baked, or it is a template
        size: size of pizza (L or XL).
    """

    type_of_food: str = "pizza"

    def __init__(self, size="L") -> None:
        """Initialize Pizza with size.

        Attributes:
            size: size of pizza

        Raises:
            ValueError: if size is not available.
        """
        if size.upper() not in AVAILABLE_PIZZA_SIZES:
            string_error = f"{size} size is not in {AVAILABLE_PIZZA_SIZES}"
            raise ValueError(string_error)
        self.size = size

    def bake(self) -> None:
        """Make pizza bake itself. Changes is_baked attr to True."""
        if not self.is_baked:
            self.is_baked = True

    # CONFUSION: can we make dynamic attribute (like property) for a class?
    @classmethod
    def get_name(cls) -> str:
        """Infer name from the class or alt_name if provided and return it."""
        if not cls.alt_name:
            return cls.__mro__[0].__name__.title()
        return cls.alt_name.title()

    @classmethod
    def get_clean_recipe(cls) -> str:
        """Return recipe of pizza as ingredients separated by comma."""
        return ", ".join(list(cls.recipe))

    def __str__(self) -> str:
        """Description of pizza instance."""
        return (
            f"{self.__class__.get_name()} {self.type_of_food}, "
            f"Size: {self.size}, Is baked: {self.is_baked}"
        )

    def __repr__(self) -> str:
        """Repr of pizza with original parameters. It will not be baked."""
        return f"{self.__class__.__name__}(size={self.size!r})"

    def __eq__(self, other: "Pizza") -> bool:  # type: ignore
        """Compare pizzas by their characteristics.

        They will be equal only with the same recipe, size and name.
        """
        if not isinstance(other, Pizza):
            return NotImplemented
        return (
            (set(self.recipe) == set(other.recipe))
            & (self.get_name == other.get_name)
            & (self.size == other.size)
        )

    def dict(self) -> dict[str, tuple[str, ...]]:
        """Return dictionary with key=name of pizza, value=recipe of pizza."""
        return {self.get_name(): self.recipe}


class LowerKeyMenu(UserDict):
    """Custom dictionary for pizza menu to be more resilient.

    Dictionary that is indifferent of case of the key
    It makes lower every key.
    """

    def __init__(self) -> None:
        """Initialize UserDict."""
        super().__init__()

    def __getitem__(self, item: str) -> type[Pizza]:
        """Key should be string and it is converted to lower case."""
        return super().__getitem__(item.lower())

    def __setitem__(self, key: str, value: type[Pizza]) -> None:
        """Key is str and will be lowered."""
        return super().__setitem__(key.lower(), value)

    def __contains__(self, item: str) -> bool:  # type: ignore
        """Item is converted to lower case."""
        return super().__contains__(item.lower())


pizza_menu = LowerKeyMenu()
P = TypeVar("P", bound=Pizza)  # to match subclasses of Pizza


def add_pizza_to_menu(cls: type[P]) -> type[P]:
    """Decorator to trace and put classes into pizza menu.

    Add pizza to a dict after every definition as a side effect
    Alternative - using Pizza.__subclasses__().
    """
    pizza_menu[cls.get_name()] = cls
    return cls


@add_pizza_to_menu
class Margherita(Pizza):
    """Margherita Pizza."""

    recipe = ("tomato sauce", "mozzarella", "tomatoes")
    emoji = "🧀"


@add_pizza_to_menu
class Pepperoni(Pizza):
    """Pepperoni Pizza."""

    recipe = ("tomato sauce", "mozzarella", "pepperoni")
    emoji = "🍕"


@add_pizza_to_menu
class Hawaiian(Pizza):
    """Hawaiian Special pizza."""

    recipe = ("tomato sauce", "mozzarella", "chicken", "pineapples")
    emoji = "🍍"
    alt_name = "Hawaiian Special"  # Give a complex name for a test


def validate_pizza(
    pizza_name: str,
    size: str,
) -> tuple[bool, str]:
    """Validate if pizza with parameters exists and return log message.

    Attributes:
        pizza_name:  pizza name from the menu
        size:  size from the available sizes

    Returns:
        A tuple with two values
            is_success (bool) - True if no error, else False
            message - if there's an error, message is meaningful text error
                if it is not an error, it will contain pizza name, emoji and size.
    """
    size = size.upper()
    if size not in AVAILABLE_PIZZA_SIZES:
        message = (
            f"size {size} is not available. "
            f"Choose one from: {AVAILABLE_PIZZA_SIZES}"
        )
        return False, message
    if pizza_name not in pizza_menu:
        message = (
            f"No such pizza on the menu, the available pizzas:\n{full_menu_str}"
        )
        return False, message

    cls_pizza = pizza_menu[pizza_name]
    message = f"{cls_pizza.get_name()} {cls_pizza.emoji} {size} size"
    return True, message


# full menu as a single multiline string
full_menu_str: str = (
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
