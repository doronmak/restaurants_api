import config
import csv


def read_file(file):
    file = open(file, 'r')
    with file:
        list_of_rows = []
        reader = csv.reader(file)
        for row in reader:
            list_of_rows.append(row)
    file.close()
    return list_of_rows


def get_csv_header(list_of_rows):
    header = list_of_rows.pop(0)
    return header


def csv_to_dict(file):
    restaurants = []
    list_of_rows = read_file(file)
    csv_header = get_csv_header(list_of_rows)
    for row in list_of_rows:
        restaurant_dict = {}
        for index in range(len(row)):
            restaurant_dict[csv_header[index]] = row[index]
        restaurants.append(restaurant_dict)
    return restaurants


if __name__ == "__main__":
    print(csv_to_dict(config.Restaurant_file))
