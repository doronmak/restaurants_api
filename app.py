from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return "Api is on fire!"


@app.get('/restaurants')
def get_all_restaurant():
    return "all rests"


@app.post('/restaurant')
def post_restaurant():
    pass


@app.get('/restaurants/{rest_id}')
def get_restaurant_by_id(rest_id):
    return "rest by id" + rest_id


@app.patch('/restaurants/{rest_id}')
def patch_restaurant_by_id(rest_id):
    return "patched" + rest_id


@app.delete('/restaurants/{rest_id}')
def delete_restaurant_by_id(rest_id):
    return "deleted" + rest_id
