from flask import (Flask, jsonify, render_template, request,
                   url_for)


from parser_man import Localisation

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def map():
    return render_template('index.html')


@app.route('/api', methods=['POST'])
def api():
    robot = url_for('static', filename='image/robot.png')
    avatar = url_for('static', filename='image/avatar.png')
    try:
        loc = Localisation()
        result = loc.run(request.form['Text1'])
        result["robot"] = robot
        result["avatar"] = avatar
        return jsonify(result)
    except Exception:
        return jsonify(status="false", robot=robot, avatar=avatar)


if __name__ == "__main__":
    app.run()
