import json
import fractions
import itertools
from math import floor
import os
from StudentMealPlanner.database.GetMethods import getIngredientAmountAndUnit

def open_recipe_json_file(file_name:str)->dict:
    '''
    Opens a json file by a specific file name and returns the data as a dictionary.

    args:
        file_name (str): The name of the file to open.
    returns:
        data (dict): The data from the json file.
    raises:
        FileNotFoundError: If the file does not exist.
    '''

    with open(f'./recipes/{file_name}') as f:
        data = json.load(f)
    return data
    
def titles_similar_to(search_term:str, recipes:dict)->list:
    '''
    Returns a list of recipe titles that are similar to the search term.

    args:
        search_term (str): The search term to compare to the recipe titles.
        recipes (dict): The dictionary of recipes.
    returns:
        similar_titles (list(lists)): A list of recipe titles and their index in the recipes array that are similar to the search term.
    '''
    similar_titles = []
    for i,recipe in enumerate(recipes.values()):
        # print(recipe)
        if search_term.lower() in recipe['name'].lower():
            similar_titles.append({'title':recipe['name'],'index':list(recipes.keys())[i]}) #index here is the key of the key value pair in the dictionary
            # similar_titles.append({'title':recipe['name'],'index':i})
    return similar_titles


def convert_to_g(ingredient_and_measurement: tuple[float, str]) -> float:
    '''
    Convert ingredient measurement to grams
    We assume density of water for volume measurements
    '''
    quantity = ingredient_and_measurement[0]
    measurement = ingredient_and_measurement[1]
    equivalent_terms = [["pint", "pt", "pints"], ["pound", "lb", "pounds"], ["oz", "ounce", "ounces"], ["g", "grams", "gs"], ["kg", "kilograms", "kgs"]]
    terms_to_methods = {"cup": lambda x: x * 236.6, "pint": lambda x: x*568.3, "pound": lambda x: x*453.6, "g": lambda x: x, "kg": lambda x: x*1000, 'oz': lambda x: x*28.35}
    for terms in equivalent_terms:
        if measurement.lower() in terms:
            measurement = terms[0]
    return terms_to_methods[measurement](quantity)
    

def get_ingredient_quantity_and_measurement(quantity: str) -> tuple[float, str]:
    vals = quantity.split(' ')
    if "/" in vals[0]:
        vals[0] = float(fractions.Fraction(int(vals[0][0]), int(vals[0][2])))
    else:
        vals[0] = float(vals[0])
    return tuple(vals)

def calculate_waste(recipes: list[dict]) -> float:
    '''
    find each unique ingredient in the recipes and add amount used of each
    subtract from amount that is generally purchased
    add these together to get total waste
    '''
    unused_measurements = ["tbsp", "tsp", "teaspoon", "tablespoon", "inch", "serving"]
    ingredients_and_amounts = {}
    for recipe in recipes:
        for ingredient in recipe['ingredients']:
            if recipe['ingredients'][ingredient]['quantity'] == "" or recipe['ingredients'][ingredient]['quantity'].startswith("<"):
                continue
            quantity_and_measurement = get_ingredient_quantity_and_measurement(recipe['ingredients'][ingredient]['quantity'])
            if len(quantity_and_measurement) == 1 or True in [quantity_and_measurement[1].lower().startswith(x) for x in unused_measurements]:
                continue
            try:
                if ingredient in ingredients_and_amounts.keys():
                    ingredients_and_amounts[ingredient] += convert_to_g(quantity_and_measurement)
                else:
                    ingredients_and_amounts[ingredient] = convert_to_g(quantity_and_measurement)
            except:
                continue
    
    total_waste_percentage = 0
    for ingredient in ingredients_and_amounts.keys():
        try:
            val = convert_to_g(tuple(getIngredientAmountAndUnit(ingredient)))
        except:
            val = 500
        #ingredient_amount = convert_to_g(get_ingredient_quantity_and_measurement(val))
        ingredient_amount = val
        ingredient_used = ingredients_and_amounts[ingredient]
        while ingredient_amount < ingredient_used:
            ingredient_used -= ingredient_amount
        total_waste_percentage += ingredient_used/ingredient_amount
    total_waste_percentage /= len(ingredients_and_amounts.keys())
    return total_waste_percentage

def MaximiseBy(selectedRecipes: list[dict], maximise_value: str, number_of_recipes: int) -> tuple[list[dict], float, float]:
    '''
    Given a maximise_value (such as protein) find a combination of numbers, without repeats, that maximises the given value. 
    Each possible combination should fall within the maximum quantity of each key ingredient
    The return value should be a dict that represents all the recipes that are selected
    '''
    if len(selectedRecipes) < number_of_recipes:
        return selectedRecipes
    best_comb = []
    curr_val = 0
    curr_waste_percentage = 1
    ids = [x['id'] for x in selectedRecipes]
    for recipe_comb in itertools.combinations(ids, number_of_recipes):
        #Check combination waste and minimise
        #check if value is maximised
        set_value = 0
        chosen_recipes = [x for x in selectedRecipes if x['id'] in recipe_comb]
        for recipe in chosen_recipes:
            set_value += recipe[maximise_value]
        waste_percentage = calculate_waste(chosen_recipes)
        if set_value > curr_val and waste_percentage < curr_waste_percentage:
            best_comb = chosen_recipes.copy()
            curr_val = set_value
            curr_waste_percentage = waste_percentage

    return best_comb, curr_val, curr_waste_percentage
            

def is_sub(sub: list, lst: list) -> bool:
    ln = len(sub)
    for i in range(len(lst) - ln + 1):
        if all(sub[j] == lst[i+j] for j in range(ln)):
            return True
    return False

def findRecipe(id_of_chosen_recipe: str) -> list[dict]:
    
    # Read recipe information from a JSON file
    with open("./StudentMealPlanner/database/db-recipes-modified.json", 'r') as json_file:
        recipes = json.load(json_file)
    ingredient_names = list((recipes[id_of_chosen_recipe]['ingredients']).keys())
    tags = recipes[id_of_chosen_recipe]['tags']
    return best_matches_from_ingredients(ingredient_names=ingredient_names, recipes=recipes, tags=tags)

    

def best_matches_from_ingredients(ingredient_names: list[str], recipes: dict, tags: list[str] = ["main"]) -> list[dict]:
    list_of_recipes = []
    all_ingredients = []
    list_of_recipeIDs = []
    generalised_ingredients = [['salt'], ['black', 'pepper'], ['eggs'], ['egg'], ['vegetable', 'broth'], ['garlic'], ['water'], ['olive', 'oil'], ['thyme'], ['lettuce'], ['butter'], ['rosemary'], ['parsley'], ['chives'], ['onions'], ['mustard']]
    # Assume half of the ingredients match for now
    matching_threshold = 0.4

    
    for i in range(len(ingredient_names)):
        split_ingredient_name = ingredient_names[i].split()
        for generalised_ingredient in generalised_ingredients:
            if is_sub(generalised_ingredient, split_ingredient_name):
                ingredient_names[i] = ' '.join(generalised_ingredient)
                break
    all_ingredients = ingredient_names.copy()
    if 'main' in tags or 'side' in tags:
        user_dish_is_dessert = False
    else:
        user_dish_is_dessert = True

    # Iterate through recipes and find a match based on ingredients
    for recipe_id, recipe in recipes.items():
        recipe_ingredients = list(recipe.get('ingredients', {}).keys())
        recipe_tags = recipe.get('tags', [])
        for i in range(len(recipe_ingredients)):
            split_ingredient_name = recipe_ingredients[i].split()
            for generalised_ingredient in generalised_ingredients:
                if is_sub(generalised_ingredient, split_ingredient_name):
                    recipe_ingredients[i] = ' '.join(generalised_ingredient)
                    break

        # Calculate the percentage of matching ingredients
        matched_count = sum(ingredient_name in recipe_ingredients for ingredient_name in ingredient_names)
        matching_percentage = matched_count / len(ingredient_names)

        # Check if the matching percentage exceeds the threshold and if the user_dish_type_choice is in the tags 
        if matching_percentage >= matching_threshold and ((user_dish_is_dessert and 'dessert' in recipe_tags) or (not user_dish_is_dessert and 'side' in recipe_tags) or (not user_dish_is_dessert and 'main' in recipe_tags)):
            #Add dish to list of recipes
            #list_of_recipes.append(recipe_id + " " + recipe_tags)
            all_ingredients.extend(recipe_ingredients.copy())
            list_of_recipes.append(recipe)
            list_of_recipeIDs.append(recipe_id)

    # list_of_recipeIDs.remove(id_of_chosen_recipe)
    all_ingredients = list(set(all_ingredients))
    return list_of_recipes
    

#print(MaximiseBy(findRecipe('2'), 'carbs', 3))

# if __name__ == '__main__':
#     data =open_recipe_json_file('db-recipes-modified.json')
#     title_data = titles_similar_to('er', data)
#     print(len(title_data))
#     print(title_data[0])
#     # print('')