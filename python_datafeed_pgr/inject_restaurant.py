#! /usr/bin/env python3
# coding: utf-8
from db_connexion import SQLconnexion

class InjectRestaurantData:

    def __init__(self):
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

        for restaurant in self.restaurants:
            restaurant_info = {
                "id" : "",
                "name" : restaurant,
                "address_id" : address_ids.pop(),
                "pizza_ids" : pizza_ids,
                "ingredient_ids" : ingredient_ids,
                "ingredients_quantity" : ingr_qty_per_rest
            }

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
