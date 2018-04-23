#! /usr/bin/env python3
# coding: utf-8
from faker_generator import FakerGenerator
from inject import InjectData

def main():
    # data = FakerGenerator()
    # data.get_json_file("data.json")
    # data.set_fake_users(5)
    # data.set_fake_address(5)
    #
    # print(data.fake_data)

    inject = InjectData()
    inject.set_role()
    inject.set_employees(5)
    inject.set_customers(5)

if __name__ == "__main__":
    main()
