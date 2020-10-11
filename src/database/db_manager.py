from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Restaurant


class RestaurantsDB(object):
    def __init__(self, protocol, user, password, host, name, port):
        self.db_conn_string = f"{protocol}://{user}:{password}@{host}:{port}/{name}"
        self.engine = create_engine(self.db_conn_string, echo=False)
        self.SessionManager = sessionmaker(self.engine)
        self.session = self.SessionManager()

    def create_restaurant_table(self):
        Base.metadata.create_all(self.engine)

    def add_new_restaurant(self, restaurant_name, restaurant_type, restaurant_phone, restaurant_location):
        try:
            new_rest = Restaurant(name=restaurant_name,
                                  type=restaurant_type,
                                  phone=restaurant_phone,
                                  location=restaurant_location)
            self.session.add(new_rest)
            self.session.commit()
            return new_rest
        except Exception as error:
            raise error

    def get_restaurant_by_id(self, rest_id):
        restaurant = self.session.query(Restaurant).filter(Restaurant.id == rest_id).first()
        if restaurant is not None:
            return restaurant
        else:
            raise Exception('Restaurant was not found')

    def delete_restaurant_by_id(self, rest_id):
        try:
            rest_to_delete = self.get_restaurant_by_id(rest_id)
            self.session.delete(rest_to_delete)
            self.session.commit()
            return rest_to_delete
        except Exception as error:
            raise error

    def get_all_restaurants(self):
        try:
            restaurants = self.session.query(Restaurant.id, Restaurant.name, Restaurant.type, Restaurant.phone,
                                             Restaurant.location)
            rest_list = []
            for restaurant in restaurants:
                rest_list.append(restaurant)
            return rest_list
        except Exception as error:
            raise error

    def update_restaurant(self, rest_id, updated_restaurant):
        restaurant = self.get_restaurant_by_id(rest_id)
        restaurant.name = updated_restaurant.name
        restaurant.type = updated_restaurant.type
        restaurant.phone = updated_restaurant.phone
        restaurant.location = updated_restaurant.location
        self.session.commit()
        return restaurant
