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
    print(anvil.server.call("get_jugendherbergen"))
    self.drop_down_1.items = [(name, JID) for name, JID in anvil.server.call("get_jugendherbergen", "name, JID")]
    if self.drop_down_1.items:
      self.drop_down_1.selected_value = self.drop_down_1.items[0][1] 
      print(self.drop_down_1.items)


  def drop_down_j_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.drop_down_1.selected_value is None:
        print("No selection made")
        return
    
    selected_jid = self.drop_down_1.selected_value
    
    zimmer_data = anvil.server.call('get_zimmer_for_jugendherberge', selected_jid)
  
    print(zimmer_data)
    
    self.data_grid_1.rows = zimmer_data

  def drop_down_usr_change(self, **event_args):
    """This method is called when an item is selected"""
    #ss
    pass

  def drop_down_price_change(self, **event_args):
    """This method is called when an item is selected"""
    #ss
    pass

  def drop_down_z_change(self, **event_args):
    """This method is called when an item is selected"""
    #ss
    pass

  def date_picker_start_change(self, **event_args):
    """This method is called when the selected date changes"""
    #ss
    pass

  def date_picker_end_change(self, **event_args):
    """This method is called when the selected date changes"""
    #ss
    pass

  def drop_down_guest_change(self, **event_args):
    """This method is called when an item is selected"""
    #ss
    pass

  def guest_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    #ss
    pass

  def button_book_click(self, **event_args):
    """This method is called when the button is clicked"""
    #ss
    pass
