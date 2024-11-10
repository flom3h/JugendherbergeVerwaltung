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
def get_user(rows="*"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {rows} FROM tblBenutzer"))
  print(res)
  return res

@anvil.server.callable
def get_jugendherbergen(rows="*"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {rows} FROM jugendherbergen"))
  print(res)
  return res

@anvil.server.callable
def get_zimmer(rows="*"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {rows} FROM zimmer"))
  print(res)
  return res

@anvil.server.callable
def get_preiskategorie(rows="*"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {rows} FROM preiskategorie"))
  print(res)
  return res

@anvil.server.callable
def get_buchung():
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {rows} FROM jugendherbergen"))
  print(res)
  return res

@anvil.server.callable
def get_buchung_benutzer():
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {rows} FROM jugendherbergen"))
  print(res)
  return res


@anvil.server.callable
def get_available_dates(room_id, start_date, end_date):
    bookings = app_tables.tblBuchung.search(fkZimmer=room_id)
    for booking in bookings:
        if (start_date <= booking['Endzeit'] and end_date >= booking['Startzeit']):
            return False  # Room is not available
    return True  # Room is available

@anvil.server.callable
def confirm_booking(user_id, room_id, start_date, end_date, mitbucher_ids):
    # First, check if room is available
    if not get_available_dates(room_id, start_date, end_date):
        return "Room is not available for the selected dates."

    # Add booking to tblBuchung
    booking = app_tables.tblBuchung.add_row(
        Startzeit=start_date,
        Endzeit=end_date,
        fkZimmer=room_id
    )

    # Link the main user to the booking
    app_tables.tblBuchungBenutzer.add_row(
        IDBenutzer=user_id,
        IDBuchung=booking['IDBuchung'],
        Benutzerrolle="Main"
    )

    # Link additional mitbucher
    for mitbucher_id in mitbucher_ids:
        app_tables.tblBuchungBenutzer.add_row(
            IDBenutzer=mitbucher_id,
            IDBuchung=booking['IDBuchung'],
            Benutzerrolle="Mitbucher"
        )

    return "Booking confirmed!"
