import os
import requests
import dotenv
from datetime import datetime
dotenv.load_dotenv()

nutritionix_headers = {'x-app-id': os.getenv('NUTRITIONIX_ID'),
                       "x-app-key": os.getenv('NUTRITIONIX_API_KEY'), }

sheety_username = 'f285aa2dc34ece9c97eaa30689bd83aa'
sheety_projectName = 'nutritionTrack'
sheetName = 'workouts'
sheety_header = {'Authorization': f'Bearer {os.getenv("SHEETY_BEARER_AUTH")}'}


def get_meals_data():
    nutrition_endpoint = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    query = input("Tell me, what did you eat? ")
    meal_params = {"query": query,
                   "timezone": "JST"}
    response = requests.post(
        nutrition_endpoint, headers=nutritionix_headers, json=meal_params)
    response.raise_for_status()

    nutrition_data = response.json()['foods']  # list of meals
    return nutrition_data


def update_spreadsheet(nutrition_data):
    sheety_endpoint = f"https://api.sheety.co/{sheety_username}/{sheety_projectName}/{sheetName}"

    for meal in nutrition_data:
        sheety_params = {'workout': {
            'date': datetime.fromisoformat(meal['consumed_at']
                                           ).strftime('%d-%m-%Y'),
            'foodName': meal['food_name'],
            'quantity': meal['serving_qty'],
            'unit': meal["serving_unit"],
            "calories": meal['nf_calories'],
        }}
        sheety_response = requests.post(sheety_endpoint,
                                        headers=sheety_header,
                                        json=sheety_params)
        sheety_response.raise_for_status()

if __name__ == "__main__":
    nutrition_data = get_meals_data()
    update_spreadsheet(nutrition_data)
