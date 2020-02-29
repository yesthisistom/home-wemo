import model
from flask import Blueprint, render_template, request

index_blueprint = Blueprint('index', __name__, template_folder='templates')


@index_blueprint.route("/changestatus", methods=['POST'])
def changestatus():
    print("Post request")
    print('form:', request.form)
    device_id = request.form['device']
    desired_status = request.form['desired_status']

    print(device_id, desired_status, type(desired_status))

    return str(model.change_state(device_id, desired_status))


@index_blueprint.route("/")
def index():
    devices = model.get_devices()
    devices = sorted(devices, key=lambda x: len(x.activities), reverse=True)
    for device in devices:
        print(device)
    return render_template('index.html', devices=devices)
