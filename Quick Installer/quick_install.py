import sys
import sqlite3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

#create Sql database
p_list = sqlite3.connect('programs_to_install')
db = p_list.cursor()

#create table with 3 columns file_name, binary, and file_type
db.execute('''
           CREATE TABLE IF NOT EXISTS software_values
           ([file_name] TEXT PRIMARY KEY,
           [binary] BLOB,
           [file_type] TEXT)
           ''')

#use this to add to the created database
db.execute('''
           INSERT INTO software_values (file_name, binary, file_type)
           
           ''')
