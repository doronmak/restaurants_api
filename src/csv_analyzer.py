import csv


class CsvFileAdapter(object):
    def __init__(self, file):
        self.csv_file = file
        self.file_after_read = self.read_file()
        self.csv_as_dict = self.csv_to_dict()

    def read_file(self):
        with open(self.csv_file, 'r') as file:
            list_of_rows = []
            reader = csv.reader(file)
            for row in reader:
                list_of_rows.append(row)
        list_of_rows.pop(0)
        for row in list_of_rows:
            location = row.pop(-1)
            row.append(location.split("/"))
        return list_of_rows

    def csv_to_dict(self):
        header = ["Name", "Type", "Phone", "Location"]
        restaurants = []
        for row in self.file_after_read:
            restaurant_dict = {}
            for index in range(len(row)):
                restaurant_dict[header[index]] = row[index]
            restaurants.append(restaurant_dict)
        return restaurants
