import pytest

from pizza.pizza_menu import Pepperoni, Margherita, Hawaiian

# parameters for tests:
all_pizzas_parameters = pytest.mark.parametrize(
    "pizza_class",
    [
        Pepperoni,
        Margherita,
        Hawaiian,
    ],
)
all_types_delivery = pytest.mark.parametrize("is_delivery", [True, False])
