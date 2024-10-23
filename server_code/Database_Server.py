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
def say_hello(name):
  print("Hello, " + name + "!")
  return 42

@anvil.server.callable
def get_jugendherbergen(rows="*"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {rows} FROM jugendherbergen"))
  print(res)
  return res

@anvil.server.callable
def get_zimmer_for_jugendherberge(jid, columns="ZID, zimmernummer, bettenanzahl, preis_pro_nacht, gebucht"):
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    query = f"SELECT {columns} FROM zimmer WHERE JID=?"
    cursor.execute(query, (jid,))
    rows = cursor.fetchall()
    zimmer_list = [
        {
            "ZID": row[0],
            "zimmernummer": row[1],
            "bettenanzahl": row[2],
            "preis_pro_nacht": row[3],
            "gebucht": row[4]
        }
        for row in rows
    ]
    
    print(zimmer_list)
    return zimmer_list

