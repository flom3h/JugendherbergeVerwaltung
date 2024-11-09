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
def get_benutzer():
    benutzer_list = []
    
    rows = app_tables.tblBenutzer.search()
    
    for row in rows:
        benutzer_list.append({
            "IDBenutzer": row['IDBenutzer'],
            "Vorname": row['Vorname'],
            "Nachname": row['Nachname'],
            "Email": row['Email'],
            "Passwort": row['Passwort'],
            "fkPreiskategorie": row['fkPreiskategorie']
        })
    
    return benutzer_list

@anvil.server.callable
def get_jugendherberge():
    jugendherberge_list = []
    
    rows = app_tables.tblJugendherberge.search()
    
    for row in rows:
        jugendherberge_list.append({
            "IDJugendherberge": row['IDJugendherberge'],
            "Name": row['Name']
        })
    
    return jugendherberge_list

@anvil.server.callable
def get_zimmer():
    zimmer_list = []
    
    rows = app_tables.tblZimmer.search()
    
    for row in rows:
        zimmer_list.append({
            "IDZimmer": row['IDZimmer'],
            "MaxBettenanzahl": row['MaxBettenanzahl'],
            "fkJugendherberge": row['fkJugendherberge'],
            "fkPreiskategorie": row['fkPreiskategorie']
        })
    
    return zimmer_list

@anvil.server.callable
def get_preiskategorie():
    preiskategorie_list = []
    
    rows = app_tables.tblPreiskategorie.search()
    
    for row in rows:
        preiskategorie_list.append({
            "IDPreiskategorie": row['IDPreiskategorie'],
            "Preis": row['Preis']
        })
    
    return preiskategorie_list

@anvil.server.callable
def get_buchung():
    buchung_list = []
    
    rows = app_tables.tblBuchung.search()
    
    for row in rows:
        buchung_list.append({
            "IDBuchung": row['IDBuchung'],
            "Startzeit": row['Startzeit'],
            "Endzeit": row['Endzeit'],
            "fkZimmer": row['fkZimmer']
        })
    
    return buchung_list

@anvil.server.callable
def get_buchung_benutzer():
    buchung_benutzer_list = []
    
    rows = app_tables.tblBuchungBenutzer.search()
    
    for row in rows:
        buchung_benutzer_list.append({
            "IDBB": row['IDBB'],
            "IDBenutzer": row['IDBenutzer'],
            "IDBuchung": row['IDBuchung'],
            "Benutzerrolle": row['Benutzerrolle']
        })
    
    return buchung_benutzer_list

@anvil.server.callable
def test_table_access():
    try:
        users = app_tables.tblbenutzer.search()  # Adjust table name as needed
        return [user for user in users]  # Return a basic list of users to confirm access
    except Exception as e:
        return f"Error: {e}"


@anvil.server.callable
def get_price_categories():
    categories = app_tables.tblPreiskategorie.search()
    return [{"price": category['Preis'], "id": category['IDPreiskategorie']} for category in categories]

@anvil.server.callable
def get_jugendherbergen():
    jugendherbergen = app_tables.tblJugendherberge.search()
    return [{"name": jugend['Name'], "id": jugend['IDJugendherberge']} for jugend in jugendherbergen]

@anvil.server.callable
def get_rooms(jugendherberge_id, preiskategorie_id):
    rooms = app_tables.tblZimmer.search(
        fkJugendherberge=jugendherberge_id,
        fkPreiskategorie=preiskategorie_id
    )
    return [{"room_id": room['IDZimmer'], "max_betten": room['MaxBettenanzahl']} for room in rooms]

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
