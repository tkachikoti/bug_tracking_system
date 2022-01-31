from datetime import date
from flat_file_database import FlatFileDatabase
from utility_module import get_current_time_in_milliseconds, get_date_from_milliseconds

#components_cvs = FlatFileDatabase('models/components.csv')

#print(components_cvs.get_field_names())

#components_cvs.create_row_on_csv({'component_name': 'Component 10', 'component_description': 'This a description of component 10'})

# print(components_cvs.BinarySearch('component_name', 'Component 7'))


# print(FlatFileDatabase('models/components.csv').get_table_rows())

def timeTest():
    # date object of today's date

    print(get_date_from_milliseconds(1643667342654))


timeTest()