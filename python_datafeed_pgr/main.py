#! /usr/bin/env python3
# coding: utf-8
from faker_generator import FakerGenerator

def main():
    data = FakerGenerator()
    data.get_json_file("data.json")
    print(data.fake_data)

if __name__ == "__main__":
    main()
