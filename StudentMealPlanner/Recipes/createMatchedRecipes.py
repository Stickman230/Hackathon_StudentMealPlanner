import json



"""
Find recipes based on ingredients and dish type.

Parameters:
    - ingredient_names (list): A list of ingredient names to match against recipes.
    - user_dish_type_choice (str): The dish type (main, side, dessert) chosen by the user to filter recipes.
    - id_of_chosen_recipe (str): The ID of the user's chosen recipe.

Returns:
A dictionary containing the final suggested recipes.
The keys are recipe IDs concatenated with the dish type, and
the values are lists of recipe IDs with similar ingredients."""
            
            
def find_linked_recipes(id_of_chosen_recipe: str) -> list[str]:
    list_of_recipes = []
    list_of_recipeIDs = []

    # Read recipe information from a JSON file
    with open("C:\\Users\\Varun\\Downloads\\db-recipes-modified.json", 'r') as json_file:
        recipes = json.load(json_file)

    # Assume half of the ingredients match for now
    matching_threshold = 0.2

    ingredient_names = list((recipes[id_of_chosen_recipe]['ingredients']).keys())
    tags = recipes[id_of_chosen_recipe]['tags']
    if 'main' in tags or 'side' in tags:
        user_dish_is_dessert = False
    else:
        user_dish_is_dessert = True

    # Iterate through recipes and find a match based on ingredients
    for recipe_id, recipe in recipes.items():
        recipe_ingredients = list(recipe.get('ingredients', {}).keys())
        recipe_tags = recipe.get('tags', [])

        # Calculate the percentage of matching ingredients
        matched_count = sum(ingredient_name in recipe_ingredients for ingredient_name in ingredient_names)
        matching_percentage = matched_count / len(ingredient_names)

        # Check if the matching percentage exceeds the threshold and if the user_dish_type_choice is in the tags
        if matching_percentage >= matching_threshold and ((user_dish_is_dessert and 'dessert' in recipe_tags) or (not user_dish_is_dessert and 'side' in recipe_tags) or (not user_dish_is_dessert and 'main' in recipe_tags)):
            #Add dish to list of recipes
            #list_of_recipes.append(recipe_id + " " + recipe_tags)
            list_of_recipes.append(recipe['name'])
            list_of_recipeIDs.append(recipe_id)

    list_of_recipeIDs.remove(id_of_chosen_recipe)
    return list_of_recipeIDs