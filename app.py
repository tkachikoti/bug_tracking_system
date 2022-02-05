import math

from operator import itemgetter
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for

from flaskr.flat_file_database import FlatFileDatabase
from flaskr.ticket_form import CreateTicketForm, UpdateTicketForm
from flaskr.utility_module import find_index_in_list_of_dictionaries
from flaskr.utility_module import string_cosine_similarity

MODEL_FILE_PATH = Path("flaskr/models/")
COMPONENTS = MODEL_FILE_PATH / "components.csv"
PRIORITY_AND_SEVERITY = MODEL_FILE_PATH / "priority_and_severity_options.csv"
STATUS_OPTIONS = MODEL_FILE_PATH / "status_options.csv"
TICKETS = MODEL_FILE_PATH / "tickets.csv"

app = Flask(__name__, root_path='flaskr')

@app.route('/', methods=['GET'])
def index():
    """Render the index page of the application. The function also
    performs a sort operation on the data from the tickets.csv file.
    """
    sort_options = {
        'sort_by': 'uid', 'order_by_descending': '0'}

    if request.method == 'GET' and request.args.get('sort_by', False):
        sort_options['sort_by'] = request.args.get('sort_by')
        sort_options['order_by_descending'] = (
            request.args.get('order_by_descending'))

    return render_template(
        'index.html.jinja',
        page_title='Home',
        sort_options=sort_options,
        tickets_cvs=sorted(
            FlatFileDatabase(TICKETS).select_all_rows_on_csv(),
            key=itemgetter(sort_options['sort_by']),
            reverse=bool(int(sort_options['order_by_descending']))),
        priority_and_severity_options_csv=(
            FlatFileDatabase(PRIORITY_AND_SEVERITY).select_all_rows_on_csv()),
        status_options_csv=(
            FlatFileDatabase(STATUS_OPTIONS).select_all_rows_on_csv()))

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Render the create page of the application. When a POST request is
    received, the function will validate the data and create a new row
    in the tickets.csv file.
    """
    if request.method == 'POST' and request.form.get('component_name', False):
        # Validate the data
        form = CreateTicketForm(request.form)

        if form.validate():
            FlatFileDatabase(TICKETS).modify_row_on_csv({
                'component_name': request.form['component_name'],
                'title': request.form['title'],
                'description': request.form['description'],
                'priority': request.form['priority'],
                'severity': request.form['severity'],
                'status': request.form['status']}, 'create')

        # Redirect to the home page
        return redirect(url_for('index'))
    else:
        return render_template(
            'ticket_form.html.jinja',
            page_title = 'Create Ticket',
            components_csv = FlatFileDatabase(
                COMPONENTS).select_all_rows_on_csv(),
            priority_and_severity_options_csv = (FlatFileDatabase(
                PRIORITY_AND_SEVERITY).select_all_rows_on_csv()),
            status_options_csv = (FlatFileDatabase(
                STATUS_OPTIONS).select_all_rows_on_csv()))

@app.route('/update', methods=['GET', 'POST'])
def update():
    """Render the update page of the application. When a POST request is
    received, the function will validate the data and update the row
    in the tickets.csv file.
    """
    if request.method == 'POST' and request.form.get('uid', False):
        # Validate the data
        form = UpdateTicketForm(request.form)

        if form.validate():
            FlatFileDatabase(TICKETS).modify_row_on_csv({
                'uid': request.form['uid'],
                'created_at': request.form['created_at'],
                'created_at_full_date': request.form['created_at_full_date'],
                'updated_at': request.form['updated_at'],
                'updated_at_full_date': request.form['updated_at_full_date'],
                'component_name': request.form['component_name'],
                'title': request.form['title'],
                'description': request.form['description'],
                'priority': request.form['priority'],
                'severity': request.form['severity'],
                'status': request.form['status']}, 'update')

        # Redirect to the home page
        return redirect(url_for('index'))
    elif request.method == 'GET':
        if request.args['uid']:
            tickets_cvs = (FlatFileDatabase(
                TICKETS).select_all_rows_on_csv())
            ticket_data = tickets_cvs[find_index_in_list_of_dictionaries(
                tickets_cvs, 'uid', search_value=request.args['uid'])]

            return render_template(
                'ticket_form.html.jinja',
                page_title = 'Update Ticket',
                ticket_data = ticket_data,
                components_csv = FlatFileDatabase(
                    COMPONENTS).select_all_rows_on_csv(),
                priority_and_severity_options_csv = (FlatFileDatabase(
                    PRIORITY_AND_SEVERITY).select_all_rows_on_csv()),
                status_options_csv = (FlatFileDatabase(
                    STATUS_OPTIONS).select_all_rows_on_csv()))
        else:
            # Redirect to the home page
            return redirect(url_for('index'))

@app.route('/view', methods=['GET'])
def view():
    """Render the view page of the application. When a GET request is
    received, the UID paramater is used to find the row with the
    corresponding UID in the tickets.csv file
    """
    if request.method == 'GET' and request.args.get('uid', False):
        tickets_cvs = (FlatFileDatabase(
            TICKETS).select_all_rows_on_csv())
        ticket_data = tickets_cvs[find_index_in_list_of_dictionaries(
            tickets_cvs, 'uid', search_value=request.args['uid'])]

        return render_template(
            'view.html.jinja',
            page_title = 'View Ticket',
            ticket_data = ticket_data,
            priority_and_severity_options_csv = (FlatFileDatabase(
                PRIORITY_AND_SEVERITY).select_all_rows_on_csv()),
            status_options_csv = (FlatFileDatabase(
                STATUS_OPTIONS).select_all_rows_on_csv()))
    else:
        # Redirect to the home page
        return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    """Render the search page of the application. When a GET request
    containing a search term is received, the function will search the
    tickets.csv file for the search term and return the results.
    The search function uses consine similarity to find the rows from
    the tickets.csv file that are most similar to the search term. This
    is achieved by converting the search term and the rows of data
    into vectors. The cosine similarity is then
    calculated between the search term and the rows of data. The
    function then sorts the rows of data in descending order with
    respect to the cosine similarity. The higher the similarity score,
    the closer the match.
    """
    search_results = []
    if request.args.get('search_value', '').strip():
        tickets_cvs = (FlatFileDatabase(
            TICKETS).select_all_rows_on_csv())

        for ticket in tickets_cvs:
            similarity_score = string_cosine_similarity(
                ' '.join(ticket.values()), request.args['search_value'])
            if similarity_score:
                ticket['similarity_score'] = math.floor(
                    similarity_score * 100)
                search_results.append(ticket)

    return render_template(
        'search.html.jinja',
        page_title='Search',
        search_value=request.args.get('search_value', '').strip(),
        search_results=sorted(
            search_results,
            key=itemgetter('similarity_score'),
            reverse=True),
        status_options_csv=(
            FlatFileDatabase(STATUS_OPTIONS).select_all_rows_on_csv()))

@app.route('/delete', methods=['POST'])
def delete():
    """Delete the row with the corresponding UID in the tickets.csv
    file.
    """
    if request.form.get('uid', False):
        FlatFileDatabase(TICKETS).modify_row_on_csv(
            {'uid': request.form['uid']}, 'delete')

    # Redirect to the home page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
