#! /usr/bin/env python3
# coding: utf-8
import random
from faker import Faker
from db_connexion import SQLconnexion

class InjectPizzaData:

    def __init__(self):
        self.fake_data = Faker("fr_FR")
        self.ingredients = ["tomate", "mozzarella", "jambon", "champignon", "viande hachée", "merguez", "poivrons", "gorgonzola", "emmental", "oignon", "basilic"]
        self.pizzas = ["reine", "orientale", "tex mex", "4 fromages", "margharita", "savoyarde", "al carne"]
        self.categories = ["vegetarienne", "base creme fraiche", "base sauce tomate", "light", "pour les gourmands", "edition limitée", "classiques", "nouveauté", "sans porc", "sans gluten", "calzone"]

    def set_ingredients(self):

        with SQLconnexion() as connexion:
            for ingredient in self.ingredients:
                ingredient_info = {
                    "name" : ingredient,
                    "price_per_unit" : round(random.uniform(1.0, 15.0), 2),
                    "global_quantity" : random.randint(1, 50)
                }

                with connexion.cursor() as cursor:
                    sql = """INSERT INTO ingredient (nom, prix_unitaire, quantite_globale)
                        VALUES (%s, %s, %s)"""
                    cursor.execute(sql, (ingredient_info["name"],
                                         ingredient_info["price_per_unit"],
                                         ingredient_info["global_quantity"]))
                connexion.commit()

    def set_recipes(self, number):

        words_list = ["recette", "pizza", "four", "sauce tomate", "fromage",
                      "origan", "enfourner", "ajouter le jambon", "cuire",
                      "étaler la pate", "croquante", "saler", "poivrer"]

        with SQLconnexion() as connexion:
            numb_recipes = 0
            while numb_recipes < number:
                recipe = {
                    "recipe" : "La recette de " + self.fake_data.random_element(elements=self.pizzas),
                    "description" : self.fake_data.sentence(nb_words=30, ext_word_list=words_list)
                }
                with connexion.cursor() as cursor:
                    sql = """INSERT INTO recette (recette, description)
                        VALUES (%s, %s)"""
                    cursor.execute(sql, (recipe["recipe"], recipe["description"]))
                connexion.commit()

                numb_recipes += 1

    def set_categories(self):

        with SQLconnexion() as connexion:
            for category in self.categories:
                category_info = {
                    "id" : "",
                    "name" : category,
                    "sub_categories" : random.sample(self.categories, random.randint(2, 4))
                }

                with connexion.cursor() as cursor:
                    sql = """INSERT INTO categorie_pizza (nom_categorie)
                            VALUES (%s)"""
                    cursor.execute(sql, (category_info["name"]))
                connexion.commit()

                with connexion.cursor() as cursor:
                    sql = """SELECT id FROM categorie_pizza
                            WHERE nom_categorie = %s"""
                    cursor.execute(sql, (category_info["name"]))
                    result = cursor.fetchone()
                    category_info["id"] = result["id"]

                for sub_category in category_info["sub_categories"]:
                    with connexion.cursor() as cursor:
                        sql = """INSERT INTO sous_cat_par_cat (id_cat_parent, id_cat_enfant)
                                SELECT %s, id AS id_enfant
                                FROM categorie_pizza
                                WHERE nom_categorie = %s"""
                        cursor.execute(sql, (category_info['id'], sub_category))
                    connexion.commit()

    def set_pizza(self):

        # We get information already inserted
        ingredient_ids = self._get_ingredient_ids()
        recipe_ids = self._get_recipe_ids()
        category_associations = self._get_category_ids_association()


        # For each pizza in the list, we insert all the information
        for pizza in self.pizzas:
            ## WE SET UP THE NECESSARY DATAS FOR EACH PIZZA ##
            pizza_info = {
                "id" : "",
                "name" : pizza,
                "description" : self.fake_data.sentence(15),
                "price_per_unit" : round(random.uniform(9.90, 16.90), 2),
                "recipe_id" : recipe_ids.pop(), # get a {'id': X}
                "ingredient_ids" : random.sample(ingredient_ids, 3), # get a ({'id': X}, {'id': X}, {'id': X})
                "category_associations" : random.sample(category_associations, 2)
            }

            # We define a simple list of ingedient ids from the sample
            simple_ingredient_ids = [ingredient['id'] for ingredient in pizza_info["ingredient_ids"]]

            # We defin a coherent and simple list of category_ids
            all_category_ids = [category['id_cat_parent'] for category in pizza_info["category_associations"]] + \
                                  [category['id_cat_enfant'] for category in pizza_info["category_associations"]]
            simple_category_ids = list(set(all_category_ids))

            ##  WE START THE INSERTION ##
            with SQLconnexion() as connexion:
                # We had basic pizza info into pizza Table
                with connexion.cursor() as cursor:
                    sql = """INSERT INTO pizza
                                (nom, description, prix_unitaire, id_recette)
                        VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, (pizza_info["name"],
                                         pizza_info["description"],
                                         pizza_info["price_per_unit"],
                                         pizza_info['recipe_id']["id"]))
                connexion.commit()

                # We get the pizza id we just created thanks to th insertion
                with connexion.cursor() as cursor:
                    sql = """SELECT id FROM pizza ORDER BY id DESC LIMIT 1"""
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    pizza_info["id"] = result["id"]

                # For each category ids, we insert the pizza_id and category_id associations
                for category_id in simple_category_ids:
                    with connexion.cursor() as cursor:
                        sql = """INSERT INTO categorie_par_pizza (id_pizza, id_categorie)
                            VALUES (%s, %s)"""
                        cursor.execute(sql, (pizza_info["id"], category_id))
                    connexion.commit()

                # For each ingredients_ids, we link ingredients to the pizza and set up arbitrary the global_quantity
                for ingredient_id in simple_ingredient_ids:
                    necessary_quantity = round(random.random(), 2)
                    with connexion.cursor() as cursor:
                        sql = """INSERT INTO quantite_ingredient_par_pizza
                                    (id_ingredient, id_pizza, quantite_necessaire)
                                VALUES (%s, %s, %s)"""
                        cursor.execute(sql, (ingredient_id,
                                             pizza_info["id"],
                                             necessary_quantity))
                    connexion.commit()

    def _get_ingredient_ids(self):

        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id FROM ingredient"""
                cursor.execute(sql)
                ingredient_ids = cursor.fetchall()
                return ingredient_ids

    def _get_recipe_ids(self):

        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id FROM recette"""
                cursor.execute(sql)
                recipe_ids = cursor.fetchall()
                return recipe_ids

    def _get_category_ids_association(self):

        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id_cat_parent, id_cat_enfant FROM sous_cat_par_cat"""
                cursor.execute(sql)
                category_associations = cursor.fetchall()
                return category_associations
