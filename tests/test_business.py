"""Tests for business logic (client, restaurant, pizza)."""
import pytest

from pizza.business import Client, Restaurant
from pizza.constants import AVAILABLE_PIZZA_SIZES
from pizza.pizza_menu import Pizza, pizza_menu, validate_pizza

from .help_funcs import all_pizzas_parameters, all_types_delivery

# CONFUSION: I don't know how to persuade linter
# to believe that they have this attribute
Restaurant = Restaurant.__wrapped__  # type: ignore
Client = Client.__wrapped__  # type: ignore

# To take random first actual values if they don't matter
first_pizza_name = next(iter(pizza_menu.values())).name
first_pizza_size = AVAILABLE_PIZZA_SIZES[0]


@all_pizzas_parameters
def test_pizza_equality(pizza_class: type[Pizza]):
    """Test equality and inequality of the same pizza."""
    assert pizza_class() == pizza_class()
    assert pizza_class(size="XL") != pizza_class(size="L")


def test_pizza_inequality():
    """Test on first two pizzas from menu that they are considered different."""
    if len(pizza_menu) > 1:
        pizza1, pizza2 = list(pizza_menu.values())[:2]
        assert pizza1(size="L") != pizza2(size="L")


@all_types_delivery
def test_pizza_order(is_delivery: bool):  # noqa: FBT001
    """Test that client ordered 2 pizzas, has 2 pizzas in his _stock.

    And pizzas are baked
    No pizza left in a restaurant for him.
    """
    restaurant = Restaurant(pizza_menu)
    client = Client(is_delivery=is_delivery, restaurant=restaurant)
    n_orders = 2
    for _ in range(n_orders):
        client.order(first_pizza_name)
    assert len(client._stock) == n_orders
    assert len(restaurant._stock) == 0
    assert all(pizza.is_baked is True for pizza in client._stock)


@all_pizzas_parameters
def test_different_pizza(pizza_class: type[Pizza]):
    """Test that pizzas can be baked and they're pizzas indeed."""
    pizza = pizza_class()
    assert pizza.type_of_food == "pizza"
    assert pizza.is_baked is False
    pizza.bake()
    assert pizza.is_baked is True


@all_pizzas_parameters
def test_unknown_size_pizza(pizza_class: type[Pizza]):
    """If size is unknown then ValueError is raised."""
    unk_size = "definitely_unknown_size"
    with pytest.raises(ValueError, match=rf"{unk_size} size is not in.*"):
        pizza_class(size=unk_size)


def test_pizza_validation():
    """Test that validation func don't allow incorrect pizza names and sizes"""
    known_pizza = first_pizza_name
    known_size = first_pizza_size
    unk_pizza = "definitely_unknown_pizza"
    unk_size = "definitely_unknown_size"
    test_cases = {
        (known_pizza, known_size): True,
        (unk_pizza, known_size): False,
        (known_pizza, unk_size): False,
        (unk_pizza, unk_size): False,
    }
    for case, result in test_cases.items():
        flag, _ = validate_pizza(pizza_name=case[0], size=case[1])
        assert flag is result


def test_pizza_order_diff_clients():
    """Test that pizza is picked up and delivered to a client who ordered.

    Side note: checks aren't meaningful because orders are blocking sequential.
    """
    restaurant = Restaurant(pizza_menu)
    client1 = Client(name="PP1", is_delivery=True, restaurant=restaurant)
    client2 = Client(name="PP2", is_delivery=False, restaurant=restaurant)
    client1.order("Pepperoni")
    client2.order("Pepperoni")
    assert client1 != client2
    assert len(restaurant._stock) == 0
    assert len(client1._stock) == 1
    assert len(client2._stock) == 1
