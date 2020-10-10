from fastapi import FastAPI
from database.db_manager import DB
from restaurants_analyzer import CSVAnalyzer
from pydantic import BaseModel
import config

app = FastAPI()

restaurants_db = DB(db_type=config.db_type, db_user=config.db_user, db_password=config.db_password,
                    db_host=config.db_host,
                    db_name=config.db_name)

csv_reader = CSVAnalyzer(config.Restaurant_file)


class Restaurant(BaseModel):
    name: str
    type: str
    phone: str
    location: list


def first_app_init():
    restaurants_db.create_restaurant_table()
    csv_dict = csv_reader.csv_as_dict
    for restaurant in csv_dict:
        restaurants_db.add_new_restaurant(restaurant_name=restaurant['Name'], restaurant_type=restaurant['Type'],
                                          restaurant_phone=restaurant['Phone'], restaurant_location=restaurant['Location'])


@app.get('/')
def index():
    return "Api is on fire!"


@app.get('/restaurants')
def get_all_restaurant():
    rest_list = restaurants_db.get_all_restaurants()
    return rest_list


@app.post('/restaurant')
async def post_restaurant(restaurant: Restaurant):
    restaurants_db.add_new_restaurant(restaurant_name=restaurant.Name, restaurant_type=restaurant.Type, restaurant_phone=restaurant.Phone,
                                      restaurant_location=restaurant.Location)
    return "post new restaurant"


@app.get('/restaurants/{rest_id}')
def get_restaurant_by_id(restaurant_id):
    return restaurants_db.get_restaurant_by_id(restaurant_id)


@app.put('/restaurants/{rest_id}')
async def patch_restaurant_by_id(restaurant_id, restaurant: Restaurant):
    update_restaurants = {
        "Name": restaurant.name,
        "Type": restaurant.type,
        "Phone": restaurant.phone,
        "Location": restaurant.location
    }
    restaurants_db.update_restaurant(restaurant_id, update_restaurants)
    return "patched" + restaurant_id


@app.delete('/restaurants/{rest_id}')
def delete_restaurant_by_id(rest_id):
    restaurants_db.delete_restaurant_by_id(rest_id)
    return "delete restaurant" + rest_id
