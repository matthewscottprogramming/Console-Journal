import datetime
from collections import OrderedDict
import sys
import os

from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
  content = TextField()
  timestamp = DateTimeField(default=datetime.datetime.now)
  
  class Meta:
    database = db

def clear():
  os.system('cls' if os.name=='nt' else 'clear')
    
def initialize():
  '''Create the database and the table if they don't exist'''
  db.connect()
  db.create_tables([Entry], safe=True)

  
def menu_loop(menu):
  '''This displays a command line menu based interface to the user'''
  choice = None
  while choice != 'q':
    clear()
    print('Enter (q) to quit')
    for key, value in menu.items():
      print('{}) {}'.format(key, value.__doc__))
    choice = input('Action: ').lower().strip()
    if choice == 'q':
      break
    if choice in menu:
      clear()
      menu[choice]()
    else: print("Invalid - Enter:", ",".join((menu).keys()))
  
def add_entry():
  '''adds an entry to the entry table in the database'''
  print("Enter your entry press control+d when finished")
  data = sys.stdin.read().strip()
  if data:
    print()
    if input('Save entry? [Y/N]').lower().strip() != 'n':
      Entry.create(content=data)
      print("Saved successfully")      

def view_entries(search_query = None):
  
  '''Gets an entry from the database'''
  entries = Entry.select().order_by(Entry.timestamp.desc())
  
  if search_query:
    entries = entries.where(Entry.content.contains(search_query))
    
  for entry in entries:
    clear()
    timestamp = entry.timestamp.strftime('%A %B %d %Y %I:%M%p')
    print(timestamp)
    print("="*len(timestamp))
    print(entry.content)
    print("\n"*2+"="*len(timestamp))
    print('n) Next entry')
    print('d) Delete entry')
    print('q) Return to main menu')
    next_action = input('Action: [Ndq] ').lower().strip()
    if next_action == 'q':
      break
    elif next_action == 'd':
      delete_entry(entry)
    
                        
                        

def delete_entry(entry):
  '''Deletes an entry from the database'''
  if input("Are you sure? [Yn]: ").lower().strip() == "y":
    entry.delete_instance()
    print("Entry deleted")

def search_entries():
  '''This will find all entries with a given string of characters inside'''
  view_entries(input('Search Query: '))
  
  

menu = OrderedDict([
   ('a', add_entry),
   ('v', view_entries),
    ('s', search_entries),
  ])


if __name__ == "__main__":
  initialize()
  menu_loop(menu)
