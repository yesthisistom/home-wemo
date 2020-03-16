import model
from flask import Blueprint, render_template, redirect, flash

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, HiddenField, SubmitField, SelectField

device_management_blueprint = Blueprint('device_management', __name__, template_folder='templates')


@device_management_blueprint.route("/edit_device/<int:dev_id>")
def edit_device(activity_id):
    return activity_id


@device_management_blueprint.route("/admin")
def device_management():

    network_devices = model.wemo_control.get_devices_on_network()
    known_devices = model.get_devices()

    name_status_dict = {}
    for device in known_devices:
        name_status_dict[device.name] = 'Active'
        if device.mac not in [dev.mac for dev in network_devices]:
            name_status_dict[device.name] = 'Not Found'

    unknown_list = []
    for device in network_devices:
        if device.mac not in [dev.mac for dev in known_devices]:
            unknown_list.append(device)

    return render_template('device_management.html',
                           unknown_list=unknown_list, name_status_dict=name_status_dict)