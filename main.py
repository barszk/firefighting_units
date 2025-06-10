from tkinter import *
import tkinter.messagebox as messagebox
from tkinter import simpledialog
import tkintermapview
import requests
from bs4 import BeautifulSoup

fire_units = []
firefighters = []
fires = []
active_markers = []

class FireUnit:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.firefighters = []
        self.fires = []

    def get_coordinates(self):
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.location}"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            lat = float(soup.select(".latitude")[1].text.replace(",", "."))
            lon = float(soup.select(".longitude")[1].text.replace(",", "."))
            return [lat, lon]
        except:
            return [52.23, 21.01]

class Firefighter:
    def __init__(self, name, unit: FireUnit):
        self.name = name
        self.unit = unit
        self.coordinates = unit.coordinates

class FireEvent:
    def __init__(self, location, unit: FireUnit):
        self.location = location
        self.unit = unit
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.location}"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            lat = float(soup.select(".latitude")[1].text.replace(",", "."))
            lon = float(soup.select(".longitude")[1].text.replace(",", "."))
            return [lat, lon]
        except:
            return [52.23, 21.01]

def clear_markers():
    global active_markers
    for marker in active_markers:
        marker.delete()
    active_markers.clear()

def update_all_markers():
    clear_markers()
    for unit in fire_units:
        m = map_widget.set_marker(unit.coordinates[0], unit.coordinates[1], text=unit.name)
        active_markers.append(m)
    for fire in fires:
        m = map_widget.set_marker(fire.coordinates[0], fire.coordinates[1], text=f"Pożar: {fire.location}")
        active_markers.append(m)

def add_fire_unit():
    name = entry_unit_name.get()
    loc = entry_unit_location.get()
    if not name or not loc:
        messagebox.showerror("Błąd", "Uzupełnij nazwę i lokalizację!")
        return
    unit = FireUnit(name, loc)
    fire_units.append(unit)
    listbox_units.insert(END, f"{name} ({loc})")
    entry_unit_name.delete(0, END)
    entry_unit_location.delete(0, END)
    update_all_markers()

def edit_fire_unit():
    idx = listbox_units.curselection()
    if not idx:
        messagebox.showerror("Błąd", "Wybierz jednostkę do edycji!")
        return
    unit = fire_units[idx[0]]
    new_name = simpledialog.askstring("Edytuj jednostkę", "Nowa nazwa:", initialvalue=unit.name)
    new_loc = simpledialog.askstring("Edytuj jednostkę", "Nowa lokalizacja:", initialvalue=unit.location)
    if not new_name or not new_loc:
        return
    unit.name = new_name
    unit.location = new_loc
    unit.coordinates = unit.get_coordinates()
    listbox_units.delete(idx)
    listbox_units.insert(idx, f"{new_name} ({new_loc})")
    update_all_markers()

def delete_fire_unit():
    idx = listbox_units.curselection()
    if not idx:
        messagebox.showerror("Błąd", "Wybierz jednostkę do usunięcia!")
        return
    unit = fire_units.pop(idx[0])
    for ff in unit.firefighters:
        if ff in firefighters:
            firefighters.remove(ff)
    for f in unit.fires:
        if f in fires:
            fires.remove(f)
    listbox_units.delete(idx[0])
    listbox_firefighters.delete(0, END)
    for ff in firefighters:
        listbox_firefighters.insert(END, f"{ff.name} (jednostka: {ff.unit.name})")
    listbox_fires.delete(0, END)
    for f in fires:
        listbox_fires.insert(END, f"Pożar: {f.location} (jednostka: {f.unit.name})")
    update_all_markers()

def add_firefighter():
    name = entry_firefighter_name.get()
    idx = listbox_units.curselection()
    if not idx or not name:
        messagebox.showerror("Błąd", "Wybierz jednostkę i wpisz imię strażaka!")
        return
    unit = fire_units[idx[0]]
    ff = Firefighter(name, unit)
    firefighters.append(ff)
    unit.firefighters.append(ff)
    listbox_firefighters.insert(END, f"{name} (jednostka: {unit.name})")
    entry_firefighter_name.delete(0, END)

def edit_firefighter():
    idx = listbox_firefighters.curselection()
    if not idx:
        messagebox.showerror("Błąd", "Wybierz strażaka do edycji!")
        return
    firefighter = firefighters[idx[0]]
    new_name = simpledialog.askstring("Edytuj strażaka", "Nowe imię:", initialvalue=firefighter.name)
    if not new_name:
        return
    firefighter.name = new_name
    listbox_firefighters.delete(idx)
    listbox_firefighters.insert(idx, f"{new_name} (jednostka: {firefighter.unit.name})")

def delete_firefighter():
    idx = listbox_firefighters.curselection()
    if not idx:
        messagebox.showerror("Błąd", "Wybierz strażaka do usunięcia!")
        return
    firefighter = firefighters.pop(idx[0])
    firefighter.unit.firefighters.remove(firefighter)
    listbox_firefighters.delete(idx[0])

def add_fire():
    loc = entry_fire_location.get()
    idx = listbox_units.curselection()
    if not idx or not loc:
        messagebox.showerror("Błąd", "Wybierz jednostkę i wpisz lokalizację!")
        return
    unit = fire_units[idx[0]]
    fire = FireEvent(loc, unit)
    fires.append(fire)
    unit.fires.append(fire)
    listbox_fires.insert(END, f"Pożar: {loc} (jednostka: {unit.name})")
    entry_fire_location.delete(0, END)
    update_all_markers()

def edit_fire():
    idx = listbox_fires.curselection()
    if not idx:
        messagebox.showerror("Błąd", "Wybierz pożar do edycji!")
        return
    fire = fires[idx[0]]
    new_loc = simpledialog.askstring("Edytuj pożar", "Nowa lokalizacja:", initialvalue=fire.location)
    if not new_loc:
        return
    fire.location = new_loc
    fire.coordinates = fire.get_coordinates()
    listbox_fires.delete(idx)
    listbox_fires.insert(idx, f"Pożar: {new_loc} (jednostka: {fire.unit.name})")
    update_all_markers()

def delete_fire():
    idx = listbox_fires.curselection()
    if not idx:
        messagebox.showerror("Błąd", "Wybierz pożar do usunięcia!")
        return
    fire = fires.pop(idx[0])
    fire.unit.fires.remove(fire)
    listbox_fires.delete(idx[0])
    update_all_markers()