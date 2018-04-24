#! /usr/bin/env python3
# coding: utf-8
from inject_pizza import InjectPizzaData
from inject_user import InjectUserData

class Inject:

    def __init__(self):
        self.inject_user = InjectUserData()
        self.inject_pizza = InjectPizzaData()

    def start(self):
        self.inject_user.set_role()
        self.inject_user.set_employees(5)
        self.inject_user.set_customers(5)

        self.inject_pizza.set_ingredients()
        self.inject_pizza.set_recipes(10)
        self.inject_pizza.set_categories()
