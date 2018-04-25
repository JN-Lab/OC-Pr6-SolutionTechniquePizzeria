#! /usr/bin/env python3
# coding: utf-8
import random
from faker import Faker
from db_connexion import SQLconnexion


class InjectOrderData:

    def __init__(self):
        self.fake_data = Faker("fr_FR")
        self.delivery_types = ["sur place", "web", "telephone"]
        self.payment_methods = ["CB", "espece"]
        self.payment_status = ["en attente", "paye"]
        self.order_status = ["en attente", "en preparation", "en livraison", "livree"]

    def set_delivery_types(self):
        with SQLconnexion() as connexion:
            for delivery_type in self.delivery_types:
                with connexion.cursor() as cursor:
                    sql = """INSERT INTO type_livraison (type_livraison)
                        VALUES (%s)"""
                    cursor.execute(sql, (delivery_type))
                connexion.commit()

    def set_payment_methods(self):
        with SQLconnexion() as connexion:
            for payment_method in self.payment_methods:
                with connexion.cursor() as cursor:
                    sql = """INSERT INTO mode_reglement (mode_reglement)
                        VALUES (%s)"""
                    cursor.execute(sql, (payment_method))
                connexion.commit()

    def set_payment_status(self):
        with SQLconnexion() as connexion:
            for status in self.payment_status:
                with connexion.cursor() as cursor:
                    sql = """INSERT INTO statut_paiement (statut_paiement)
                        VALUES (%s)"""
                    cursor.execute(sql, (status))
                connexion.commit()

    def set_order_status(self):
        with SQLconnexion() as connexion:
            for status in self.order_status:
                with connexion.cursor() as cursor:
                    sql = """INSERT INTO statut_commande (statut_commande)
                        VALUES (%s)"""
                    cursor.execute(sql, (status))
                connexion.commit()

    def set_order(self, number):

        # We get address_ids
        all_address_ids = self._get_address_ids()
        address_ids = [address["id"] for address in all_address_ids]

        # We get pizza informations
        all_pizza_infos = self._get_pizza_informations()

        # We get the restaurant ids
        all_restaurant_ids = self._get_restaurant_ids()
        restaurant_ids = [restaurant['id'] for restaurant in all_restaurant_ids]

        with SQLconnexion() as connexion:
            numb_order = 0
            while numb_order < number:

                selected_pizza = random.sample(all_pizza_infos, 3)
                pizza_infos = {
                    "ids" : [pizza['id'] for pizza in selected_pizza],
                    "qties" : random.choices(range(1,4), k=3),
                    "unit_prices" : [pizza["prix_unitaire"] for pizza in selected_pizza],
                    "price_per_pizza_types" : []
                }
                pizza_infos["price_per_pizza_types"] = [qty * unit_price for qty, unit_price in zip(pizza_infos["qties"], pizza_infos["unit_prices"])]

                order = {
                    "id" : "",
                    "amount" : sum(pizza_infos["price_per_pizza_types"]),
                    "date" : self.fake_data.date_this_year(),
                    "delivery_address_id" : self.fake_data.random_element(elements=address_ids),
                    "invoice_address_id" : self.fake_data.random_element(elements=address_ids),
                    "delivery_type": self.fake_data.random_element(elements=self.delivery_types),
                    "payment_method": self.fake_data.random_element(elements=self.payment_methods),
                    "payment_status": self.fake_data.random_element(elements=self.payment_status),
                    "order_status": "en attente",
                    "restaurant_id" : self.fake_data.random_element(elements=restaurant_ids),
                }

                print(pizza_infos)
                print(order)
                numb_order += 1

    def _get_address_ids(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id FROM adresse"""
                cursor.execute(sql)
                address_ids = cursor.fetchall()
                return address_ids

    def _get_pizza_informations(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id, prix_unitaire FROM pizza"""
                cursor.execute(sql)
                pizza_infos = cursor.fetchall()
                return pizza_infos

    def _get_restaurant_ids(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id FROM restaurant"""
                cursor.execute(sql)
                restaurant_ids = cursor.fetchall()
                return restaurant_ids
