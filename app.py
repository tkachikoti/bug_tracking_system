from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from FlatFileDatabase import FlatFileDatabase

APP = Flask(__name__)

@APP.route('/')
def index():
    components_csv = FlatFileDatabase('models/components.csv')
    return render_template(
        'index.html.jinja',
        page_title = 'Home',
        components_csv = components_csv.get_table_rows())

@APP.route('/create')
def create():
    components_csv = FlatFileDatabase('models/components.csv')
    priority_and_severity_options_csv = FlatFileDatabase(
        'models/priority_and_severity_options.csv')
    return render_template(
        'create.html.jinja',
        page_title = 'Create Ticket',
        components_csv = components_csv.get_table_rows(),
        priority_and_severity_options_csv = (
            priority_and_severity_options_csv.get_table_rows()))

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=3000, debug=True)