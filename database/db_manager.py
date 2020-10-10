from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Restaurants


def rest_to_dict(restaurant):
    header = ["ID", "Name", "Type", "Phone", "Location"]
    rest_dict = {}
    for index in range(len(restaurant)):
        rest_dict[header[index]] = restaurant[index]
    return rest_dict


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
        new_rest = Restaurants(name=restaurant_name,
                               type=restaurant_type,
                               phone=restaurant_phone,
                               location=restaurant_location)
        self.session.add(new_rest)
        self.session.commit()

    def get_restaurant_by_id(self, rest_id):
        restaurant = self.session.query(Restaurants.name, Restaurants.type, Restaurants.phone,
                                        Restaurants.location).filter(Restaurants.id == rest_id)
        return rest_to_dict(restaurant[0])

    def delete_restaurant_by_id(self, rest_id):
        deleted_object = Restaurants.__table__.delete().where(Restaurants.id.in_([rest_id]))
        self.session.execute(deleted_object)
        self.session.commit()

    def get_all_restaurants(self):
        restaurants = self.session.query(Restaurants.id, Restaurants.name, Restaurants.type, Restaurants.phone,
                                         Restaurants.location)
        rest_list = []
        for restaurant in restaurants:
            rest_list.append(rest_to_dict(restaurant))
        return rest_list

    def update_restaurant(self, rest_id, updated_restaurant):
        restaurant = self.session.query(Restaurants).filter(Restaurants.id == rest_id).first()
        restaurant.name = updated_restaurant["Name"]
        restaurant.type = updated_restaurant["Type"]
        restaurant.phone = updated_restaurant["Phone"]
        restaurant.location = updated_restaurant["Location"]
        self.session.commit()
