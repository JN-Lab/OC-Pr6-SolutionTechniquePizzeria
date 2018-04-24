#! /usr/bin/env python3
# coding: utf-8
from faker import Faker

class InjectOrderData:

    def __init__(self):
        self.fake_data = Faker("fr_FR")
        self.delivery_type = ["sur place", "web", "telephone" ]
        self.payment_method = ["CB", "espece"]
        self.payment_status = ["en attente", "paye"]
        self.order_status = ["en attente", "en preparation", "en livraison", "livree"]
