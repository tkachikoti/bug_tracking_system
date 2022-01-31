import csv

from utility_module import find_index_in_list_of_dictionaries, sort_list_of_dictionaries, get_current_time_in_milliseconds

class FlatFileDatabase:
    def __init__(self, file_path = 'models/components.csv'):
        self.__file_path = file_path
        self.__field_names = []

    def __get_file_path(self):
        return self.__file_path

    def get_field_names(self):
        return self.__field_names

    def __set_field_names(self, field_names):
        self.__field_names = field_names
        return self

    def __generate_uid(self):
        new_uid = 1
        table_rows_from_csv = self.select_all_rows_on_csv()
        if len(table_rows_from_csv) > 0:
            sorted_table_rows_from_csv = (
                sort_list_of_dictionaries(table_rows_from_csv, 'uid'))
            new_uid = int(sorted_table_rows_from_csv[-1]['uid']) + 1
        return new_uid

    def __open_csv_file_for_writing(self, modified_table_rows):
        with open(self.__get_file_path(), mode='w', newline='') as csv_file:
            csv_file_writer = csv.DictWriter(csv_file, fieldnames=self.get_field_names())
            csv_file_writer.writeheader()
            for table_row in modified_table_rows:
                csv_file_writer.writerow(table_row)
        return self

    def select_all_rows_on_csv(self):
        table_rows_from_csv = []
        with open(self.__get_file_path(), mode='r', newline='') as csv_file:
            csv_file_reader = csv.DictReader(csv_file)
            self.__set_field_names(list(csv_file_reader.fieldnames))
            for table_row in csv_file_reader:
                table_rows_from_csv.append(table_row)
        return table_rows_from_csv

    def modify_row_on_csv(self, table_row, mode):
        original_table_rows_from_csv = self.select_all_rows_on_csv()
        if mode == 'create':
            self.__create_row_on_csv(original_table_rows_from_csv, table_row)
        elif mode == 'update':
            self.__update_row_on_csv(original_table_rows_from_csv, table_row)
        elif mode == 'delete':
            self.__delete_row_on_csv(original_table_rows_from_csv, table_row)
        return self

    def __create_row_on_csv(self, original_table_rows_from_csv, new_table_row):
        new_table_row['uid'] = self.__generate_uid()
        new_table_row['created_at'] = get_current_time_in_milliseconds()
        modified_table_rows_from_csv = original_table_rows_from_csv
        modified_table_rows_from_csv.append(new_table_row)
        self.__open_csv_file_for_writing(modified_table_rows_from_csv)
        return self

    def __update_row_on_csv(self, original_table_rows_from_csv, updated_table_row):
        index_of_updated_table_row = find_index_in_list_of_dictionaries(
            original_table_rows_from_csv, 'uid', updated_table_row['uid'])
        if index_of_updated_table_row != -1:
            modified_table_rows_from_csv = original_table_rows_from_csv
            updated_table_row['updated_at'] = get_current_time_in_milliseconds()
            modified_table_rows_from_csv[index_of_updated_table_row] = updated_table_row
            self.__open_csv_file_for_writing(modified_table_rows_from_csv)
        return self

    def __delete_row_on_csv(self, original_table_rows_from_csv, deleted_table_row):
        index_of_deleted_table_row = find_index_in_list_of_dictionaries(
            original_table_rows_from_csv, 'uid', deleted_table_row['uid'])
        if index_of_deleted_table_row != -1:
            modified_table_rows_from_csv = self.select_all_rows_on_csv()
            del modified_table_rows_from_csv[index_of_deleted_table_row]
            self.__open_csv_file_for_writing(modified_table_rows_from_csv)
        return self
