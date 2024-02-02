import sqlite3

def setupDatabase():
    connection = sqlite3.connect('ingredient.db')
    cursor = connection.cursor()

    # Creating table
    ingredientTable = """ CREATE TABLE Ingredient (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        category VARCHAR(255),
        quantity INTEGER,
        unit VARCHAR(255),
        BuyPlace TEXT,
        highPrice REAL,
        lowPrice REAL
    ); """

    userIngredientTable = """ CREATE TABLE UserIngredient (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        category VARCHAR(255),
        quantity INTEGER,
        unit VARCHAR(255),
        BuyPlace TEXT,
        price REAL,
        ingredientID INTEGER,
        FOREIGN KEY (ingredientID) REFERENCES Ingredient(ID)
    ); """
 
    cursor.execute(ingredientTable)
    cursor.execute(userIngredientTable)

    print("tables created")

    connection.commit() 
    connection.close()

setupDatabase()