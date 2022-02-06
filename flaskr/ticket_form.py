"""This module contains the classes that are used to validate the data
from the create and update POST requests. The module imports several
classes and a module from the wtforms module.
"""
from wtforms import Form, StringField, validators

class CreateTicketForm(Form):
    """This class is used to validate the data from the create POST request."""
    component_name = StringField('component_name', [validators.Length(min=1, max=50)])
    title = StringField('title', [validators.Length(min=1, max=250)])
    description = StringField('description', [validators.Length(min=1, max=5000)])
    priority = StringField('priority', [validators.Length(min=1, max=1)])
    severity = StringField('severity', [validators.Length(min=1, max=1)])
    status = StringField('status', [validators.Length(min=1, max=1)])

class UpdateTicketForm(Form):
    """This class is used to validate the data from the update POST request."""
    uid = StringField('uid', [validators.Length(min=1, max=50)])
    created_at = StringField('created_at', [validators.Length(min=1, max=50)])
    created_at_full_date = StringField('created_at_full_date', [validators.Length(min=1, max=50)])
    component_name = StringField('component_name', [validators.Length(min=1, max=50)])
    title = StringField('title', [validators.Length(min=1, max=250)])
    description = StringField('description', [validators.Length(min=1, max=5000)])
    priority = StringField('priority', [validators.Length(min=1, max=1)])
    severity = StringField('severity', [validators.Length(min=1, max=1)])
    status = StringField('status', [validators.Length(min=1, max=1)])
