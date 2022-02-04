# importing "operator" for implementing itemgetter
from datetime import datetime
import math
from operator import itemgetter

# Import class time from time module
from time import time

def sort_list_of_dictionaries(
        list_of_dictionaries, key='', order_by_descending=False):
    """Sort a list of dictionaries by a key. If order_by_descending is
    True, the data is sorted in descending order. If order_by_descending
    is False, the data is sorted in ascending order.
    :param list_of_dictionaries: a list of dictionaries
    :type list_of_dictionaries: list
    :param key: the key to sort by
    :type key: str
    :param order_by_descending: whether to sort in descending order,
    defaults to False.
    :type order_by_descending: bool
    :rtype: list
    :return: the sorted list of dictionaries
    """
    sorted_list_of_dictionaries = []
    if key:
        sorted_list_of_dictionaries = sorted(
            list_of_dictionaries,
            key=itemgetter(key),
            reverse=order_by_descending)
    return sorted_list_of_dictionaries

def find_index_in_list_of_dictionaries(
        list_of_dictionaries: list, key, search_value: str):
    """Find the index of a dictionary in a list of dictionaries using a
    key to specify the field and a search value to find a matching
    value.
    :param list_of_dictionaries: a list of dictionaries
    :type list_of_dictionaries: list
    :param key: the key to search by
    :type key: str
    :param search_value: the value to search for
    :type search_value: str
    """
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

def get_date_from_milliseconds(milliseconds):
    return datetime.fromtimestamp(milliseconds/1000.0)

def get_current_time_in_milliseconds():
    return int(time() * 1000)

def convert_list_of_strings_into_list_of_stripped_lowercase_strings(list_of_strings):
    list_of_lowercase_strings = []
    for string in list_of_strings:
        list_of_lowercase_strings.append(string.lower().strip())
    return list_of_lowercase_strings

def generate_dictionary_of_word_count(input_string):
    list_of_words = (
        convert_list_of_strings_into_list_of_stripped_lowercase_strings(
            input_string.split()))
    dictionary_of_word_count = {}
    for word in list_of_words:
        if word in dictionary_of_word_count:
            dictionary_of_word_count[word] += 1
        else:
            dictionary_of_word_count[word] = 1
    return dictionary_of_word_count

def generate_word_vector(dictionary_of_word_count, list_of_words):
    word_count_vector = []
    for word in list_of_words:
        word_count_vector.append(dictionary_of_word_count.setdefault(word, 0))
    return word_count_vector

def dot_product(vector_a, vector_b):
    product = 0
    for index, value in enumerate(vector_a):
        product += value * vector_b[index]
    return product

def magnitude(vec):
    sum_add = 0
    for index, value in enumerate(vec):
        sum_add += value * value
    return math.sqrt(sum_add)

def cosine_similarity(vector_a, vector_b):
    return dot_product(vector_a, vector_b) / (magnitude(vector_a) * magnitude(vector_b))

def text_cosine_similarity(string_1, string_2):
    dictionary_of_word_count_1 = generate_dictionary_of_word_count(string_1)
    dictionary_of_word_count_2 = generate_dictionary_of_word_count(string_2)
    list_of_words = {
        **dictionary_of_word_count_1, **dictionary_of_word_count_2}
    vector_a = generate_word_vector(
        dictionary_of_word_count_1, list_of_words.keys())
    vector_b = generate_word_vector(
        dictionary_of_word_count_2, list_of_words.keys())
    return cosine_similarity(vector_a, vector_b)

def convert_dictionary_into_string(dictionary):
    string_made_of_concatenated_dictionary_values = ''
    for key, value in dictionary.items():
        string_made_of_concatenated_dictionary_values += ' ' + value
    return string_made_of_concatenated_dictionary_values
