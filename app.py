from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from FlatFileDatabase import FlatFileDatabase

APP = Flask(__name__)

@APP.route('/')
def index():
    components_csv = FlatFileDatabase('models/components.csv')
    return render_template(
        'index.html',
        data=components_csv.get_table_rows())

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)