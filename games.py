#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for

import os, re, sys

import CARL, boggle, boggle_old
from nav import nav
import profanity_test

app = Flask(__name__)

def run_perl_blacklist(s):
    singlequote = "'"
    return re.sub('[";'+singlequote+']', '', s)


def run_perl(request, perl_program):
    args = request.args.to_dict()
    cgi_vars = ""
    for v in args:
        cgi_vars += " " + '"' + v + "=" + run_perl_blacklist(args[v]).replace('+', '%2B') + '"'
    #return '<pre>'+cgi_vars+'</pre>' + os.popen("perl " + perl_program + cgi_vars).read()
    return os.popen("perl " + perl_program + cgi_vars).read()

def run_perl_page(request, perl_program, title):
    page = run_perl(request, perl_program)
    return render_template("header.html", nav=nav, active=title) + page + render_template("footer.html")

@app.route("/")
def main():
    return render_template("index.html", nav=nav, active="games")

#START checks
@app.route("/check.txt")
def check():
    return "success"

@app.route("/profanity-check-1")
def profanity_check_1():
    return profanity_test.test()

@app.route("/profanity-check-2")
def profanity_check_2():
    try:
        channel = request.args.get("channel", "")
    except ValueError:
        channel = ""
    return profanity_test.test2(channel)

@app.route("/tensorflow-check")
def tensorflow_check():
    import tensorflow as tf
    return tf.__version__
#END checks

#START STOICHIOMETRY
def chem_whitelist(s):
    return re.sub('[^a-zA-Z\d\w.()+-=>→↔⇆]', '', s)

@app.route("/chem", methods=["GET", "POST"])
def stoichiometry():
    args = request.args.to_dict()
    result = ""
    equation = ""
    compound = ""
    grams_or_moles = ""
    grams_or_moles_value = ""

    if "equation" in args:
        equation = chem_whitelist(args["equation"])
        optional_args = ""
        if "compound" in args and "grams_or_moles" in args and "grams_or_moles_value" in args:
            compound = chem_whitelist(args["compound"])
            grams_or_moles = args["grams_or_moles"]
            grams_or_moles_value = chem_whitelist(args["grams_or_moles_value"])
            optional_args = " '" + compound + "' " + grams_or_moles_value + " " + grams_or_moles
        result = os.popen("java -jar Stoichiometry.jar '" + equation + "'" + optional_args).read()
    return render_template("stoichiometry.html", nav=nav, active="chem", result=result, equation=equation, compound=compound, grams_or_moles_value=grams_or_moles_value, grams_or_moles=grams_or_moles)
#END STOICHIOMETRY

#START MATH
@app.route("/math")
def math_page():
    return render_template("math.html", nav=nav, active="math")

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
    return run_perl_page(request, "whack.pl", "whack")
#END WHACK

#START MAZE
@app.route("/maze")
def maze_page():
    return render_template("maze.html", nav=nav, active="maze")

@app.route("/showmaze.pl", methods=["GET", "POST"])
def showmaze_page():
    return run_perl_page(request, "showmaze.pl", "maze")
#END MAZE

#START BOGGLE
@app.route("/boggle", methods=["GET", "POST"])
def boggle_page():
    return boggle.app(request)
#END BOGGLE

#START BOGGLE_OLD
@app.route("/boggle_old", methods=["GET", "POST"])
def boggle_old_page():
    return boggle_old.page(request.args)
#END BOGGLE_OLD

#START CARL
@app.route("/carl_api", methods=["GET", "POST"])
def carl_api():
    carl = request.args.get("carl", "")
    user = request.args.get("user", "")
    allowProfanity = request.args.get("profanity", "") == "true"

    return CARL.answer(carl, user, allowProfanity)

@app.route("/carl", methods=["GET", "POST"])
def carl_page():
    carl = request.args.get("carl", "")
    user = request.args.get("user", "")
    allowProfanity = request.args.get("profanity", "") == "true"

    carl2 = CARL.answer(carl, user, allowProfanity)

    return render_template(
        "carl.html",
        nav=nav,
        active="CARL",
        allowProfanity=allowProfanity,
        carl=carl,
        user=user,
        carl2=carl2
    )
#END CARL

if __name__ == "__main__":
    # app.run()
    app.run(host= '0.0.0.0') # for local testing
