import sqlite3


def getIngredient(ingredient_name: str) -> dict[str, object]:
    connection = sqlite3.connect('ingredient.db')
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM Ingredient WHERE name = " + ingredient_name + ";").fetchall()
    cursor.close()
    connection.close()
    return result

def getUserIngredient(ingredient_name: str) -> dict[str, object]:
    connection = sqlite3.connect('ingredient.db')
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM UserIngredient WHERE name = " + ingredient_name + ";").fetchall()
    cursor.close()
    connection.close()
    return result
    

def getIngredientAmount(ingredient_name: str) -> str:
    connection = sqlite3.connect('ingredient.db')
    cursor = connection.cursor()
    result = cursor.execute("SELECT quantity FROM Ingredient WHERE name = " + ingredient_name + ";").fetchall()
    cursor.close()
    connection.close()
    return result
    
def getIngredientAmountAndUnit(ingredient_name: str) -> str:
    connection = sqlite3.connect('ingredient.db')
    cursor = connection.cursor()
    result = cursor.execute("SELECT quantity, unit FROM Ingredient WHERE name = " + ingredient_name + ";").fetchone()
    cursor.close()
    connection.close()
    return result

def get_ingredient_amount(ingredient_name: str) -> str:
    connection = sqlite3.connect('ingredient.db')
    cursor = connection.cursor()
    result = cursor.execute("SELECT quantity, unit FROM Ingredient WHERE name = " + ingredient_name + ";").fetchone()
    result = str(result[0]) + " " + result[1]
    cursor.close()
    connection.close()
    return result
    