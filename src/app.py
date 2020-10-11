from fastapi import FastAPI
from src.database.db_manager import DB
from src.csv_analyzer import CSVAnalyzer
from src.settings import config, resources
from src.models.Restaurant import Restaurant
from fastapi.responses import JSONResponse

app = FastAPI()

restaurants_db = DB(db_type=config.DB_PROTOCOL, db_user=config.DB_USERNAME, db_password=config.DB_PASSWORD,
                    db_host=config.DB_HOST,
                    db_name=config.DB_NAME)

csv_reader = CSVAnalyzer(config.RESTAURANTS_FILE)


def first_app_init():
    restaurants_db.create_restaurant_table()
    csv_dict = csv_reader.csv_as_dict
    for restaurant in csv_dict:
        restaurants_db.add_new_restaurant(restaurant_name=restaurant['Name'], restaurant_type=restaurant['Type'],
                                          restaurant_phone=restaurant['Phone'],
                                          restaurant_location=restaurant['Location'])


@app.get('/')
def index():
    data = "Api is on fire!"
    return JSONResponse(content=data, status_code=200)


@app.get(f"{resources.RESTAURANTS}")
def get_all_restaurant():
    restaurants_list = []
    for rest in restaurants_db.get_all_restaurants():
        restaurants_list.append(restaurant_to_dict(rest))
    return JSONResponse(content=restaurants_list, status_code=200)


@app.post(f"{resources.RESTAURANTS}")
async def post_restaurant(restaurant: Restaurant):
    new_rest = restaurants_db.add_new_restaurant(restaurant_name=restaurant.name, restaurant_type=restaurant.type,
                                                 restaurant_phone=restaurant.phone,
                                                 restaurant_location=restaurant.location)
    data = restaurant_to_dict(new_rest)
    return JSONResponse(content=data, status_code=201)


@app.get(f"{resources.RESTAURANTS}" + '/{restaurant_id}')
def get_restaurant_by_id(restaurant_id):
    rest = restaurants_db.get_restaurant_by_id(restaurant_id)
    data = restaurant_to_dict(rest)
    return JSONResponse(content=data, status_code=200)


@app.put(f"{resources.RESTAURANTS}" + '/{restaurant_id}')
async def put_restaurant_by_id(restaurant_id, update_restaurants: Restaurant):
    update_rest = restaurants_db.update_restaurant(restaurant_id, update_restaurants)
    data = restaurant_to_dict(update_rest)
    return JSONResponse(content=data, status_code=200)


@app.delete(f"{resources.RESTAURANTS}" + '/{restaurant_id}')
def delete_restaurant_by_id(restaurant_id):
    deleted_rest = restaurants_db.delete_restaurant_by_id(restaurant_id)
    data = restaurant_to_dict(deleted_rest)
    return JSONResponse(content=data, status_code=200)


def restaurant_to_dict(restaurant):
    return {
        "id": restaurant.id,
        "Name": restaurant.name,
        "Type": restaurant.type,
        "Phone": restaurant.phone,
        "Location": restaurant.location
    }
