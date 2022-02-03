import math

from flask import Flask, render_template, request, redirect, url_for

from flat_file_database import FlatFileDatabase
from utility_module import convert_dictionary_into_string
from utility_module import find_index_in_list_of_dictionaries
from utility_module import sort_list_of_dictionaries, text_cosine_similarity


app = Flask(__name__, root_path='flaskr')

@app.route('/', methods=['GET'])
def index():
    """< Summary. >
    :param <variable_name>: <variable_description>, defaults to <default_value>
    :type <variable_name>: <variable_type>(, optional)
    <other parameters and types>
    :raises <error_type>: <error_description>
    <other exceptions>
    :rtype: <return_type>
    :return: <return_description>
    """
    sort_options = {
        'sort_by': 'uid',
        'order_by_descending': '0'}
    if request.method == 'GET' and request.args.get('sort_by', False):
        sort_options['sort_by'] = request.args.get('sort_by')
        sort_options['order_by_descending'] = request.args.get('order_by_descending')
    return render_template(
        'index.html.jinja',
        page_title = 'Home',
        sort_options = sort_options,
        tickets_cvs = sort_list_of_dictionaries(
            FlatFileDatabase(
                'flaskr/models/tickets.csv').select_all_rows_on_csv(),
                sort_options['sort_by'],
                bool(int(sort_options['order_by_descending']))),
        priority_and_severity_options_csv = (FlatFileDatabase(
            'flaskr/models/priority_and_severity_options.csv').select_all_rows_on_csv()),
        status_options_csv = (FlatFileDatabase(
            'flaskr/models/status_options.csv').select_all_rows_on_csv()))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST' and request.form.get('component_name', False):
        # Get the data from the form
        # Validate the data
        FlatFileDatabase('flaskr/models/tickets.csv').modify_row_on_csv({
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
                'flaskr/models/components.csv').select_all_rows_on_csv(),
            priority_and_severity_options_csv = (FlatFileDatabase(
                'flaskr/models/priority_and_severity_options.csv').select_all_rows_on_csv()),
            status_options_csv = (FlatFileDatabase(
                'flaskr/models/status_options.csv').select_all_rows_on_csv()))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST' and request.form.get('uid', False):
        # Get the data from the form
        # Validate the data
        FlatFileDatabase('flaskr/models/tickets.csv').modify_row_on_csv({
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
                'flaskr/models/tickets.csv').select_all_rows_on_csv())
            ticket_data = tickets_cvs[find_index_in_list_of_dictionaries(
                tickets_cvs, 'uid', search_value=request.args['uid'])]
            return render_template(
                'ticket_form.html.jinja',
                page_title = 'Update Ticket',
                ticket_data = ticket_data,
                components_csv = FlatFileDatabase(
                    'flaskr/models/components.csv').select_all_rows_on_csv(),
                priority_and_severity_options_csv = (FlatFileDatabase(
                    'flaskr/models/priority_and_severity_options.csv').select_all_rows_on_csv()),
                status_options_csv = (FlatFileDatabase(
                    'flaskr/models/status_options.csv').select_all_rows_on_csv()))
        else:
            # Redirect to the home page
            return redirect(url_for('index'))

@app.route('/view')
def view():
    if request.args.get('uid', False):
        tickets_cvs = (FlatFileDatabase(
            'flaskr/models/tickets.csv').select_all_rows_on_csv())
        ticket_data = tickets_cvs[find_index_in_list_of_dictionaries(
            tickets_cvs, 'uid', search_value=request.args['uid'])]
        return render_template(
            'view.html.jinja',
            page_title = 'View Ticket',
            ticket_data = ticket_data,
            priority_and_severity_options_csv = (FlatFileDatabase(
                'flaskr/models/priority_and_severity_options.csv').select_all_rows_on_csv()),
            status_options_csv = (FlatFileDatabase(
                'flaskr/models/status_options.csv').select_all_rows_on_csv()))
    else:
        # Redirect to the home page
        return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    search_results = []
    print(request.form.get('search_value', ''))
    if request.form.get('search_value', '').strip():
        tickets_cvs = (FlatFileDatabase(
            'flaskr/models/tickets.csv').select_all_rows_on_csv())
        for ticket in tickets_cvs:
            similarity_score = text_cosine_similarity(
                convert_dictionary_into_string(ticket),
                    request.form['search_value'])
            if similarity_score:
                ticket['similarity_score'] = math.floor(
                    similarity_score * 100)
                search_results.append(ticket)

    return render_template(
        'search.html.jinja',
        page_title = 'Search',
        search_value = request.form.get('search_value', '').strip(),
        search_results = sort_list_of_dictionaries(
            search_results, 'similarity_score', True),
        status_options_csv = (FlatFileDatabase(
            'flaskr/models/status_options.csv').select_all_rows_on_csv()))

@app.route('/delete')
def delete():
    if request.args.get('uid', False):
        FlatFileDatabase('flaskr/models/tickets.csv').modify_row_on_csv({
            'uid': request.args['uid']}, 'delete')
    # Redirect to the home page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
