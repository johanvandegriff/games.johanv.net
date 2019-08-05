from flask import Flask, request
import carl

#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField, SubmitField
#from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("index.html")

#START CARL
@app.route("/carl_raw", methods=["GET", "POST"])
def carl_raw():
    form = request.args
    carl = form.get("carl", "")
    user = form.get("user", "")
    channelID = int(form.get("channelID", "0"))
    return answer(carl, user, channelID)

@app.route("/carl")
def carl_interface():
    form = request.args
    carl = form.get("carl", "")
    user = form.get("user", "")
    try:
        channelID = int(form.get("channelID", "0"))
    except ValueError:
        channelID = 0
    
    selected = ["", "", ""]
    selected[channelID] = " selected"
    carl2 = answer(carl, user, channelID)

    return render_template(
        "carl.html",
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
