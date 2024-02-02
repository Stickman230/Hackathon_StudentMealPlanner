import json
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
if __name__ == '__main__':
    data =open_recipe_json_file('db-recipes-modified.json')
    title_data = titles_similar_to('er', data)
    print(len(title_data))
    print(title_data[0])
    # print('')