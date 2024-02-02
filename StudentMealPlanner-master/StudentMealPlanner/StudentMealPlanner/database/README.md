

## not sql injection secure ##

two tables make our database :

TABLE Ingredient (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    category VARCHAR(255),
    quantity INTEGER,
    mesurmentUnit VARCHAR(255),
    BuyPlace TEXT,
    highPrice REAL,
    lowPrice REAL

and :

TABLE UserIngredient (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    quantity INTEGER,
    BuyPlace TEXT,
    price REAL,
    ingredientID INTEGER,
    FOREIGN KEY (ingredientID) REFERENCES Ingredient(ID)

------------------------------------------------------------------------------------
we run the database creation in the database.py, then populate with db_add_content.py

the sqlite_db file contains all the info needed for the database

the ID INTEGER, name VARCHAR(255), category VARCHAR(255) and quantity INTEGER are the basic knowlege needed. The mesurmentUnit VARCHAR(255), BuyPlace TEXT, highPrice REAL and lowPrice REAL give more info about the ingredient. the mesurementUnit is a VARCHAR.

run database before launch if no .db file in the folder


