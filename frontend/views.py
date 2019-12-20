from flask import Flask, render_template, redirect, flash, url_for, request, jsonify
from config import Config
from form import LoginForm
from parser_man import Localisation
import json


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/api', methods=['POST'])
def api():
    band_member = url_for('static', filename ='image/bandmember.jpg')
    avatar = url_for('static', filename ='image/avatar_g2.jpg')
    try:
        loc = Localisation()
        result = loc.run(request.form['Text1'])
        result["robot"] = band_member
        result["avatar"] = avatar
        return jsonify(result)
    except:
        return jsonify(status = "false", robot = band_member, avatar = avatar)


#### Parti hors sujet !!!!!!! #####

@app.route('/pybot')
def pybot():
    return render_template('grandpy.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/cv')
def cv():
    return render_template('cv.html')

@app.route('/index')
def index():
    user = {'first_name':'Nathan'}
    return render_template("index.html", user=user)

#### Parti hors sujet !!!!!!! #####


if __name__ == "__main__":
    app.run()