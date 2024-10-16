from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # [("Feldkirch", 0), ("Mordor", 1)]
    # Any code you write here will run before the form opens.
    print(anvil.server.call("say_hello", "sauron"))
    print(anvil.server.call("get_jugendherbergen"))
    self.drop_down_1.items=anvil.server.call("get_jugendherbergen", "name, JID")

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    jid = self.drop_down_1.items[self.drop_down_1.selected_value -1][1]
    print(jid)
    anvil.server.call('get_zimmer_for_jugendherberge', jid)