from flask import Flask, request, render_template, url_for
import os

import CARL, boggle
from nav import nav
import profanity_test

app = Flask(__name__)

def run_perl(request, perl_program):
    args = request.args.to_dict()
    cgi_vars = ""
    for v in args:
        cgi_vars += " " + '"' + v + "=" + args[v].replace('+', '%2B') + '"'
    #return '<pre>'+cgi_vars+'</pre>' + os.popen("perl " + perl_program + cgi_vars).read()
    return os.popen("perl " + perl_program + cgi_vars).read()

def run_perl_page(request, perl_program, title):
    page = run_perl(request, perl_program)
    return render_template("header.html", nav=nav, active=title) + page + render_template("footer.html")

@app.route("/")
def main():
    return render_template("index.html", nav=nav, active="Games")

@app.route("/profanity-test")
def profanitytest():
    return profanity_test.test()

#START check
@app.route("/check.txt")
def check():
    return "success"
#END check

#START MATH
@app.route("/math")
def math_page():
    return render_template("math.html", nav=nav, active="Math")

@app.route("/math_game.pl", methods=["GET", "POST"])
def math_game():
    return run_perl_page(request, "math_game.pl", "Math")

@app.route("/math_score.pl", methods=["GET", "POST"])
def math_score():
    return run_perl_page(request, "math_score.pl", "Math")
#END MATH

#START WHACK
@app.route("/whack.pl", methods=["GET", "POST"])
def whack_page():
    return run_perl_page(request, "whack.pl", "Whack")
#END WHACK

#START MAZE
@app.route("/maze")
def maze_page():
    return render_template("maze.html", nav=nav, active="Maze")

@app.route("/showmaze.pl", methods=["GET", "POST"])
def showmaze_page():
    return run_perl_page(request, "showmaze.pl", "Maze")
#END MAZE

#START BOGGLE
@app.route("/boggle", methods=["GET", "POST"])
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

@app.route("/carl", methods=["GET", "POST"])
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
