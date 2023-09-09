"""Module to create parametrization for tests.

all_pizzas_parameters: all pizzas (real class) from the menu
all_types_delivery: all types of delivery (True, False).
"""
import pytest

from pizza.pizza_menu import pizza_menu

all_pizzas_parameters = pytest.mark.parametrize(
    "pizza_class",
    list(pizza_menu.values()),
)
all_types_delivery = pytest.mark.parametrize("is_delivery", [True, False])
