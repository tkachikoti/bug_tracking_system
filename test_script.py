import math
from flat_file_database import FlatFileDatabase
from utility_module import text_cosine_similarity

def convert_dictionary_into_string(dictionary):
    string_made_of_concatenated_dictionary_values = ''
    for key, value in dictionary.items():
        string_made_of_concatenated_dictionary_values += ' ' + value
    return string_made_of_concatenated_dictionary_values

def testThisOUt():
    tickets_cvs = FlatFileDatabase('flaskr/models/tickets.csv').select_all_rows_on_csv()

    for ticket in tickets_cvs:
        print(math.floor(text_cosine_similarity(convert_dictionary_into_string(ticket), "what") * 100))

testThisOUt()