#! /usr/bin/env python3
# coding: utf-8
import random
from faker import Faker
from db_connexion import SQLconnexion


class InjectRestaurantData:

    def __init__(self):
        self.fake_data = Faker("fr_FR")
        self.restaurants = ["OC-Pizza Paris13",
                            "OC-Pizza Paris18",
                            "OC-Pizza Paris9",
                            "OC-Pizza Vincennes",
                            "OC-Pizza Pantin"]

    def set_restaurants(self):

        # Get get address ids and put them into a list
        all_address_ids = self._get_address_ids()
        address_ids = [address["id"] for address in all_address_ids]

        # Get pizza ids and put them into a words_list
        all_pizza_ids = self._get_pizza_ids()
        pizza_ids = [pizza["id"] for pizza in all_pizza_ids]

        # Get ingredient informations (id + quantity)
        # Put each information into a list
        # Split global quantity into 5 equal parts because 5 restaurants
        all_ingredient_infos = self._get_ingredient_infos()
        ingredient_ids = [ingredient["id"] for ingredient in all_ingredient_infos]
        ingredients_quantity = [ingredient["quantite_globale"] for ingredient in all_ingredient_infos]
        ingr_qty_per_rest = [quantity / 5 for quantity in ingredients_quantity]

        # We get the employee id and put them into a list
        all_employee_ids = self._get_employee_ids()
        employee_ids = [employee['id_utilisateur'] for employee in all_employee_ids]

        # Invent fake date for start job
        date_list = []
        numb_date = 0
        while numb_date < 5:
            date = self.fake_data.date()
            date_list.append(date)
            numb_date += 1

        # We go for insertion
        for restaurant in self.restaurants:
            restaurant_info = {
                "id" : "",
                "name" : restaurant,
                "address_id" : address_ids.pop(),
                "pizza_ids" : pizza_ids,
                "ingredient_ids" : ingredient_ids,
                "ingredients_quantity" : ingr_qty_per_rest,
                "employee_ids" : random.sample(employee_ids, 5),
                "date_start" : date_list
            }

            print(restaurant_info)

            with SQLconnexion() as connexion:
                # We insert basic information into restaurant table
                with connexion.cursor() as cursor:
                    sql = """INSERT INTO restaurant (nom, id_adresse_location)
                        VALUES (%s, %s)"""

                    cursor.execute(sql, (restaurant_info["name"],
                                         restaurant_info["address_id"]))
                connexion.commit()

                # We get the restaurant id we just injected
                with connexion.cursor() as cursor:
                    sql = """SELECT id FROM restaurant
                        ORDER BY id DESC LIMIT 1"""
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    restaurant_info["id"] = result["id"]

                # We insert ingredients quantity per restaurant
                # We use the index to push the associated quantity
                for index, ingredient_id in enumerate(ingredient_ids):
                    with connexion.cursor() as cursor:
                        sql = """INSERT INTO stock_ingredient_par_restaurant
                                    (id_ingredient, id_restaurant, quantite_allouee)
                                VALUES (%s, %s, %s)"""
                        cursor.execute(sql, (ingredient_id,
                                             restaurant_info["id"],
                                             restaurant_info["ingredients_quantity"][index]))
                    connexion.commit()

                # We insert pizza availability on a basis way (all available for initialization)
                for pizza_id in pizza_ids:
                    with connexion.cursor() as cursor:
                        sql = """INSERT INTO disp_pizza_par_rest
                                    (id_pizza, id_restaurant, disponibilite)
                            VALUES (%s, %s, %s)"""
                        cursor.execute(sql, (pizza_id,
                                             restaurant_info["id"],
                                             "disponible"))
                    connexion.commit()

                # We insert employee staff
                for index, employe_id in enumerate(employee_ids):
                    with connexion.cursor() as cursor:
                        sql = """INSERT INTO staff
                                    (id_restaurant, id_utilisateur, date_debut, date_fin)
                                VALUES(%s, %s, %s, %s)"""
                        cursor.execute(sql, (restaurant_info["id"],
                                             employe_id,
                                             restaurant_info["date_start"][index],
                                             restaurant_info["date_start"][index]))
                    connexion.commit()

    def _get_address_ids(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id FROM adresse"""
                cursor.execute(sql)
                address_ids = cursor.fetchall()
                return address_ids

    def _get_ingredient_infos(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id, quantite_globale FROM ingredient"""
                cursor.execute(sql)
                ingredient_infos = cursor.fetchall()
                return ingredient_infos

    def _get_pizza_ids(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id FROM pizza"""
                cursor.execute(sql)
                pizza_ids = cursor.fetchall()
                return pizza_ids

    def _get_employee_ids(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id_utilisateur FROM employe"""
                cursor.execute(sql)
                employe_id = cursor.fetchall()
                return employe_id
