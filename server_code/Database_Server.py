import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def get_users():
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    res = cursor.execute("SELECT UID, name FROM users").fetchall()
    return [(row[1], row[0]) for row in res]  # (name, UID) pairs

@anvil.server.callable
def get_prices():
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    res = cursor.execute("SELECT price_id, price FROM prices").fetchall()
    return [(str(row[1]), row[0]) for row in res]  # (price, price_id) pairs

@anvil.server.callable
def get_room_types():
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    res = cursor.execute("SELECT room_type_id, type_name FROM room_types").fetchall()
    return [(row[1], row[0]) for row in res]  # (type_name, room_type_id) pairs

@anvil.server.callable
def get_price_categories():
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    res = cursor.execute("SELECT IDPreiskategorie, Preis FROM tblPreiskategorie").fetchall()
    return [(f"{price} €", price_id) for price_id, price in res]


@anvil.server.callable
def get_guest_counts():
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    res = cursor.execute("SELECT guest_count_id, count FROM guest_counts").fetchall()
    return [(str(row[1]), row[0]) for row in res]  # (count, guest_count_id) pairs

@anvil.server.callable
def book_room(zid):
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    cursor.execute("UPDATE zimmer SET gebucht = 1 WHERE ZID = ?", (zid,))
    conn.commit()
    return {"status": "success"}
