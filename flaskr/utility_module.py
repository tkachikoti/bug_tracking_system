"""This module contains the utility functions for the flask application.
The functions in this module are helper functions to support the
features of the flask application. This module imports other modules
from Python's standard library, including: datetime, math, operator and time.
"""
from datetime import datetime
import math
from operator import itemgetter
import string
from time import time

import numpy as np

def find_index_in_list_of_dictionaries(list_of_dictionaries: list, key, search_value: str) -> int:
    """Use a binary search algorithm to find the index of a dictionary
    in a list of dictionaries. A key is used to specify the field. A
    search value to find a matching value in a given dictionary.
    :param list_of_dictionaries: a list of dictionaries
    :type list_of_dictionaries: list
    :param key: the key to search by
    :type key: str
    :param search_value: the value to search for
    :type search_value: str
    """
    sorted_list_of_dictionaries = sorted(
        list_of_dictionaries,
        key=itemgetter(key),
        reverse=False)
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

def get_date_from_milliseconds(milliseconds: int) -> str:
    """Convert milliseconds to a date string.
    :param milliseconds: the number of milliseconds
    :type milliseconds: int
    :rtype: str
    :return: the date string in the format: 'YYYY-MM-DD HH:MM:SS.Ms'
    """
    ONE_THOUSAND_SECONDS = 1000.0
    return datetime.fromtimestamp(milliseconds/ONE_THOUSAND_SECONDS)

def get_current_time_in_milliseconds() -> int:
    """Get the current time in milliseconds.
    :rtype: int
    :return: the current time in milliseconds
    """
    ONE_THOUSAND_SECONDS = 1000
    return int(time() * ONE_THOUSAND_SECONDS)

def generate_dictionary_of_word_count(input_string: str) -> dict:
    """Generate a dictionary containing the words from input_string as
    keys and each words'count as the corresponding value. The
    input_string is converted to a list of lower case words that are
    stripped of white space and punctuation. The newly created list of
    words is then iterated through and the dictionary is updated with
    the words and their count.
    :param input_string: the string to be converted
    :type input_string: str
    :rtype: dict
    :return: a dictionary containing the words from input_string and
    their count.
    """
    list_of_words = [
        word.translate(str.maketrans('','',string.punctuation)).lower().strip() \
        for word in input_string.split()
    ]
    dictionary_of_word_count = {}
    for word in list_of_words:
        if word in dictionary_of_word_count:
            dictionary_of_word_count[word] += 1
        else:
            dictionary_of_word_count[word] = 1
    return dictionary_of_word_count

def magnitude(vector: list) -> float:
    """Calculate the magnitude of a vector.
    :param vector: the vector to be calculated
    :type vector: list
    :rtype: float
    :return: the magnitude of the vector
    """
    return math.sqrt(sum(pow(element, 2) for element in vector))

def string_cosine_similarity(string_1: str, string_2: str) -> float:
    """Calculate the cosine similarity between two strings.
    :param string_1: the first string
    :type string_1: str
    :param string_2: the second string
    :type string_2: str
    :rtype: float
    :return: the cosine similarity between the two strings
    """
    dictionary_of_word_count_1 = generate_dictionary_of_word_count(string_1)
    dictionary_of_word_count_2 = generate_dictionary_of_word_count(string_2)
    list_of_words = {
        **dictionary_of_word_count_1, **dictionary_of_word_count_2}
    vector_a = [
        dictionary_of_word_count_1.get(word, 0) for word in list_of_words]
    vector_b = [
        dictionary_of_word_count_2.get(word, 0) for word in list_of_words]
    return np.dot(vector_a, vector_b) / (magnitude(vector_a) * magnitude(vector_b))
