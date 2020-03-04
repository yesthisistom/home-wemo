import model
from flask import Blueprint, render_template, redirect

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, HiddenField, SubmitField, SelectField

activity_blueprint = Blueprint('activity', __name__, template_folder='templates')


class ActivityForm(FlaskForm):
    activityname = StringField('Activity Name', validators=[DataRequired()])
    activitytime = StringField('Activity Time', validators=[DataRequired()])
    activitydays = SelectField('Activity Days',
                               choices=[('All Days', "All Days"),
                                        ('Weekdays', 'Weekdays'),
                                        ('Weekends', "Weekends")
                                        ])

    deviceid = HiddenField('Device ID', validators=[DataRequired()])
    activitytype = SelectField('Activity Type',
                               choices=[('True', "Turn On"),
                                        ('False', 'Turn Off')])

    activityid = HiddenField('Activity ID')
    delete = SubmitField('Delete Activity')
    submit = SubmitField('Save Activity')


@activity_blueprint.route("/edit/<int:activity_id>")
def edit_activity(activity_id):
    activity = model.get_activity(activity_id)

    activity_form = ActivityForm(activityname=activity.activity_name, activitytime=activity.activity_time,
                                 activitydays=activity.activity_days, activitytype=activity.turn_on,
                                 deviceid=activity.device_id, activityid=activity_id)
    return render_template('add_activity.html', form=activity_form)


@activity_blueprint.route("/add/<int:device_id>")
def add_activity(device_id):
    activity_form = ActivityForm(deviceid=device_id)
    return render_template('add_activity.html', form=activity_form)


@activity_blueprint.route('/save', methods=['POST'])
def save_activity():

    activity_form = ActivityForm()

    # Validate form
    if activity_form.validate_on_submit():

        turn_on = True if activity_form.activitytype.data == 'True' else False

        # Check if we're updating or creating a new piece of data
        if activity_form.activityid.data:
            if activity_form.submit.data:
                # Update data
                model.update_activity(activity_form.activityid.data,
                                      activity_form.activityname.data,
                                      activity_form.activitytime.data,
                                      activity_form.activitydays.data,
                                      turn_on)
            elif activity_form.delete.data:
                print('delete requested')
                model.delete_activity(activity_form.activityid.data)
        else:
            # Create data
            model.add_activity(activity_form.deviceid.data,
                               activity_form.activityname.data,
                               activity_form.activitytime.data,
                               activity_form.activitydays.data,
                               turn_on)
        return redirect('/')

    print('validate failed?')
    print(activity_form.errors)
    return redirect('/')
