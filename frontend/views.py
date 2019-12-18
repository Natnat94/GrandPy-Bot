from flask import Flask, render_template, redirect, flash, url_for, request, jsonify
from config import Config
from form import LoginForm
from parser_man import Localisation
import json


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/map', methods=['GET','POST'])
def map():
    result = "{ lat: 48.85, lng: 2.29 }"
    if request.method == "POST":
        try:
            loc = Localisation()
            result = loc.run(request.form['Text1'])
            return jsonify(result = result)
        except:
            print("probleme")

    return render_template('map.html', result = result)

@app.route('/api', methods=['GET','POST'])
def api():
    if request.method == "POST":
        loc = Localisation()
        result = loc.run(request.form['Text1'])
        return jsonify(result = result)
    return render_template('map.html', result = result)


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