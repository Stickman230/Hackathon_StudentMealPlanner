import json
import random

def load_recipes_from_json(json_file):
    with open(json_file, 'r') as file:
        recipes = json.load(file)
    return recipes

def randomise_recipe(similar_recipes: list[dict], blacklist_ingredients: list[str], recipes):
    while True:
        # Choose a random ID from SimilarIngredients
        random_id = random.choice(list(similar_recipes.keys()))

        # Check if the random ID has any blacklisted ingredients
        if any(ingredient in blacklist_ingredients.get(random_id, []) for ingredient in recipes[random_id]['ingredients']):
            continue  # Skip recipes with blacklisted ingredients

        # Check if the random ID is in SimilarIngredients
        if random_id in similar_recipes:
            # Choose a random recipe from the similar ingredients list
            similar_recipe_id = random.choice(similar_recipes[random_id])

            # Check if the similar recipe ID has any blacklisted ingredients
            if any(ingredient in blacklist_ingredients.get(similar_recipe_id, []) for ingredient in recipes[similar_recipe_id]['ingredients']):
                continue  # Skip recipes with blacklisted ingredients

            # Return the chosen similar recipe
            return recipes[similar_recipe_id]

# Example JSON file name
json_file = "db-recipes-modified.json"

# Load recipes from the JSON file
recipes = load_recipes_from_json(json_file)

# Example SimilarIngredients dictionary
similar_ingredients = {
    1: [2, 3],
    4: [5, 6],
    # Add more entries as needed
}

# Example BlacklistIngredients dictionary
blacklist_ingredients = {
    1: ["ingredient2", "ingredient4"],
    4: ["ingredient7", "ingredient8"],
    # Add more entries as needed
}

# Get a random recipe from the loaded recipes that has similar ingredients and does not contain blacklisted ingredients
random_recipe = randomise_recipe(similar_ingredients, blacklist_ingredients, recipes)

print("Random Recipe (After Blacklisting and Including Similar Ingredients):")
print(random_recipe)
