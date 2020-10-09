from fastapi import FastAPI
from database.db_manager import DB
from restaurants_analyzer import CSVAnalyzer
import config

app = FastAPI()

restaurants_db = DB(db_type=config.db_type, db_user=config.db_user, db_password=config.db_password,
                    db_host=config.db_host,
                    db_name=config.db_name)

csv_reader = CSVAnalyzer(config.Restaurant_file)


def first_app_init():
    restaurants_db.create_restaurant_table()
    csv_dict = csv_reader.csv_as_dict
    for restaurant in csv_dict:
        restaurants_db.add_new_restaurant(rest_name=restaurant['Name'], rest_type=restaurant['Type'],
                                          rest_phone=restaurant['Phone'], rest_location=restaurant['Location'])


@app.get('/')
def index():
    return "Api is on fire!"


@app.get('/restaurants')
def get_all_restaurant():
    rest_list = restaurants_db.get_all_restaurants()
    return rest_list


@app.post('/restaurant')
def post_restaurant():
    pass


@app.get('/restaurants/{rest_id}')
def get_restaurant_by_id(rest_id):
    return restaurants_db.get_restaurant_by_id(rest_id)


@app.patch('/restaurants/{rest_id}')
def patch_restaurant_by_id(rest_id):
    return "patched" + rest_id


@app.delete('/restaurants/{rest_id}')
def delete_restaurant_by_id(rest_id):
    return restaurants_db.delete_restaurant_by_id(rest_id)
