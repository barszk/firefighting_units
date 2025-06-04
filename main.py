from tkinter import *

import tkintermapview

users:list = []

class User:
    def __init__(self, unit_name, location, all_employees, selected_employees, fire_places, extinguished_fires):
        self.unit_name = unit_name
        self.location = location
        self.all_employees = all_employees
        self.selected_employees = selected_employees
        self.fire_places = fire_places
        self.extinguished_fires = extinguished_fires
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        address_url: str = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(address_url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude: float = float(response_html.select(".longitude")[1].text.replace(",", "."))
        # print(longitude)
        latitude: float = float(response_html.select(".latitude")[1].text.replace(",", "."))
        # print(latitude)
        return [latitude, longitude]

    def add_unit():