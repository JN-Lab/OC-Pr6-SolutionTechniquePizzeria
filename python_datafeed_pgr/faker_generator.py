#! /usr/bin/env python3
# coding: utf-8
import json
import os
import faker

class FakerGenerator:
    """ This class creates fake datas thansk to faker library and feed a json
    file to save them"""
    def __init__(self):
        self.fake_data = {}

    def get_json_file(self, file_name):
        directory = os.path.dirname(__file__)
        path_to_file = os.path.join(directory, file_name)
        print(path_to_file)
        try:
            with open(path_to_file, "r") as file:
                data = json.load(file)
                self.fake_data.update(data)
        except FileNotFoundError as error_message:
            print("The file was not found: ", error_message)
        except:
            print("Destination unknown")
