"""Tests for business logic (client, restaurant, pizza)."""
import pytest

from pizza.business import Client, Restaurant
from pizza.constants import AVAILABLE_PIZZA_SIZES
from pizza.pizza_menu import Pizza, pizza_menu, validate_pizza

from .help_funcs import all_pizzas_parameters, all_types_delivery

# CONFUSION: I don't know how to persuade linter
# to believe that they have this attribute
# To test decorated methods comment these 2 lines!!!
Restaurant = Restaurant.__wrapped__  # type: ignore
Client = Client.__wrapped__  # type: ignore

# To take random first actual values if they don't matter
first_pizza_name = next(iter(pizza_menu.values())).name
first_pizza_size = AVAILABLE_PIZZA_SIZES[0]
unk_pizza = "definitely_unknown_pizza"
unk_size = "definitely_unknown_size"


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
    n_orders = 20
    for _ in range(n_orders):
        client.make_order(first_pizza_name)
    assert len(client.get_stock()) == n_orders
    assert len(restaurant.get_stock()) == 0
    assert all(
        pizza.is_baked and isinstance(pizza, Pizza) is True
        for pizza in client.get_stock()
    )


@all_pizzas_parameters
def test_different_pizza(pizza_class: type[Pizza]):
    """Test that pizzas can be baked and they're pizzas indeed."""
    pizza = pizza_class()
    assert pizza.is_baked is False
    pizza.bake()
    assert pizza.is_baked is True


@all_pizzas_parameters
def test_unknown_size_pizza(pizza_class: type[Pizza]):
    """If size is unknown then ValueError is raised."""
    unk_size = "definitely_unknown_size"
    with pytest.raises(ValueError, match=rf"{unk_size} size is not in.*"):
        pizza_class(size=unk_size)


@pytest.mark.parametrize(
    ("pizza_name", "pizza_size", "is_valid"),
    [
        (first_pizza_name, first_pizza_size, True),
        (unk_pizza, first_pizza_size, False),
        (first_pizza_name, unk_size, False),
        (unk_pizza, unk_size, False),
    ],
)
def test_pizza_validation(pizza_name, pizza_size, is_valid):
    """Test that validation func don't allow incorrect pizza names and sizes"""
    flag, _ = validate_pizza(pizza_name=pizza_name, size=pizza_size)
    assert flag is is_valid


def test_pizza_order_diff_clients():
    """Test that pizza is picked up and delivered to a client who ordered.

    Side note: checks aren't meaningful because orders are blocking sequential.
    """
    restaurant = Restaurant(pizza_menu)
    client1 = Client(name="PP1", is_delivery=True, restaurant=restaurant)
    client2 = Client(name="PP2", is_delivery=False, restaurant=restaurant)
    client1.make_order("Pepperoni")
    client2.make_order("Pepperoni")
    assert client1 != client2
    assert len(restaurant.get_stock()) == 0
    assert len(client1.get_stock()) == 1
    assert len(client2.get_stock()) == 1
