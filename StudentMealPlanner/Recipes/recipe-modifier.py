import json
import re
import unicodedata as ud
import fractions

'''
Ingredient rules shall be:
"Ingredient Name": {
"Quantity": "",
"State": "chopped/whipped"
}


Parsing Rules:
If it starts with a number then continue and check if the term "cup/s" "tbsp" "tsp" "teaspoon/s" "tablespoon/s" "pt" "lb" "pound/s" "inch/es" "serving/s" appears. This should go into quantity
The next section, up to a comma(if one exists), should be the ingredient name.
If there is a comma then the proceeding text is the state
'''

def modify_recipes() -> None:

    terms = ["cup", "pint", "tbsp", "tsp", "teaspoon", "tablespoon", "pt", "lb", "pound", "inch", "serving", 'oz', 'g', 'kg', 'ml', 'ounce', 'pinch']

    data = ''

    with open(".\\database\\db-recipes.json", 'r') as file:
        data = file.read()

    recipes: dict = json.loads(data)

    for recipeId in recipes.keys():
        ingredients: list[str] = recipes[recipeId]['ingredients']
        recipes[recipeId]['raw_ingredients'] = recipes[recipeId]['ingredients']
        recipes[recipeId]['ingredients'] = {}
        ingredient_mod: dict[str, dict[str, str]] = {}
        for ingredient in ingredients:
            ingredient = ingredient.lower()
            if ingredient.startswith("<hr>"):
                continue
            quantity = ""
            state = ""
            ingredient_name = ""
            parsed_ingredient = ingredient.split()
            if re.fullmatch("[0-9]", ingredient[0]) or re.fullmatch("[\u00BC-\u00BE\u2150-\u215E]", ingredient[0]):
                #Has quantity
                if re.fullmatch("[\u00BC-\u00BE\u2150-\u215E]", ingredient[0]):
                    nominator, _, denominator = ud.normalize('NFKD', parsed_ingredient[0]).partition('⁄')
                    quantity = str(fractions.Fraction(*map(int, (nominator, denominator))))
                quantity = parsed_ingredient[0]
                parsed_ingredient[0] = ""
                if re.fullmatch("[\u00BC-\u00BE\u2150-\u215E]", parsed_ingredient[1]) or re.fullmatch("[0-9]/[0-9]", parsed_ingredient[1]):
                    if re.fullmatch("[\u00BC-\u00BE\u2150-\u215E]", parsed_ingredient[1]):
                        nominator, _, denominator = ud.normalize('NFKD', parsed_ingredient[1]).partition('⁄')
                        quantity += " " + str(fractions.Fraction(*map(int, (nominator, denominator))))
                    quantity += " " + parsed_ingredient[1]
                    parsed_ingredient[1] = ""
                    if True in [parsed_ingredient[2] == x or parsed_ingredient[2]+"s" == x for x in terms]:
                        quantity += " " + parsed_ingredient[2].strip()
                        parsed_ingredient[2] = ""
                    continue
                if True in [parsed_ingredient[1] == x or parsed_ingredient[1]+"s" == x for x in terms]:
                    quantity += " " + parsed_ingredient[1].strip()
                    parsed_ingredient[1] = ""
            else:
                a = 1

            for item in parsed_ingredient:
                if item.endswith(','):
                    ingredient_name += " " + item[:-1]
                    break
                ingredient_name += " " + item

            ingredient_name = ingredient_name.strip()
            #ingredient_name = ' '.join([x for x in parsed_ingredient if not x.endswith(",")]).strip()
        
            if "," in ingredient:
                state = ingredient.split(", ")[1].strip()
        
            
            ingredient_mod[ingredient_name] = {'quantity': quantity, 'state': state}
        recipes[recipeId]['ingredients'] = ingredient_mod


    with open(".\\database\\db-recipes-modified.json", 'w') as file:
        file.write(json.dumps(recipes))