import pizza.business as m
import pytest

import pizza.pizza_menu


@pytest.mark.parametrize(
    "pizza_class",
    [
        pizza.pizza_menu.Pepperoni,
        pizza.pizza_menu.Margherita,
        pizza.pizza_menu.Hawaiian,
    ],
)
def test_pizza_equality(pizza_class):
    assert pizza_class() == pizza_class()
    assert pizza_class(size="M") != pizza_class(size="L")


@pytest.mark.parametrize("is_delivery", [True, False])
def test_pizza_order(is_delivery):
    restaurant = m.Restaurant(pizza.pizza_menu.assortment)
    client = m.Client(is_delivery=is_delivery, restaurant=restaurant)
    client.order("Pepperoni")
    client.order("Pepperoni")
    assert len(client.stock) == 2
    assert len(restaurant._stock) == 0
    assert all(
        [i.is_baked is True for i in client.stock]
    )  # make sure that pizzas are cooked


@pytest.mark.parametrize(
    "pizza_class",
    [
        pizza.pizza_menu.Pepperoni,
        pizza.pizza_menu.Margherita,
        pizza.pizza_menu.Hawaiian,
    ],
)
def test_different_pizza(pizza_class):
    pizza = pizza_class()
    assert pizza.type_of_food == "pizza"
    assert pizza.is_baked is False
    pizza.bake()
    assert pizza.is_baked is True


@pytest.mark.parametrize("is_delivery", [True, False])
def test_pizza_order_diff_clients(is_delivery):
    """Test that pizza is picked up and delivered to a client who ordered
    Side note: checks aren't meaningful because orders are blocking sequential
    """
    restaurant = m.Restaurant(pizza.pizza_menu.assortment)
    client1 = m.Client(name="PP1", is_delivery=True, restaurant=restaurant)
    client2 = m.Client(name="PP2", is_delivery=False, restaurant=restaurant)
    client1.order("Pepperoni")
    client2.order("Pepperoni")
    assert client1 != client2
    assert len(restaurant._stock) == 0
    assert len(client1.stock) == 1
    assert len(client2.stock) == 1
