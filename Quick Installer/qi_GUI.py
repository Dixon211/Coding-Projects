from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
import subprocess
import os
import sqlite3



def create_DB():
    #create Sql database
    conn = sqlite3.connect('programs_to_install.db')
    db = conn.cursor()

    #create table with 3 columns file_name, binary, and file_type in database
    db.execute('''
            CREATE TABLE IF NOT EXISTS software_values
            ([file_name] TEXT PRIMARY KEY,
            [binary] BLOB)
            ''')
    conn.close()


def move_DBinfo():
    conn = sqlite3.connect('programs_to_install.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM software_values")
    rows = cursor.fetchall()
    for row in rows:
        column1_value = row[0]
        app_names.append(column1_value)
    conn.close()  
    
            
class LeftBox(BoxLayout):
    def __init__(self, app_names, **kwargs):
        super().__init__(**kwargs)
        self.app_names=app_names
        self.app_list = BoxLayout(orientation="vertical")
        self.add_widget(self.app_list)
        self.tiles = []
        for app in self.app_names:
            tile = App_Tiles(app)
            self.tiles.append(tile)
            self.app_list.add_widget(tile)
 
            
            
class App_Tiles(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation="horizontal"
        
        self.app_title = Label(text=self.app)
        self.add_widget(self.app_title)
        
        self.app_checkbox= CheckBox()
        self.add_widget(self.app_checkbox)
        
        
            
        
            
               
class RightBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        add_prgm_but = Button(text="Add Program...")
        add_batch_but = Button(text="Add Batch File...")
        install_but = Button(text = "Install")
        
        add_prgm_but.bind(on_press=self.open_file_explor)
        
        self.add_widget(add_prgm_but)
        self.add_widget(add_batch_but)
        self.add_widget(install_but)
     
    def open_file_explor(self, *args):
        file_explorer = File_Explorer()
        file_explorer.open()


class File_Explorer(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = sqlite3.connect('programs_to_install.db')
        self.cursor = self.conn.cursor()

        self.title="File Explorer"
        file_win = BoxLayout(orientation="vertical")
        options_box =BoxLayout(orientation="horizontal", size_hint_y = None, height = 100)
        self.file_explr=FileChooserListView(path=os.path.expanduser("~"))
        self.file_explr.bind(selection=self.select_file)
        self.selected_file = None
        
        back_btn=Button(text="Back")
        back_btn.bind(on_release=self.go_up_one_directory)
        
        self.open_btn=Button(text="Add to List")
        self.open_btn.disabled = True
        self.open_btn.bind(on_release= lambda instance: self.add_to_DB(self.selected_file))
        
        close_btn=Button(text="Close")
        close_btn.bind(on_release=self.dismiss)

        file_win.add_widget(options_box)
        file_win.add_widget(self.file_explr)
        
        options_box.add_widget(back_btn)
        options_box.add_widget(self.open_btn)
        options_box.add_widget(close_btn)

        self.content=file_win
    
    def __del__(self):
        self.conn.close()

    def go_up_one_directory(self, instance):
        current_path = self.file_explr.path
        if current_path and current_path != '/': # '/' = root directory for UNIX systems
            parent_directory = os.path.dirname(current_path)
            self.file_explr.path = parent_directory

    def select_file(self, instance, selection):
        if selection:
            self.selected_file = selection[0]
            self.open_btn.disabled=False
        else:
            self.selected_file=None
            self.open_btn.disabled=True
    
    def add_to_DB(self, selected_file):
        with open(selected_file, "rb") as file:
            byte_data = file.read()
        file_name = os.path.basename(selected_file)
        
        self.cursor.execute("INSERT OR REPLACE INTO software_values (file_name, binary) VALUES (?, ?)",
                            (file_name, byte_data))
        self.conn.commit()

        self.title = "File added!"


class MyApp(App):
    def build(self):
        self.title="Quick Install"
        main_box = BoxLayout(orientation="horizontal")
        left_half=LeftBox(app_names)
        right_half=RightBox(orientation="vertical")
        main_box.add_widget(left_half)
        main_box.add_widget(right_half)
        return main_box


if __name__ == "__main__":
    app_names = []
    create_DB()
    move_DBinfo()
    MyApp().run()
