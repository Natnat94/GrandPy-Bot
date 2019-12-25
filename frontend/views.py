from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   url_for)

from config import Config
from parser_man import Localisation

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/api', methods=['POST'])
def api():
    robot = url_for('static', filename ='image/robot.png')
    avatar = url_for('static', filename ='image/avatar.png')
    try:
        loc = Localisation()
        result = loc.run(request.form['Text1'])
        result["robot"] = robot
        result["avatar"] = avatar
        return jsonify(result)
    except:
        return jsonify(status = "false", robot = robot, avatar = avatar)


if __name__ == "__main__":
    app.run()
