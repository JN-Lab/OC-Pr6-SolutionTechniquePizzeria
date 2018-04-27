#! /usr/bin/env python3
# coding: utf-8
import random
import datetime
from db_connexion import SQLconnexion

class DataInteractions:

    def __init__(self):
        pass

    def modify_some_orders_status(self):
        """The objective of this method is to create some interactions with orders
        which had been injected and pass them from 'en attente' statut to
        'en preparation' status """

        # We get 10 order_ids on a random way
        orders = self._get_10_orders()

        # on modifie leur statut de commande à en preparations en ajoutant 30 minutes ou 2heures
        with SQLconnexion() as connexion:
            for order in orders:
                step_date = order["date_debut_operation"] + datetime.timedelta(minutes=random.randint(10, 75))
                with connexion.cursor() as cursor:
                    sql = """UPDATE evolution_preparation
                            SET date_fin_operation = %s
                            WHERE id_commande = %s"""
                    cursor.execute(sql, (step_date,
                                         order["id_commande"]))
                connexion.commit()

                with connexion.cursor() as cursor:
                    sql = """INSERT INTO evolution_preparation
                                (id_commande, id_statut_commande,
                                date_debut_operation, date_fin_operation)
                            VALUES (%s, %s, %s, NULL)"""
                    cursor.execute(sql, (order["id_commande"],
                                         "2",
                                         step_date))
                connexion.commit()


    def _get_10_orders(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id_commande, date_debut_operation FROM evolution_preparation
                    ORDER BY RAND() LIMIT 10"""
                cursor.execute(sql)
                orders = cursor.fetchall()
                return orders

    def modify_some_ingredients_quantity_per_restaurants(self):
        """The objective of this method is to update the quantity of some ingredients
        for some restaurants to zero on a random way"""

        ingredients = self._get_ingredients_quantity_per_restaurant()

        # We get a sample of 6 ingredients-restaurants
        sample_ingredients = random.sample(ingredients, 6)

        with SQLconnexion() as connexion:
            for ingredient in sample_ingredients:

                # We get initial quantity before to set it to zero
                initial_quantity = 0
                with connexion.cursor() as cursor:
                    sql = """SELECT quantite_allouee FROM stock_ingredient_par_restaurant
                            WHERE id_ingredient = %s AND id_restaurant = %s"""
                    cursor.execute(sql, (ingredient["id_ingredient"],
                                         ingredient["id_restaurant"]))
                    quantity = cursor.fetchone()
                    initial_quantity = quantity["quantite_allouee"]

                # We set the quantity to zero
                with connexion.cursor() as cursor:
                    sql = """UPDATE stock_ingredient_par_restaurant
                            SET quantite_allouee = '0'
                            WHERE id_ingredient = %s AND id_restaurant = %s"""
                    cursor.execute(sql, (ingredient["id_ingredient"],
                                         ingredient["id_restaurant"]))
                connexion.commit()

                # We update the global quantity from this ingredient on ingredient table
                with connexion.cursor() as cursor:
                    sql = """UPDATE ingredient
                            SET quantite_globale = quantite_globale - %s
                            WHERE id = %s"""
                    cursor.execute(sql, (initial_quantity,
                                         ingredient["id_ingredient"]))
                connexion.commit()



    def _get_ingredients_quantity_per_restaurant(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT * FROM stock_ingredient_par_restaurant"""
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
