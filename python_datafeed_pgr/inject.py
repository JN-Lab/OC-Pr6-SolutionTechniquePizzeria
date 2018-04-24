#! /usr/bin/env python3
# coding: utf-8
from inject_pizza import InjectPizzaData
from inject_user import InjectUserData
from inject_restaurant import InjectRestaurantData
from inject_order import InjectOrderData

class Inject:

    def __init__(self):
        self.inject_user = InjectUserData()
        self.inject_pizza = InjectPizzaData()
        self.inject_restaurant = InjectRestaurantData()
        self.inject_order = InjectOrderData()

    def start(self):
        self.inject_user.set_role()
        self.inject_user.set_employees(5)
        self.inject_user.set_customers(5)

        self.inject_pizza.set_ingredients()
        self.inject_pizza.set_recipes(10)
        self.inject_pizza.set_categories()
        self.inject_pizza.set_pizza()

        self.inject_restaurant.set_restaurants()

        self.inject_order.set_delivery_types()
        self.inject_order.set_payment_methods()
        self.inject_order.set_payment_status()
        self.inject_order.set_order_status()
