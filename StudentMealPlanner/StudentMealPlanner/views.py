"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, jsonify,request
from StudentMealPlanner import app
from helper import titles_similar_to, open_recipe_json_file
from helpers import findRecipe,open_recipe_json_file,findRecipe,MaximiseBy,best_matches_from_ingredients

RECIPES = open_recipe_json_file('db-recipes-modified.json')

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/searchrecipes', methods=['POST'])
def searchrecipes():
    """returns a json with a list of dictionaries containing recipe titles and its corresponding index"""

    searchQuery = request.get_json()['searchQuery']
    print(searchQuery)
    recipe_data= titles_similar_to(searchQuery, RECIPES)
    return jsonify({'recipes':recipe_data})

@app.route('/getrecipe',methods=['POST'])
def getrecipe():
    """returns a json with a recipe"""
    recipeIndex = request.get_json()['recipeNumber']
    # print('recipeIndex1')
    # print(recipeIndex)
    # print(list(RECIPES.keys()))
    recipe = RECIPES[recipeIndex]
    # print(recipe)
    return jsonify({'recipe':recipe})


@app.route('/getsimilarrecipe',methods=['POST'])
def getsimilarrecipe():
    """returns a json with a recipe
    the keys must be ids of recipes, and the values must be the recipes"""
    recipeIndex = request.get_json()['recipeNumber']
    print('recipeIndex2')
    print(recipeIndex)
    
    recipes = findRecipe(recipeIndex)[:5]
    return jsonify({'recipe':recipes})
@app.route('/searchrecipesbyingredients',methods=['POST'])
def searchrecipesbyingredients():
    """returns a json with a list of recipe ids"""
    print('searchrecipesbyingredients')
    print(request.get_json())
    ingredients = request.get_json()['ingredients']
    print(ingredients)
    # recipes = findRecipe(ingredients)
    recipes = best_matches_from_ingredients(ingredients, RECIPES)
    print('RECIPES HERE')
    recipes = [i['id'] for i in recipes]
    print(recipes)
    return jsonify({'recipe':recipes})
    # #temporary
    # recipeData =open_recipe_json_file('db-recipes-modified.json')
    # recipes = [i for i in recipeData]
    # return jsonify({'recipe':recipes[:10]})


@app.route('/optimiseMenu', methods=['POST'])
def optimize_menu():
    
    data = request.json
    selected_recipes_ids = data.get('menuItems', [])
    maximise_value = data.get('nutrient', '')
    number_of_recipes = data.get('numberOfMeals', 0)

    # if not selected_recipes_ids or not maximise_value or not number_of_recipes:
    #     return jsonify({'error': 'Invalid request data'}), 400
    selected_recipes = [findRecipe(ID)[0] for ID in selected_recipes_ids]
    # print(selected_recipes[0][0]['id'])
    # Call your MaximiseBy function
    optimized_menu, max_value, waste_percentage = MaximiseBy(
        selected_recipes, maximise_value, int(number_of_recipes)
    )

    response_data = {
        'optimizedMenu': optimized_menu,
        'maxValue': max_value,
        'wastePercentage': waste_percentage
    }

    return jsonify(response_data)

    
@app.route('/favicon.ico')
def getFavicon():
    with open('./StudentMealPlanner/static/favicon.ico', 'rb') as f:
        data = f.read()
    return data