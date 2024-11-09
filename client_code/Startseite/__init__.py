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
    self.drop_down_usr.items = [(name, UID) for name, UID in anvil.server.call("get_users")]
    self.drop_down_price.items = anvil.server.call("get_price_categories")
    self.drop_down_z.items = [(type_name, room_type_id) for type_name, room_type_id in anvil.server.call("get_room_types")]
    self.drop_down_guest.items = [(str(count), guest_count_id) for count, guest_count_id in anvil.server.call("get_guest_counts")]



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
    """This method is called when the book button is clicked"""
    selected_room = self.data_grid_1.selected_row  # Ensure the row is selected in data grid
    if selected_room and not selected_room['gebucht']:
        result = anvil.server.call("book_room", selected_room["ZID"])
        if result["status"] == "success":
            selected_room["gebucht"] = 1  # Update UI without re-fetching data
            self.data_grid_1.refresh_data_bindings()  # Refresh the grid to show change
            alert("Room successfully booked!")
        else:
            alert("Error occurred while booking.")
    else:
        alert("Please select an available room to book.")

