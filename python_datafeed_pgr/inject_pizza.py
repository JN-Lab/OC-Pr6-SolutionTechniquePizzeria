#! /usr/bin/env python3
# coding: utf-8
import random
from db_connexion import SQLconnexion
from faker import Faker

class InjectPizzaData:

    def __init__(self):
        self.fake_data = Faker("fr_FR")
        self.ingredients = ["tomate", "mozzarella", "jambon", "champignon", "viande hachée", "merguez", "poivrons", "gorgonzola", "emmental", "oignon", "basilic"]
        self.pizzas = ["reine", "orientale", "tex mex", "4 fromages", "margharita", "savoyarde", "al carne"]
        self.categories = ["vegetarienne", "base creme fraiche", "base sauce tomate", "light", "pour les gourmands", "edition limitée", "classiques"]

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
                    "sub_categories" : random.sample(self.categories, random.randint(0, 3))
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

        ingredient_ids = self._get_ingredient_ids()
        print(ingredient_ids)
        recipe_ids = self._get_recipe_ids()
        category_ids = self._get_category_ids()
        category_associations = self._get_category_ids_association()
        print(category_associations)
        #get ingredients id
        #get recette
        #get categorie id and category association

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

    def _get_category_ids(self):

        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id FROM categorie_pizza"""
                cursor.execute(sql)
                category_ids = cursor.fetchall()
                return category_ids

    def _get_category_ids_association(self):

        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id_cat_parent, id_cat_enfant FROM sous_cat_par_cat"""
                cursor.execute(sql)
                category_associations = cursor.fetchall()
                return category_associations
