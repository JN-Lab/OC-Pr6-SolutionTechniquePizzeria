#! /usr/bin/env python3
# coding: utf-8
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
