from flask import Flask, request, render_template, url_for

#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField, SubmitField
#from wtforms.validators import DataRequired, NumberRange

import os

import CARL, boggle

from nav import nav

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("index.html", nav=nav, active="Games")

#START MAZE
@app.route("/maze")
def maze_page():
    return render_template("maze.html", nav=nav, active="Maze")

@app.route("/showmaze.pl", methods=['GET', 'POST'])
def showmaze_page():
    cgi_var_names = ["doors", "rooms", "current_room", "door_choice", "users"]
    cgi_vars = ""
    for v in cgi_var_names:
        if v in request.args:
            cgi_vars += " " + v + "=" + request.args[v]
    page = os.popen("perl showmaze.pl" + cgi_vars).read()
    return render_template("header.html", nav=nav, active="Maze") + page + render_template("footer.html")
#END MAZE

#START BOGGLE
@app.route("/boggle", methods=['GET', 'POST'])
def boggle_page():
    return boggle.page(request.args)
#END BOGGLE

#START CARL
@app.route("/carl_api", methods=["GET", "POST"])
def carl_api():
    carl = request.args.get("carl", "")
    user = request.args.get("user", "")
    try:
        channelID = int(request.args.get("channelID", "0"))
    except ValueError:
        channelID = 0
    return CARL.answer(carl, user, channelID)

@app.route("/carl")
def carl_page():
    carl = request.args.get("carl", "")
    user = request.args.get("user", "")
    try:
        channelID = int(request.args.get("channelID", "0"))
    except ValueError:
        channelID = 0
    
    selected = ["", "", ""]
    selected[channelID] = " selected"
    carl2 = CARL.answer(carl, user, channelID)

    return render_template(
        "carl.html",
        nav=nav,
        active="CARL",
        selected0=selected[0],
        selected1=selected[1],
        selected2=selected[2],
        carl=carl,
        user=user,
        carl2=carl2
    )
#END CARL

if __name__ == "__main__":
  app.run()
