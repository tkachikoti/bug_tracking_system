"""This module contains the class FlatFileDatabase. This module includes
imports from utility_module.py and Python's built-in csv module."""
import csv

from utility_module import find_index_in_list_of_dictionaries
from utility_module import sort_list_of_dictionaries
from utility_module import get_current_time_in_milliseconds
from utility_module import get_date_from_milliseconds

class FlatFileDatabase:
    """This class is functions as a conceptual model of a CSV file.
    It is designed to facilitate the use of a CSV file as a flat file
    database. The database would contain data organised in rows and
    columns. The class contains methods that allow the user to create,
    update, and delete rows from the CSV file.The class functions best
    with a CSV file that already have headers. Five predefined headers
    are required on every table for the class to function.
    The headers are: uid, created_at, created_at_full_date, updated_at,
    and updated_at_full_date The class imports several helper functions
    from the utility_module and the Python's built-in csv module.
    """
    def __init__(self, file_path):
        """Initialize the FlatFileDatabase object.
        :param file_path: A string that represents the path to the CSV
        file relative to the root directory.
        :type file_path: str
        """
        self.__file_path = file_path
        self.__field_names = []

    def __get_file_path(self):
        """Return the file path. This is a private method.
        :rtype: str
        :return: The __file_path variable.
        """
        return self.__file_path

    def __get_field_names(self):
        """Return field names. This is a private method.
        :rtype: list
        :return: The __field_names variable.
        """
        return self.__field_names

    def __set_field_names(self, field_names):
        """Set the field names variable. This is a private method.
        :param field_names: A list of field names.
        :type field_names: list
        """
        self.__field_names = field_names
        return self

    def __generate_uid(self):
        """Generate a unique identification (UID) number. The function
        sorts the row in the CSV file by UID in ascending order. The
        function then finds the last UID number in the sorted list and
        adds 1 to it. This number is then return as an integer. This is
        a private method.
        :rtype: int
        :return: An integer that functions as a primary key for a row of
        data on the CSV file.
        """
        new_uid = 1
        table_rows_from_csv = self.select_all_rows_on_csv()
        if len(table_rows_from_csv) > 0:
            sorted_table_rows_from_csv = (
                sort_list_of_dictionaries(table_rows_from_csv, 'uid'))
            new_uid = int(sorted_table_rows_from_csv[-1]['uid']) + 1
        return new_uid

    def __open_csv_file_for_writing(self, modified_table_rows):
        """"Open the CSV file in write mode, add headers followed
        data a row at a time. This is a private method.
        :param modified_table_rows: A list of dictionaries.
        :type modified_table_rows: list
        """
        with open(self.__get_file_path(), mode='w', newline='') as \
                csv_file:
            csv_file_writer = csv.DictWriter(
                csv_file, fieldnames=self.__get_field_names())
            csv_file_writer.writeheader()
            for table_row in modified_table_rows:
                csv_file_writer.writerow(table_row)
        return self

    def select_all_rows_on_csv(self):
        """Return all rows from the CSV file (excluding the first row)
        as a list of dictionaries. Each dictionary in the list contains
        a row of data. The field names are added to __field_names
        variable for future use.
        :rtype: list
        :return: A list of dictionaries.
        """
        table_rows_from_csv = []
        with open(self.__get_file_path(), mode='r', newline='') as csv_file:
            csv_file_reader = csv.DictReader(csv_file)
            self.__set_field_names(list(csv_file_reader.fieldnames))
            for table_row in csv_file_reader:
                table_rows_from_csv.append(table_row)
        return table_rows_from_csv

    def modify_row_on_csv(self, table_row, mode):
        """Helper function that streamlines the process of modify a
        the CSV file. The current state of the CSV file is stored in a
        variable such that the data is not lost during the modification
        process.
        :param table_row: A dictionary that represents a row of data.
        :type table_row: dict
        :param mode: A string that represents the type of operation to
        performed on the CSV file.
        :type mode: str
        """
        original_table_rows_from_csv = self.select_all_rows_on_csv()
        if mode == 'create':
            self.__create_row_on_csv(original_table_rows_from_csv, table_row)
        elif mode == 'update':
            self.__update_row_on_csv(original_table_rows_from_csv, table_row)
        elif mode == 'delete':
            self.__delete_row_on_csv(original_table_rows_from_csv, table_row)
        return self

    def __create_row_on_csv(self, original_table_rows_from_csv, new_table_row):
        """Append a new row of data on the CSV file. Prior to this, a
        unique identification number (UID) and the date of creation are
        generated and added to the dictionary. This a private method.
        :param original_table_rows_from_csv: A list of dictionaries
        representing the unmodified state of the CSV file.
        :type original_table_rows_from_csv: list
        :param new_table_row: A dictionary that represents a row of data.
        :type new_table_row: dict
        """
        new_table_row['uid'] = self.__generate_uid()
        new_table_row['created_at'] = get_current_time_in_milliseconds()
        new_table_row['created_at_full_date'] = get_date_from_milliseconds(
            new_table_row['created_at'])
        modified_table_rows_from_csv = original_table_rows_from_csv
        modified_table_rows_from_csv.append(new_table_row)
        self.__open_csv_file_for_writing(modified_table_rows_from_csv)
        return self

    def __update_row_on_csv(self, original_table_rows_from_csv, updated_table_row):
        """Update an existing row of data on the CSV file. Using the
        unique identification number (UID), the unmodified state of the
        data is retrieved from the CSV file and assigned to a variable.
        Information about when the data was updated is added to the
        dictionary. The modified data then overwrites the unmodified
        data on the CSV file. If the UID is not found, the function
        adds the new data as a new entry to the CSV file.
        This a private method.
        :param original_table_rows_from_csv: A list of dictionaries
        representing the unmodified state of the CSV file.
        :type original_table_rows_from_csv: list
        :param updated_table_row: A dictionary that represents a row of
        data.
        :type updated_table_row: dict
        """
        index_of_updated_table_row = find_index_in_list_of_dictionaries(
            original_table_rows_from_csv, 'uid', updated_table_row['uid'])
        if index_of_updated_table_row != -1:
            modified_table_rows_from_csv = original_table_rows_from_csv
            updated_table_row['updated_at'] = (
                get_current_time_in_milliseconds())
            updated_table_row['updated_at_full_date'] = (
                get_date_from_milliseconds(
                    updated_table_row['updated_at']))
            modified_table_rows_from_csv[index_of_updated_table_row] = (
                updated_table_row)
            self.__open_csv_file_for_writing(modified_table_rows_from_csv)
        else:
            self.__create_row_on_csv(
                original_table_rows_from_csv, updated_table_row)
        return self

    def __delete_row_on_csv(self, original_table_rows_from_csv, deleted_table_row):
        """Delete an existing row of data on the CSV file. Using the
        unique identification number (UID), the index of the unmodified
        state of the date is retrieved and used to delete the row from
        a list of dictionaries representing the unmodified state of the
        CSV file. The modified data then overwrites the unmodified
        data on the CSV file. This a private method.
        :param original_table_rows_from_csv: A list of dictionaries
        representing the unmodified state of the CSV file.
        :type original_table_rows_from_csv: list
        :param deleted_table_row: A dictionary that represents a row of
        data.
        :type deleted_table_row: dict
        """
        index_of_deleted_table_row = find_index_in_list_of_dictionaries(
            original_table_rows_from_csv, 'uid', deleted_table_row['uid'])
        if index_of_deleted_table_row != -1:
            modified_table_rows_from_csv = self.select_all_rows_on_csv()
            del modified_table_rows_from_csv[index_of_deleted_table_row]
            self.__open_csv_file_for_writing(modified_table_rows_from_csv)
        return self
