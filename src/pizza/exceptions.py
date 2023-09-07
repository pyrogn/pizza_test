from pizza.pizza_menu import AVAILABLE_PIZZA_SIZES


class PizzaException(Exception):
    """Main Pizza Exception"""


class PizzaSizeException(PizzaException):
    """Raise when a pizza size is not available"""

    def __init__(self, pizza_size):
        full_message = f"{pizza_size} size is not available. Choose one from: {AVAILABLE_PIZZA_SIZES}"
        super().__init__(full_message)
