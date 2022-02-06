"""This module contains functions that test the functionality of the
flask application as well as helper functions that support the app.
This module imports a class from flaskr.flat_file_database and objects
from app.py.
"""
import urllib.parse

from app import app, TICKETS
from flaskr.flat_file_database import FlatFileDatabase

# Instantiate global constants used for test data.
TRACKING_ID = '#28rOpaj2dkJun$u2i07bjhThlppW23xs'
TEST_TICKET_DATA = {
    'component_name': 'App > Index page',
    'title': 'This is a test ticket title [' + TRACKING_ID + ']',
    'description': 'This is a test ticket description',
    'priority': '1',
    'severity': '1',
    'status': '1'
}

def test_index_page_get_request() -> None:
    """Test the index page containing ticket data or blank state."""
    if FlatFileDatabase(TICKETS).select_all_rows_on_csv():
        # Insert a test ticket into the tickets.csv file
        FlatFileDatabase(TICKETS).modify_row_on_csv(TEST_TICKET_DATA, 'create')

        response = app.test_client().get('/')
        assert response.status_code == 200
        assert TRACKING_ID.encode('ascii') in response.data

        # Delete the test ticket from the tickets.csv file
        FlatFileDatabase(TICKETS).modify_row_on_csv(
            {'uid': FlatFileDatabase(TICKETS).select_all_rows_on_csv()[-1]['uid']}, 'delete')
    else:
        response = app.test_client().get('/')
        assert response.status_code == 200
        assert b'No tickets found' in response.data


def test_create_page_get_request() -> None:
    """Test the get request on the create page."""
    response = app.test_client().get('/create')
    assert response.status_code == 200
    assert b'App > Create page' in response.data

def test_create_page_post_request() -> None:
    """Test the post request on the create page."""
    response = app.test_client().post(
        '/create', data=TEST_TICKET_DATA, follow_redirects=True)
    assert response.status_code == 200
    assert TRACKING_ID.encode('ascii') in response.data

    # Delete the test ticket from the tickets.csv file
    FlatFileDatabase(TICKETS).modify_row_on_csv(
        {'uid': FlatFileDatabase(TICKETS).select_all_rows_on_csv()[-1]['uid']}, 'delete')

def test_update_page_get_request() -> None:
    """Test the get request on the update page."""
    # Insert a test ticket into the tickets.csv file
    FlatFileDatabase(TICKETS).modify_row_on_csv(TEST_TICKET_DATA, 'create')

    response = app.test_client().get(
        '/update?uid=' + FlatFileDatabase(TICKETS).select_all_rows_on_csv()[-1]['uid'])
    assert response.status_code == 200
    assert TRACKING_ID.encode('ascii') in response.data

    # Delete the test ticket from the tickets.csv file
    FlatFileDatabase(TICKETS).modify_row_on_csv(
        {'uid': FlatFileDatabase(TICKETS).select_all_rows_on_csv()[-1]['uid']}, 'delete')

def test_update_page_post_request() -> None:
    """Test the post request on the update page."""
    # Insert a test ticket into the tickets.csv file
    FlatFileDatabase(TICKETS).modify_row_on_csv(TEST_TICKET_DATA, 'create')

    modified_ticket_data = FlatFileDatabase(TICKETS).select_all_rows_on_csv()[-1]
    modified_tracking_id = '#28rOpaj2dkl7it8me0wiltyb2i07bjhThlppW23xs'
    modified_ticket_data['title'] = (
        'This is a modified test ticket title [' + modified_tracking_id + ']')

    response = app.test_client().post(
        '/update', data=modified_ticket_data, follow_redirects=True)
    assert response.status_code == 200
    assert modified_tracking_id.encode('ascii') in response.data

    # Delete the test ticket from the tickets.csv file
    FlatFileDatabase(TICKETS).modify_row_on_csv(
        {'uid': FlatFileDatabase(TICKETS).select_all_rows_on_csv()[-1]['uid']}, 'delete')

def test_view_page_get_request() -> None:
    """Test the get request on the view page."""
    # Insert a test ticket into the tickets.csv file
    FlatFileDatabase(TICKETS).modify_row_on_csv(TEST_TICKET_DATA, 'create')

    response = app.test_client().get(
        '/view?uid=' + FlatFileDatabase(TICKETS).select_all_rows_on_csv()[-1]['uid'])
    assert response.status_code == 200
    assert TRACKING_ID.encode('ascii') in response.data

    # Delete the test ticket from the tickets.csv file
    FlatFileDatabase(TICKETS).modify_row_on_csv(
        {'uid': FlatFileDatabase(TICKETS).select_all_rows_on_csv()[-1]['uid']}, 'delete')

def test_search_page_get_request() -> None:
    """Test the get request on the search page."""
    # Insert a test ticket into the tickets.csv file
    FlatFileDatabase(TICKETS).modify_row_on_csv(TEST_TICKET_DATA, 'create')

    response = app.test_client().get(
        '/search?search_value=' + urllib.parse.quote(TRACKING_ID.encode('utf8')))
    assert response.status_code == 200
    assert TRACKING_ID.encode('ascii') in response.data

    # Delete the test ticket from the tickets.csv file
    FlatFileDatabase(TICKETS).modify_row_on_csv(
        {'uid': FlatFileDatabase(TICKETS).select_all_rows_on_csv()[-1]['uid']}, 'delete')

def test_delete_post_request() -> None:
    """Test the post request on the delete route."""
    # Insert a test ticket into the tickets.csv file
    FlatFileDatabase(TICKETS).modify_row_on_csv(TEST_TICKET_DATA, 'create')

    test_ticket_uid = FlatFileDatabase(TICKETS).select_all_rows_on_csv()[-1]['uid']

    response = app.test_client().post(
        '/delete', data={'uid': test_ticket_uid}, follow_redirects=True)
    assert response.status_code == 200
    assert not TRACKING_ID.encode('ascii') in response.data
