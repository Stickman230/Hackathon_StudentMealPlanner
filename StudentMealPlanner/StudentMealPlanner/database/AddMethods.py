import sqlite3
from random import uniform

def addIngredient(name,category,quantity,mesurmentU,BuyPlace):
    connection = sqlite3.connect('ingredient.db')
    cursor = connection.cursor()
    randomHigh = uniform(4,7)
    randomLow = uniform(1,4)
    result = cursor.execute('''INSERT INTO Ingredient (name, category, quantity, mesurmentUnit, BuyPlace, highPrice, lowPrice)
                    VALUES ('''+name+','+category+','+quantity+','+mesurmentU+','+BuyPlace+','+randomHigh+','+randomLow+')'+ ";")
    connection.commit()
    cursor.close()
    connection.close()

def userAddIngredient(name, category, quantity, measurementU, buyPlace, price):
    connection = sqlite3.connect('ingredient.db')
    cursor = connection.cursor()

    # Use parameterized query
    check = cursor.execute('SELECT COUNT(*) FROM UserIngredient WHERE name = ?;', (name,)).fetchone()
    if check[0] >= 9:  
        length_of_entries = check[0]
        check2 = cursor.execute('SELECT COUNT(*) FROM Ingredient WHERE name = ?;', (name,)).fetchone()
        if check2[0] >= 1:
            return
        else:
            # Fetch all prices and calculate the total
            priceVal = cursor.execute('SELECT price FROM UserIngredient WHERE name = ?;', (name,)).fetchall()
            totalprice = sum(row[0] for row in priceVal) / length_of_entries
            result0 = cursor.execute('''
                INSERT INTO Ingredient (name, category, quantity, measurementUnit, BuyPlace, highPrice, lowPrice)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            ''', (name, category, quantity, measurementU, buyPlace, totalprice, totalprice))
    else:
        result1 = cursor.execute('''
            INSERT INTO UserIngredient (name, category, quantity, measurementUnit, BuyPlace, price)
            VALUES (?, ?, ?, ?, ?, ?);
        ''', (name, category, quantity, measurementU, buyPlace, price))

    connection.commit()
    cursor.close()
    connection.close()

    
    