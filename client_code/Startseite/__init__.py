from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

class Startseite(StartseiteTemplate):
    def __init__(self, **properties):
        self.location_index = []  
        self.user_index = []
        self.category_index = []
        self.selection_index = []
        self.guest_ids = []
        self.init_components(**properties)
        self.load_initial_data()

        # Placeholder for booking feedback
        self.booking_feedback = Label(text="")
        self.add_component(self.booking_feedback)

    def prepare_data_list(self, items):
        """Prepare lists for dropdowns and index mapping from server data."""
        dropdown_list = []
        index_mapping = []
        count = 0
        for item in items:
            dropdown_list.append([item[0], count])  # item[0]: name, count: index in dropdown
            index_mapping.append([count, item[1]])  # item[1]: ID, count: index in dropdown
            count += 1
        return [dropdown_list, index_mapping]

    def map_index_to_id(self, index_map, selected_index):
        """Convert selected dropdown index to the corresponding ID."""
        for index, ID in index_map:
            if selected_index == index:
                return ID
        return None

    def load_initial_data(self):
        self.load_location_data()
        self.load_user_data(self.dropdown_usr)
        self.load_user_data(self.dropdown_guest)
        self.load_category_data()
        self.load_selection_data()
        self.display_current_bookings()

    def load_location_data(self):
        location_data = anvil.server.call('get_location')
        prepared_data = self.prepare_data_list(location_data)
        self.location_index = prepared_data[1]
        self.dropdown_j.items = prepared_data[0]

    def load_user_data(self, dropdown):
        user_data = anvil.server.call('get_user')
        prepared_data = self.prepare_data_list(user_data)
        self.user_index = prepared_data[1]
        dropdown.items = prepared_data[0]

    def load_category_data(self):
        category_data = anvil.server.call('get_category')
        prepared_data = self.prepare_data_list(category_data)
        self.category_index = prepared_data[1]
        self.dropdown_price.items = prepared_data[0]

    def load_selection_data(self):
        selected_location_id = self.map_index_to_id(self.location_index, self.dropdown_j.selected_value)
        selected_category_id = self.map_index_to_id(self.category_index, self.dropdown_price.selected_value)
        selection_data = anvil.server.call('get_selection', selected_location_id, selected_category_id)
        prepared_data = self.prepare_data_list(selection_data)
        self.selection_index = prepared_data[1]
        self.dropdown_z.items = prepared_data[0]

    def update_selection_on_location_change(self, **event_args):
        self.load_selection_data()

    def update_selection_on_category_change(self, **event_args):
        self.load_selection_data()

    def add_guest_user(self, **event_args):
        selected_value = self.dropdown_guest.selected_value
        for name_text, index in self.dropdown_guest.items:
            if index == selected_value:
                guest_link = Link(text=str(name_text))
                guest_link.icon = "fa:times"
                guest_link.icon_align = "left"
                guest_link.background = "#eee"
                guest_link.role = "lozenge"
                guest_link.border = "1px solid #888"

                guest_link.set_event_handler("click", lambda **k: self.remove_guest(k, selected_value))

                if name_text not in [component.text for component in self.user_to_add.get_components()]:
                    self.guest_ids.append(selected_value)
                    self.user_to_add.add_component(guest_link)
                else:
                    print(f"{name_text} is already added.")
                break

    def handle_booking(self):
        primary_user_id = self.map_index_to_id(self.user_index, self.dropdown_usr.selected_value)
        user_ids = self.collect_user_ids(primary_user_id)
        
        if self.validate_dates(self.datepicker_start.date, self.datepicker_end.date, "%Y-%m-%d"):
            start_date_str = str(self.datepicker_start.date)
            end_date_str = str(self.datepicker_end.date)
            selected_selection_id = self.map_index_to_id(self.selection_index, self.dropdown_z.selected_value)
            anvil.server.call('booking', user_ids, start_date_str, end_date_str, selected_selection_id)
            self.booking_feedback.text = "Buchung ist erfolgreich."
            self.display_current_bookings()
        else:
            self.booking_feedback.text = "Datum ist nicht möglich."

    def validate_dates(self, start_date, end_date, date_format):
        """Ensure start date is before end date."""
        start_dt = datetime.strptime(str(start_date), date_format)
        end_dt = datetime.strptime(str(end_date), date_format)
        return start_dt < end_dt

    def collect_user_ids(self, primary_user_id):
        all_user_ids = [self.map_index_to_id(self.user_index, i) for i in self.guest_ids]
        if primary_user_id not in all_user_ids:
            all_user_ids.append(primary_user_id)
        return all_user_ids

    def display_current_bookings(self):
        booking_data = anvil.server.call('get_data')
        self.repeating_panel_1.items = [{'column_1': record[0], 'column_2': record[1], 'column_3': record[2], 
                                         'column_4': record[3], 'column_5': record[4], 'column_6': record[5]} 
                                         for record in booking_data]

    def confirm_booking(self, **event_args):
        self.handle_booking()
