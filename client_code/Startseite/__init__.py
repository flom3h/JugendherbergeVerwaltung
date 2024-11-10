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

    # Populate dropdowns with data from the server
    self.drop_down_usr.items = anvil.server.call('get_user')
    self.drop_down_j.items = anvil.server.call('get_hostel')
    self.drop_down_price.items = anvil.server.call('get_price')

    # Initialize guest list as empty
    self.guest_list = []

  def drop_down_j_change(self, **event_args):
    """This method is called when a hostel is selected"""
    selected_jid = self.drop_down_j.selected_value
    selected_pid = self.drop_down_price.selected_value

    if selected_jid and selected_pid:
        # Fetch available rooms based on selected hostel and price category
        zimmer_data = anvil.server.call('get_room', selected_jid, selected_pid)
        self.data_grid_1.rows = zimmer_data
    else:
        self.data_grid_1.rows = []

  def drop_down_price_change(self, **event_args):
    """This method is called when a price category is selected"""
    # Re-run the room fetching process if both hostel and price are selected
    self.drop_down_j_change()

  def guest_button_click(self, **event_args):
    """This method is called when the 'Add Guest' button is clicked"""
    selected_user = self.drop_down_usr.selected_value
    if selected_user and selected_user not in self.guest_list:
        self.guest_list.append(selected_user)
        self.repeating_panel_guests.items = [{"user_id": user_id} for user_id in self.guest_list]
    else:
        alert("User already added or not selected.")

  def button_book_click(self, **event_args):
    """This method is called when the 'Book' button is clicked"""
    selected_room = self.data_grid_1.selected_row  # Ensure the row is selected in data grid
    start_date = self.date_picker_start.date
    end_date = self.date_picker_end.date

    if selected_room and start_date and end_date:
        ZID = selected_room["ZID"]
        # Call the server function to book the room
        result = anvil.server.call("booking", self.guest_list, start_date, end_date, ZID)
        
        # Handle the booking result
        if result:
            alert("Room successfully booked!")
            # Reset guest list and clear UI after booking
            self.guest_list.clear()
            self.repeating_panel_guests.items = []
            self.data_grid_1.rows = []  # Clear room grid to refresh selection
        else:
            alert("An error occurred while booking.")
    else:
        alert("Please select a room and specify start and end dates.")

  def date_picker_start_change(self, **event_args):
    """This method is called when the start date changes"""
    # Optionally add date validation logic here
    pass

  def date_picker_end_change(self, **event_args):
    """This method is called when the end date changes"""
    # Optionally add date validation logic here
    pass
