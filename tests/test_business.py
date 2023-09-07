"""Tests for business logic (client, restaurant, pizza)
I probably need to clean methods in classes from decorators using __wrapped__"""
from pizza.pizza_menu import (
    pizza_menu,
)
from pizza.business import Restaurant, Client
from tests.help_funcs import all_pizzas_parameters, all_types_delivery

Restaurant = Restaurant.__wrapped__
Client = Client.__wrapped__


@all_pizzas_parameters
def test_pizza_equality(pizza_class):
    """Test equality and inequality of the same pizza"""
    assert pizza_class() == pizza_class()
    assert pizza_class(size="M") != pizza_class(size="L")


@all_types_delivery
def test_pizza_order(is_delivery):
    """Test that client ordered 2 pizzas, has 2 pizzas in his stock
    And pizzas are baked
    No pizza left in a restaurant"""
    restaurant = Restaurant(pizza_menu)
    client = Client(is_delivery=is_delivery, restaurant=restaurant)
    client.order("Pepperoni")
    client.order("Pepperoni")
    assert len(client.stock) == 2
    assert len(restaurant._stock) == 0
    assert all([i.is_baked is True for i in client.stock])


@all_pizzas_parameters
def test_different_pizza(pizza_class):
    """Test that pizzas can be baked and they're pizzas indeed"""
    pizza = pizza_class()
    assert pizza.type_of_food == "pizza"
    assert pizza.is_baked is False
    pizza.bake()
    assert pizza.is_baked is True


@all_types_delivery
def test_pizza_order_diff_clients(is_delivery):
    """Test that pizza is picked up and delivered to a client who ordered
    Side note: checks aren't meaningful because orders are blocking sequential
    """
    restaurant = Restaurant(pizza_menu)
    client1 = Client(name="PP1", is_delivery=True, restaurant=restaurant)
    client2 = Client(name="PP2", is_delivery=False, restaurant=restaurant)
    client1.order("Pepperoni")
    client2.order("Pepperoni")
    assert client1 != client2
    assert len(restaurant._stock) == 0
    assert len(client1.stock) == 1
    assert len(client2.stock) == 1
