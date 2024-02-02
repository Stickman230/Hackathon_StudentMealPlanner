import requests

def getProductDetails(item: str = "grape") -> dict[str, str]:
    json_data = {"query": item}
    response = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', json=json_data, headers={'Content-Type': 'application/json', 'x-app-id': 'c8792809', 'x-app-key': '3b69a3fd0955a8dc23936081336987bc'})
    return response.json()['foods'][0]

print(getProductDetails())