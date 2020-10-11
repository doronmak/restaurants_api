from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Restaurant


class DB:
    def __init__(self, db_type, db_user, db_password, db_host, db_name):
        self.db_conn_string = "{}://{}:{}@{}:5432/{}".format(db_type,
                                                             db_user,
                                                             db_password,
                                                             db_host,
                                                             db_name)
        self.engine = create_engine(self.db_conn_string, echo=False)
        self.SessionManager = sessionmaker(self.engine)
        self.session = self.SessionManager()

    def create_restaurant_table(self):
        Base.metadata.create_all(self.engine)

    def add_new_restaurant(self, restaurant_name, restaurant_type, restaurant_phone, restaurant_location):
        new_rest = Restaurant(name=restaurant_name,
                              type=restaurant_type,
                              phone=restaurant_phone,
                              location=restaurant_location)
        self.session.add(new_rest)
        self.session.commit()
        return new_rest

    def get_restaurant_by_id(self, rest_id):
        return self.session.query(Restaurant).filter(Restaurant.id == rest_id).first()

    def delete_restaurant_by_id(self, rest_id):
        rest_to_delete = self.get_restaurant_by_id(rest_id)
        self.session.delete(rest_to_delete)
        print(rest_to_delete.id)
        self.session.commit()
        return rest_to_delete

    def get_all_restaurants(self):
        restaurants = self.session.query(Restaurant.id, Restaurant.name, Restaurant.type, Restaurant.phone,
                                         Restaurant.location)
        rest_list = []
        for restaurant in restaurants:
            rest_list.append(restaurant)
        return rest_list

    def update_restaurant(self, rest_id, updated_restaurant):
        restaurant = self.get_restaurant_by_id(rest_id)
        restaurant.name = updated_restaurant.name
        restaurant.type = updated_restaurant.type
        restaurant.phone = updated_restaurant.phone
        restaurant.location = updated_restaurant.location
        self.session.commit()
        return restaurant
