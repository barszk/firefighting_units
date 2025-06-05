from tkinter import *

import tkintermapview

fire_units:list = []

class FireUnit:
    def __init__(self, name,location):
        self.name = name
        self.location = location
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

def add_fire_unit():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    tmp_fire_unit = FireUnit(name = nazwa, location = miejscowosc)
    fire_units.append(tmp_fire_unit)

    print(fire_units)
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()
    show_fire_units()


def show_fire_units():
    listbox_lista_obiektow.delete(0, END)
    for idx,fire_unit in enumerate(fire_units):
        listbox_lista_obiektow.insert(idx, f"{idx+1}. {fire_unit.name}  {fire_unit.location}" )

def delete_fire_unit():
    idx=listbox_lista_obiektow.index(ACTIVE)
    fire_units[idx].marker.delete()
    fire_units.pop(idx)
    show_fire_units()

def fire_unit_details():
    idx=listbox_lista_obiektow.index(ACTIVE)
    label_name_szczegoly_obiektu_wartosc.configure(text=fire_units[idx].name)
    label_location_szczegoly_obiektu_wartosc.configure(text=fire_units[idx].location)
    map_widget.set_position(fire_units[idx].coordinates[0],fire_units[idx].coordinates[1])
    map_widget.set_zoom(16)











