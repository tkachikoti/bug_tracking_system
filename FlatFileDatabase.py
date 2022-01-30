import csv

class FlatFileDatabase:
    def __init__(self, file_path = 'models/components.csv'):
        self.__file_path = file_path
        self.__table_rows = []
        self.select_all_table_rows_from_csv()

    def get_table_rows(self):
        return self.__table_rows

    def set_table_rows(self, table_row):
        self.__table_rows.append(table_row)
        return self

    def select_all_table_rows_from_csv(self):
        with open(self.__file_path, mode='r', newline='') as csv_file:
            csv_file_reader = csv.DictReader(csv_file)
            for table_row in csv_file_reader:
                self.set_table_rows(table_row)
        return self