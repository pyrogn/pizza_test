import pytest

from pizza.pizza_menu import pizza_menu, Pepperoni, Margherita, Hawaiian

# parameters for tests:
all_pizzas_parameters = pytest.mark.parametrize(
    "pizza_class", [klass for klass in pizza_menu.values()]
)
all_types_delivery = pytest.mark.parametrize("is_delivery", [True, False])
