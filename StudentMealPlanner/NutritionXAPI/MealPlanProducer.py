#selectedRecipes is assumed to follow the format [{'ID': 1, ____, ingredients: {str: {quantity: str, state: str}}}]
import itertools
from StudentMealPlanner.database.GetMethods import get_ingredient_amount
from math import floor


def convert_to_g(ingredient_and_measurement: tuple[float, str]) -> float:
    '''
    Convert ingredient measurement to grams
    We assume density of water for volume measurements
    '''
    quantity = ingredient_and_measurement[0]
    measurement = ingredient_and_measurement[1]
    equivalent_terms = [["pint", "pt", "pints"], ["pound", "lb", "pounds"], ["oz", "ounce", "ounces"], ["g", "grams", "gs"], ["kg", "kilograms", "kgs"]]
    terms_to_methods = {"cup": lambda x: x * 236.6, "pint": lambda x: x*568.3, "pound": lambda x: x*453.6, "g": lambda x: x, "kg": lambda x: x*1000}
    for terms in equivalent_terms:
        if measurement.lower() in terms:
            measurement = terms[0]
    return terms_to_methods[measurement](quantity)
    

def get_ingredient_quantity_and_measurement(quantity: str) -> tuple[float, str]:
    vals = quantity.split(' ')
    vals[0] = float(vals[0])
    return tuple(vals)

def calculate_waste(recipes: list[dict]) -> float:
    '''
    find each unique ingredient in the recipes and add amount used of each
    subtract from amount that is generally purchased
    add these together to get total waste
    '''
    unused_measurements = ["tbps", "tsp", "teaspoon", "tablespoon", "inch", "serving"]
    ingredients_and_amounts = {}
    for recipe in recipes:
        for ingredient in recipe['ingredients']:
            quantity_and_measurement = get_ingredient_quantity_and_measurement(recipe['ingredients'][ingredient])
            if True in [quantity_and_measurement[1].lower().startswith(x) for x in unused_measurements]:
                continue
            if ingredient in ingredients_and_amounts.keys():
                ingredients_and_amounts[ingredient] += convert_to_g(quantity_and_measurement)
    
    total_waste_percentage = 0
    for ingredient in ingredients_and_amounts.keys():
        try:
            val = get_ingredient_amount(ingredient)
        except:
            val = "500 g"
        ingredient_amount = convert_to_g(get_ingredient_quantity_and_measurement(val))
        ingredient_used = ingredients_and_amounts[ingredient]
        while ingredient_amount < ingredient_used:
            ingredient_used -= ingredient_amount
        total_waste_percentage += ingredient_used/ingredient_amount
    total_waste_percentage /= len(ingredients_and_amounts.keys())
    return total_waste_percentage

def MaximiseBy(selectedRecipes: list[dict], maximise_value: str, number_of_recipes: int) -> list[dict]:
    '''
    Given a maximise_value (such as protein) find a combination of numbers, without repeats, that maximises the given value. 
    Each possible combination should fall within the maximum quantity of each key ingredient
    The return value should be a dict that represents all the recipes that are selected
    '''
    if len(selectedRecipes) < number_of_recipes:
        return selectedRecipes
    best_comb = []
    curr_val = 0
    curr_waste_percentage = 0
    ids = [x['id'] for x in selectedRecipes]
    for recipe_comb in itertools.combinations(ids, number_of_recipes):
        #Check combination waste and minimise
        #check if value is maximised
        set_value = 0
        for recipeId in recipe_comb:
            set_value += selectedRecipes[recipeId]['ingredients'][maximise_value]
        waste_percentage = calculate_waste(recipe_comb)
        if set_value > curr_val and waste_percentage < curr_waste_percentage:
            best_comb = recipe_comb
            curr_val = set_value
            curr_waste_percentage = waste_percentage
            