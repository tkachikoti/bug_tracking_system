# importing "operator" for implementing itemgetter
from operator import itemgetter

# Import class time from time module
from time import time

def sort_list_of_dictionaries(
        list_of_dictionaries, key='', order_by_descending=False):
    sorted_list_of_dictionaries = []
    if key:
        sorted_list_of_dictionaries = sorted(
            list_of_dictionaries,
            key=itemgetter(key),
            reverse=order_by_descending)
    return sorted_list_of_dictionaries

def find_index_in_list_of_dictionaries(list_of_dictionaries, key, search_value):
    sorted_list_of_dictionaries = (
        sort_list_of_dictionaries(list_of_dictionaries, key))
    first_element_index = 0
    last_element_index = len(sorted_list_of_dictionaries) - 1
    search_value_index = -1
    while (first_element_index <= last_element_index) and \
            (search_value_index == -1) and len(search_value):
        middle_element_index = (
            first_element_index + last_element_index) // 2
        middle_element = sorted_list_of_dictionaries[middle_element_index]
        if middle_element[key].lower().strip() == search_value.lower().strip():
            search_value_index = middle_element_index
        else:
            if search_value.lower().strip() < middle_element[key].lower().strip():
                last_element_index = middle_element_index -1
            else:
                first_element_index = middle_element_index +1
    return search_value_index

def get_current_time_in_milliseconds():
    return int(time() * 1000)
