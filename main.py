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

def show_unit_details():
    idx = listbox_units.curselection()
    if not idx:
        messagebox.showerror("Błąd", "Wybierz jednostkę!")
        return
    unit = fire_units[idx[0]]
    if unit.firefighters:
        details = "Strażacy:\n" + "\n".join(f" - {ff.name}" for ff in unit.firefighters)
    else:
        details = "Brak strażaków."
    messagebox.showinfo(f"Szczegóły: {unit.name}", details)

def show_only_units():
    clear_markers()
    for unit in fire_units:
        m = map_widget.set_marker(unit.coordinates[0], unit.coordinates[1], text=f"Jednostka: {unit.name}")
        active_markers.append(m)

def show_only_fires():
    clear_markers()
    for fire in fires:
        m = map_widget.set_marker(fire.coordinates[0], fire.coordinates[1], text=f"Pożar: {fire.location}")
        active_markers.append(m)

def show_selected_unit_fires():
    idx = listbox_units.curselection()
    if not idx:
        messagebox.showerror("Błąd", "Wybierz jednostkę!")
        return
    unit = fire_units[idx[0]]
    clear_markers()
    m = map_widget.set_marker(unit.coordinates[0], unit.coordinates[1], text=f"Jednostka: {unit.name}")
    active_markers.append(m)
    for fire in unit.fires:
        m = map_widget.set_marker(fire.coordinates[0], fire.coordinates[1], text=f"Pożar: {fire.location}")
        active_markers.append(m)

# GUI główny układ
root = Tk()
root.title("System Straży Pożarnej")
root.geometry("1200x800")
root.configure(bg="lightgray")

frame_top = Frame(root, bg="lightgray", pady=10)
frame_top.pack(side=TOP, fill=X)

frame_units = Frame(frame_top, bg="lightgray")
frame_units.grid(row=0, column=0, columnspan=8, pady=2, sticky=W)
Label(frame_units, text="Jednostka:", bg="lightgray").grid(row=0, column=0, sticky=E)
entry_unit_name = Entry(frame_units, width=20); entry_unit_name.grid(row=0, column=1, padx=5)
Label(frame_units, text="Lokalizacja:", bg="lightgray").grid(row=0, column=2, sticky=E)
entry_unit_location = Entry(frame_units, width=20); entry_unit_location.grid(row=0, column=3, padx=5)
Button(frame_units, text="Dodaj", command=add_fire_unit).grid(row=0, column=4, padx=5)
Button(frame_units, text="Edytuj", command=edit_fire_unit).grid(row=0, column=5, padx=5)
Button(frame_units, text="Usuń", command=delete_fire_unit).grid(row=0, column=6, padx=5)
Button(frame_units, text="Szczegóły", command=show_unit_details).grid(row=0, column=7, padx=5)

frame_ff = Frame(frame_top, bg="lightgray")
frame_ff.grid(row=1, column=0, columnspan=8, pady=2, sticky=W)
Label(frame_ff, text="Strażak:", bg="lightgray").grid(row=0, column=0, sticky=E)
entry_firefighter_name = Entry(frame_ff, width=20); entry_firefighter_name.grid(row=0, column=1, padx=5)
Button(frame_ff, text="Dodaj", command=add_firefighter).grid(row=0, column=2, padx=5)
Button(frame_ff, text="Edytuj", command=edit_firefighter).grid(row=0, column=3, padx=5)
Button(frame_ff, text="Usuń", command=delete_firefighter).grid(row=0, column=4, padx=5)

frame_fires = Frame(frame_top, bg="lightgray")
frame_fires.grid(row=2, column=0, columnspan=8, pady=2, sticky=W)
Label(frame_fires, text="Pożar:", bg="lightgray").grid(row=0, column=0, sticky=E)
entry_fire_location = Entry(frame_fires, width=20); entry_fire_location.grid(row=0, column=1, padx=5)
Button(frame_fires, text="Dodaj", command=add_fire).grid(row=0, column=2, padx=5)
Button(frame_fires, text="Edytuj", command=edit_fire).grid(row=0, column=3, padx=5)
Button(frame_fires, text="Usuń", command=delete_fire).grid(row=0, column=4, padx=5)

frame_map_buttons = Frame(frame_top, bg="lightgray")
frame_map_buttons.grid(row=3, column=0, columnspan=8, pady=5, sticky=W)
Button(frame_map_buttons, text="Mapa jednostek", command=show_only_units).grid(row=0, column=0, padx=5)
Button(frame_map_buttons, text="Mapa pożarów", command=show_only_fires).grid(row=0, column=1, padx=5)
Button(frame_map_buttons, text="Mapa pożarów wybranej jednostki", command=show_selected_unit_fires).grid(row=0, column=2, padx=5)

frame_lists = Frame(root, bg="lightgray")
frame_lists.pack(fill=X, padx=10, pady=5)
listbox_units = Listbox(frame_lists, width=40, height=10); listbox_units.grid(row=0, column=0, padx=10)
listbox_firefighters = Listbox(frame_lists, width=40, height=10); listbox_firefighters.grid(row=0, column=1, padx=10)
listbox_fires = Listbox(frame_lists, width=40, height=10); listbox_fires.grid(row=0, column=2, padx=10)

frame_map = Frame(root)
frame_map.pack(fill=BOTH, expand=True, padx=10, pady=10)
map_widget = tkintermapview.TkinterMapView(frame_map, width=1150, height=400)
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(5)
map_widget.pack()

root.mainloop()