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
