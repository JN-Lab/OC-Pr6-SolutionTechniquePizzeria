#! /usr/bin/env python3
# coding: utf-8
from db_connexion import SQLconnexion
from faker import Faker

class InjectUserData:

    def __init__(self):
        self.fake_data = Faker("fr_FR")
        self.roles = ["responsable groupe", "responsable restaurant", "pizzaiolo", "vendeur", "livreur"]

    ## INSERT FAKE ROLE ##
    def set_role(self):

        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                for role in self.roles:
                    sql = """SELECT nom FROM role WHERE nom = %s"""
                    cursor.execute(sql, (role))
                    result = cursor.fetchone()
                    if not result:
                        sql = "INSERT INTO role (nom) VALUES (%s)"
                        cursor.execute(sql, (role))
            connexion.commit()

    ## INSERT FAKE EMPLOYEES ##
    def set_employees(self, number):

        numb_employees = 0
        while numb_employees < number:
            employee = {
                "name": self.fake_data.last_name(),
                "first_name" : self.fake_data.first_name(),
                "mail" : self.fake_data.free_email(),
                "password" : self.fake_data.password(40),
                "role" : self.fake_data.random_element(elements=self.roles),
                "creation_date" : self.fake_data.date()
                }

            # insert user and get its id
            self.set_user(employee)
            user_id = self.get_last_user_id_injected()

            # get role id from employee dict
            role_id = self.get_role_id(employee['role'])

            # insert set_employee
            self.set_one_employee(user_id, role_id)

            numb_employees += 1

    def get_role_id(self, role_name):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id FROM role WHERE nom = %s"""
                cursor.execute(sql, (role_name))
                role = cursor.fetchone()
                return role["id"]

    def set_one_employee(self, user_id, role_id):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """INSERT INTO employe (id_utilisateur, id_role)
                    VALUES (%s, %s)"""
                cursor.execute(sql, (user_id, role_id))
            connexion.commit()

    # INSERT FAKE CUSTOMERS ##
    def set_customers(self, number):

        numb_customer = 0
        while numb_customer < number:
            customer = {
                "name": self.fake_data.last_name(),
                "first_name" : self.fake_data.first_name(),
                "mail" : self.fake_data.free_email(),
                "password" : self.fake_data.password(255),
                "creation_date" : self.fake_data.date(),
                "delivery_address" : {
                    "person" : self.fake_data.name(),
                    "street" : self.fake_data.street_address(),
                    "street_number" : self.fake_data.random_int(min=1, max=250),
                    "zip_code" : self.fake_data.random_int(min=10000, max=99999),
                    "info_bonus" : self.fake_data.sentence(6),
                    "city" : self.fake_data.city(),
                    "phone_number" : self.fake_data.phone_number()},
                "invoice_address" : {
                    "person" : self.fake_data.name(),
                    "street" : self.fake_data.street_address(),
                    "street_number" : self.fake_data.random_int(min=1, max=250),
                    "zip_code" : self.fake_data.random_int(min=10000, max=99999),
                    "info_bonus" : self.fake_data.sentence(6),
                    "city" : self.fake_data.city(),
                    "phone_number" : self.fake_data.phone_number()}
                }

            # Insert delivery_address and get its id
            self.set_address(customer["delivery_address"])
            delivery_address_id = self.get_last_adress_id_injected()
            #insert invoice_address and get its id
            self.set_address(customer["invoice_address"])
            invoice_address_id = self.get_last_adress_id_injected()

            # User insertion
            self.set_user(customer)

            # get  user id
            user_id = self.get_last_user_id_injected()

            # Insert set_customer
            self.set_one_customer(user_id, delivery_address_id, invoice_address_id)

            numb_customer += 1

    def set_one_customer(self, user_id, delivery_address_id, invoice_address_id):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """INSERT INTO client (id_utilisateur, id_adresse_livraison, id_adresse_facturation)
                        VALUES (%s, %s, %s )"""
                cursor.execute(sql, (user_id, delivery_address_id, invoice_address_id))
            connexion.commit()

    def set_address(self, address_elements):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """INSERT INTO adresse
                        (destinataire, voie, code_postal, ville,
                        renseignement_supplementaire, telephone, numero_voie)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (address_elements["person"],
                                     address_elements["street"],
                                     address_elements["zip_code"],
                                     address_elements["city"],
                                     address_elements["info_bonus"],
                                     address_elements["phone_number"],
                                     address_elements["street_number"]))
            connexion.commit()

    def get_last_adress_id_injected(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id FROM adresse ORDER BY id DESC LIMIT 1"""
                cursor.execute(sql)
                address_id = cursor.fetchone()
                return address_id["id"]

    def set_user(self, user_elements):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """INSERT INTO utilisateur (nom, prenom, mail, password, date_creation)
                    VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (user_elements["name"],
                                     user_elements["first_name"],
                                     user_elements["mail"],
                                     user_elements["password"],
                                     user_elements["creation_date"]))
            connexion.commit()

    def get_last_user_id_injected(self):
        with SQLconnexion() as connexion:
            with connexion.cursor() as cursor:
                sql = """SELECT id FROM utilisateur ORDER BY id DESC LIMIT 1"""
                cursor.execute(sql)
                user_id = cursor.fetchone()
                return user_id["id"]
