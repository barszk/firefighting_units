from tkinter import *
import tkintermapview

fire_units = []
firefighters = []
fires = []


class FireUnit:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.firefighters = []
        self.fires = []
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=name)

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.location}"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            lat = float(soup.select(".latitude")[1].text.replace(",", "."))
            lon = float(soup.select(".longitude")[1].text.replace(",", "."))
            return [lat, lon]
        except:
            return [latitude, longitude]

class Firefighter:
    def __init__(self, name, unit: FireUnit):
        self.name = name
        self.unit = unit
        self.coordinates = unit.coordinates
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=name)

class FireEvent:
    def __init__(self, location, unit: FireUnit):
        self.location = location
        self.unit = unit
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"Pożar: {location}")

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.location}"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            lat = float(soup.select(".latitude")[1].text.replace(",", "."))
            lon = float(soup.select(".longitude")[1].text.replace(",", "."))
            return [lat, lon]
        except:
            return [latitude, longitude]











