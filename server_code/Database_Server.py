import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3 

@anvil.server.callable
def get_location():
  con = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
  cursor = con.cursor()
  location_data = list(cursor.execute("SELECT name, JID FROM jugendherbergen"))
  con.commit()
  con.close()
  return location_data

@anvil.server.callable
def get_user():
  con = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
  cursor = con.cursor()
  user_data = list(cursor.execute("SELECT vorname, BeID FROM benutzer;"))
  con.commit()
  con.close()
  return user_data

@anvil.server.callable 
def get_category():
  con = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
  cursor = con.cursor()
  category_data = list(cursor.execute("SELECT name || ' ' || preis || '€' AS NamePreis, PID FROM preiskategorie;"))
  con.commit()
  con.close()
  return category_data

@anvil.server.callable
def get_selection(location_id, category_id):
  con = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
  cursor = con.cursor()
  selection_data = list(cursor.execute(f"SELECT 'NR:' || ZID || ' BETTEN: ' || bettenZahl AS NummerBettZahl, ZID FROM zimmer WHERE JID={location_id} AND PID = {category_id};"))
  con.commit()
  con.close()
  return selection_data

@anvil.server.callable
def booking(user_ids, start_date, end_date, selection_id):
  con = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
  cursor = con.cursor()
  print(start_date)
  cursor.execute(f"INSERT INTO buchung (startDatum, endDatum, ZID) VALUES ('{start_date}', '{end_date}', {selection_id}); ")
  con.commit()
  booking_id = cursor.lastrowid
  for user_id in user_ids:
    cursor.execute(f"INSERT INTO benutzerBuchung (BuID, BeID) VALUES ({booking_id}, {user_id});")
    con.commit()
  con.close()

@anvil.server.callable
def get_data():
  con = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
  cursor = con.cursor()
  data = list(cursor.execute("SELECT * FROM view_benutzerBuchung;"))
  con.commit()
  con.close()
  return data
