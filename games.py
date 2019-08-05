from flask import Flask, request

#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField, SubmitField
#from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def main():
    form = request.form
#    return form.get('name') + '''
    tmp = "no items"
    if 'name' in form: tmp = form['name']
    return str(tmp) + str(request.form) + str(request.args) + '''
<h1>Games<h1>
<h2>A work in progress!</h2>
<ul>
<li><a href="/carl">CARL</a></li>
<li><a href="/carl_raw">CARL (raw API, no form)</a></li>
</ul>

<br/><br/>

<h6><a href="https://johanv.xyz/">Back to main site</a></h6>
'''
"""

ROOT_DIR = "/srv"

#START CARL
import json, os, sys, random, re

def getLeastUsed(links, excludeIdx):
    least = []
    for i, item in enumerate(links):
        if i != excludeIdx:
            least.append(len(item))
    least = min(least)
    leastIdx = []
    for i, link in enumerate(links):
        if len(link) == least:
            leastIdx.append(i)
    return random.choice(leastIdx)

splitter = re.compile("[^\w']+")
def spellcheckPhrase(p, phrases):
    best = 0
    bestIdx = 0
    for i, phrase in enumerate(phrases):
        inputWords = [x.lower() for x in splitter.split(p) if x]
        phraseWords = [x.lower() for x in splitter.split(phrase) if x]
        phraseLen = len(phraseWords)

        lenFactor = 0
        if phraseLen != 0:
            lenFactor = 1.0 * len(inputWords) / phraseLen
        if abs(lenFactor - 1) >= 0.2 and abs(len(inputWords) - phraseLen) >= 3:
            continue

        foundCount = 0
        for word in inputWords:
            if word in phraseWords:
                foundCount += 1

        wordsFactor = 0
        if phraseLen != 0:
            wordsFactor = 1.0 * foundCount / phraseLen

        finalFactor = lenFactor * wordsFactor
        if finalFactor > best:
            best = finalFactor
            bestIdx = i

    return bestIdx, best

def answer(carlAsked, userAnswered, channelID):
    channels=("default", "E2", "movies")
    storageFile=ROOT_DIR+"/CARL/channels/"+channels[channelID]+".json"

    if os.path.isfile(storageFile):
        storage = json.load(open(storageFile, 'r'))
    else:
        storage = {
            'phrases':[],
            'links':[],
        }

    illegalChars = ('{', '}', '[', ']', '(', ')', '|', '\\', '<', '>', '/')

    for illegalChar in illegalChars:
        carlAsked = carlAsked.replace(illegalChar, "")
        userAnswered = userAnswered.replace(illegalChar, "")

    phrases = storage['phrases'] #a list of phrases
    links = storage['links'] #a list of links to other phrases from each phrase
    
    if len(userAnswered) == 0 or userAnswered[-1] not in ('.', '!', '?', '"', "'"):
        userAnswered += '.'

    if len(userAnswered) > 250: userAnswered = userAnswered[:250]

    if carlAsked in phrases:
        askIdx = phrases.index(carlAsked)
    else:
        askIdx = -1

    futureAskIdx = -1
    
    if userAnswered in phrases:
        answerIdx = phrases.index(userAnswered)
        if len(links[answerIdx]) > 0:
            futureAskIdx = random.choice(links[answerIdx])
        else:
            futureAskIdx = getLeastUsed(links, answerIdx) #exclude answerIdx
        if askIdx != -1:
            links[askIdx].append(answerIdx)
    else:
        bestIdx, best = spellcheckPhrase(userAnswered, phrases)
        if best > 0.6:
            if len(links[bestIdx]) > 0:
                futureAskIdx = random.choice(links[bestIdx])
            else:
                futureAskIdx = getLeastUsed(links, bestIdx) #exclude answerIdx
            if askIdx != -1:
                links[askIdx].append(bestIdx)
        else:
            futureAskIdx = getLeastUsed(links, bestIdx) #exclude answerIdx
        if askIdx != -1:
            links[askIdx].append(len(phrases))
        links.append([])
        phrases.append(userAnswered)
    json.dump(storage, open(storageFile, 'w'))
    return phrases[futureAskIdx]

#class CarlForm(FlaskForm):
#    carl = StringField('carl', validators=[DataRequired()])
#    user = PasswordField('user', validators=[DataRequired()])
#    channelID = PasswordField('channelID', validators=[NumberRange(min=0, max=2)])
#    submit = SubmitField('Talk')

@app.route("/carl_raw", methods=["GET", "POST"])
def carl_raw():
    form = request.form
    if "carl" in form:
        carl = form["carl"].value
    else:
        carl = ""

    if "user" in form:
        user = form["user"].value
    else:
        user = ""

    if "channelID" in form:
        channelID = form["channelID"].value
    else:
        channelID = "0"
    return CARL_CORE.answer(carl, user, int(channelID))

@app.route("/carl")
def carl_interface():
    form = request.form
    if "carl" in form:
        carl = form["carl"].value
    else:
        carl = ""

    if "user" in form:
        user = form["user"].value
    else:
        user = ""

    if "channelID" in form:
        channelID = form["channelID"].value
    else:
        channelID = "0"

    selected0=""
    selected1=""
    selected2=""
    if channelID == "0": selected0=" selected"
    if channelID == "1": selected1=" selected"
    if channelID == "2": selected2=" selected"
    carl2 = CARL_CORE.answer(carl, user, int(channelID))

    return '''<div style="font-size:50px"><form method="GET">
<select name="channelID">
<option value="0"'''+selected0+'''>default (profanity filter)</option>
<option value="1"'''+selected1+'''>E2 (no filter)</option>
<option value="2"'''+selected2+'''>movies (no memory of what you said)</option>
</select>
<br/>
'''+    "CARL: "+carl+"<br/>"+    "YOU: "+user+"<br/>"+    "CARL: "+carl2+"<br/>"+'''
YOU: <input type="text" name="user" autocomplete="off" style="height:75px">
<input type="hidden" name="carl" value="'''+carl2+'''"><br/>
<input type="submit" value="Talk">
</form></div>'''
#END CARL
"""
if __name__ == "__main__":
  app.run()
