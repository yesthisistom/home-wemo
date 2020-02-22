import model
from flask import Blueprint, render_template, request

index_blueprint = Blueprint('index', __name__, template_folder='templates')


@index_blueprint.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        # First pass -
        #   get current status
        #   do the opposite

        print("Post request")
        # clicked = request.form['data']
        # print("request: ", request)
        # print("clicked: ", clicked)
        status = model.get_device_state("Living room")
        print('status: ', status)
        model.change_state("Living room", 0 if status else 1)

    return render_template('index.html', devices=model.get_devices())