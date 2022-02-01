from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from flat_file_database import FlatFileDatabase

app = Flask(__name__, root_path='flaskr')

@app.route('/')
def index():
    return render_template(
        'index.html.jinja',
        page_title = 'Home',
        tickets_cvs = FlatFileDatabase(
            'flaskr/models/tickets.csv').select_all_rows_on_csv())

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Get the data from the form
        print(request.form['component_name'])
        component_name = request.form['component_name']
        description = request.form['description']
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
    elif request.method == 'GET':
        return render_template(
            'create.html.jinja',
            page_title = 'Create Ticket',
            components_csv = FlatFileDatabase(
                'flaskr/models/components.csv').select_all_rows_on_csv(),
            priority_and_severity_options_csv = (FlatFileDatabase(
                'flaskr/models/priority_and_severity_options.csv').select_all_rows_on_csv()),
            status_options_csv = (FlatFileDatabase(
                'flaskr/models/status_options.csv').select_all_rows_on_csv()))

@app.route('/delete')
def delete():
    if request.args['uid']:
        FlatFileDatabase('flaskr/models/tickets.csv').modify_row_on_csv({
            'uid': request.args['uid']}, 'delete')
        # Redirect to the home page
        return redirect(url_for('index'))
    return redirect(url_for('index'))   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
