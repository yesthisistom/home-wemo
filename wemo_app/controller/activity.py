import model
from flask import Blueprint, render_template, redirect

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, HiddenField, SubmitField

activity_blueprint = Blueprint('activity', __name__, template_folder='templates')


class ActivityForm(FlaskForm):
    activityname = StringField('Activity Name', validators=[DataRequired()])
    activitytime = StringField('Activity Time', validators=[DataRequired()])
    deviceid = HiddenField('Device ID', validators=[DataRequired()])

    submit = SubmitField('Save Activity')


@activity_blueprint.route("/add/<int:device_id>")
def add_activity(device_id):
    activity_form = ActivityForm(deviceid = device_id)
    return render_template('add_activity.html', device_id=device_id, form=activity_form)


@activity_blueprint.route('/save', methods=['POST'])
def save_activity():
    activity_form = ActivityForm()
    if activity_form.validate_on_submit():
        print(activity_form.activityname.data, activity_form.activitytime.data, activity_form.deviceid.data)
        return redirect('/')

    return redirect('/') # Todo: re-route