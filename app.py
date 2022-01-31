from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from flat_file_database import FlatFileDatabase

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html.jinja',
        page_title = 'Home',
        components_csv = FlatFileDatabase(
            'models/components.csv').select_all_rows_on_csv())

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Get the data from the form
        component_name = request.form['component_name']
        component_description = request.form['component_description']
        # Validate the data
        if not component_name or not component_description:
            flash('Please enter all the fields', 'error')
        # If the data is valid, add it to the CSV file
        else:
            # Append the data to the CSV file
            FlatFileDatabase('models/components.csv').add_row(
                [component_name, component_description])
            # Redirect to the home page
            return redirect(url_for('/'))
    elif request.method == 'GET':
        return render_template(
            'create.html.jinja',
            page_title = 'Create Ticket',
            components_csv = FlatFileDatabase(
                'models/components.csv').select_all_rows_on_csv(),
            priority_and_severity_options_csv = (FlatFileDatabase(
                'models/priority_and_severity_options.csv').select_all_rows_on_csv()),
            status_options_csv = (FlatFileDatabase(
                'models/status_options.csv').select_all_rows_on_csv()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
