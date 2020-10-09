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

    def add_new_restaurant(self, rest_name, rest_type, rest_phone, rest_location):
        new_rest = Restaurants(name=rest_name,
                               type=rest_type,
                               phone=rest_phone,
                               location=rest_location)
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
