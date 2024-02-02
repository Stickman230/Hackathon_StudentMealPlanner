import sqlite3
import json
import re
from random import uniform

encountered_names = []
conversions = {"cup": lambda x: x / 236.6, "pint": lambda x: x/568.3, "pound": lambda x: x/453.6, "g": lambda x: x, "kg": lambda x: x/1000, 'oz': lambda x: x/28.35}

def seedDatabase(name: str,category: str,quantity: str,buyPlace: str):
    connection = sqlite3.connect('ingredient.db')
    cursor = connection.cursor()
    
    randomHigh = round(uniform(4,7),2)
    randomLow = round(uniform(1,4),2)
    
    # define unit as last data after space in quantity
    quantity_pattern = re.compile(r'(\S+) (\D+)')
    match = quantity_pattern.search(quantity)
    
    # Inserting values without specifying the ID (it will auto-increment)
    if match:
        unit = match.group(2)
        quantity = quantity.replace(unit, '').strip()
        if unit in ['oz', 'pint', 'pound', 'g', 'kg']:
            quantity = int(conversions[unit](500))
        cursor.execute('''
                    INSERT INTO Ingredient (name, category, quantity, unit, BuyPlace, highPrice, lowPrice)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                ''', (name, category, quantity, unit, buyPlace, randomHigh, randomLow))
    else:
        cursor.execute('''
                    INSERT INTO Ingredient (name, category, quantity, unit, BuyPlace, highPrice, lowPrice)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                ''', (name, category, quantity, 'None', buyPlace, randomHigh, randomLow))


    encountered_names.append(name)
    connection.commit() 
    connection.close()
    
def testDatabase():
    connection = sqlite3.connect('ingredient.db')
    cursor = connection.cursor()
    
    data=cursor.execute('''SELECT * FROM Ingredient''').fetchall()
    print(data)
    
    connection.commit() 
    connection.close()
    
json_file_path = "db-recipes-modified.json"
name = ''
category = ''
with open(json_file_path, "r",encoding="utf-8") as json_file:
    data = json.load(json_file)
    last_words = []
    for recipe in data.keys():
        names = data[recipe]['ingredients']
        for name in names:
            if name in encountered_names:
                break
            # define category as 
            # last word of full name (exept if too long (probaly link) or if it finishes by ) (probably info)
            words = name.split()
            if words:
                if len(words[-1]) <= 16 and words[-1][-1] != ')':
                    category = words[-1]
                else:
                    category = 'None'
            quantity = data[recipe]['ingredients'][name]['quantity']
            seedDatabase(name,category,quantity,'Tesco')

testDatabase()


    