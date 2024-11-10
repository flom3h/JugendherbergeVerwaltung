from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

class Startseite(StartseiteTemplate):
    def __init__(self, **properties):
        self.j_index = []
        self.user_index = []
        self.price_index = []
        self.z_index = []
        self.guest_index = []
        self.init_components(**properties)
        self.loading_data()
        self.booking_comback = Label(text="")
        self.add_component(self.booking_comback)

    # Loading Data
    def data_modify(self, data):
        data_list = []
        relation = []
        count = 0
        for i in data:
            data_list.append([i[0], count])
            relation.append([count, i[1]])
            count += 1
        return [data_list, relation]

    def transform_index_to_id(self, relation, selected_index):
        for index, ID in relation:
            if selected_index == index:
                return ID
        return None

    def loading_data(self):
        self.load_j()
        self.load_usr(self.dropdown_usr)
        self.load_usr(self.dropdown_guest)
        self.load_price()
        self.load_z()
        self.display_booking()

    def load_j(self):
        data_list = anvil.server.call('get_j')
        data_modify = self.data_modify(data_list)
        self.j_index = data_modify[1]
        self.dropdown_j.items = data_modify[0]

    def load_usr(self, dropdown):
        data_list = anvil.server.call('get_user')
        data_modify = self.data_modify(data_list)
        self.user_index = data_modify[1]
        dropdown.items = data_modify[0]

    def load_price(self):
        data_list = anvil.server.call('get_price')
        data_modify = self.data_modify(data_list)
        self.price_index = data_modify[1]
        self.dropdown_price.items = data_modify[0]

    def load_z(self):
        j_selected = self.transform_index_to_id(self.j_index, self.dropdown_j.selected_value)
        price_selected = self.transform_index_to_id(self.price_index, self.dropdown_price.selected_value)
        data_list = anvil.server.call('get_z', j_selected, price_selected)
        data_modify = self.data_modify(data_list)
        self.z_index = data_modify[1]
        self.dropdown_z.items = data_modify[0]

    def dropdown_j_change(self, **event_args):
        self.load_z()

    def dropdown_price_change(self, **event_args):
        self.load_z()

    def add_user_click(self, **event_args):
        value = self.dropdown_guest.selected_value
        for text, i in self.dropdown_guest.items:
            if i == value:
                name = Link(text=str(text))
                name.icon = "fa:times"
                name.icon_align = "left"
                name.background = "#eee"
                name.role = "lozenge"
                name.border = "1px solid #888"
                name.set_event_handler("click", lambda **k: self.del_btn(k, value))
                if text not in [component.text for component in self.user_to_add.get_components()]:
                    self.guest_index.append(value)
                    self.user_to_add.add_component(name)
                else:
                    print(f"{text} is already added.")
                break

    def get_booking_data(self):
        main_BeID = self.transform_index_to_id(self.user_index, self.dropdown_usr.selected_value)
        users = self.get_extra_user_id(main_BeID)
        if self.check_date(self.datepicker_start.date, self.datepicker_end.date, "%Y-%m-%d"):
            start_date = str(self.datepicker_start.date)
            end_date = str(self.datepicker_end.date)
            zid = self.transform_index_to_id(self.z_index, self.dropdown_z.selected_value)
            anvil.server.call('booking', users, start_date, end_date, zid)
            self.booking_comback.text = "Buchung ist erfolgreich."
            self.display_booking()
        else:
            self.booking_comback.text = "Datum ist nicht möglich."

    def check_date(self, start_date, end_date, date_format):
        d1 = datetime.strptime(str(start_date), date_format)
        d2 = datetime.strptime(str(end_date), date_format)
        return d1 < d2

    def get_extra_user_id(self, main_ID):
        users_id = [self.transform_index_to_id(self.user_index, i) for i in self.guest_index]
        if main_ID not in users_id:
            users_id.append(main_ID)
        return users_id

    def display_booking(self):
        data = anvil.server.call('get_data')
        self.repeating_panel_1.items = [{'column_1': i[0], 'column_2': i[1], 'column_3': i[2], 
                                         'column_4': i[3], 'column_5': i[4], 'column_6': i[5]} for i in data]

    def button_book_click(self, **event_args):
        self.get_booking_data()
