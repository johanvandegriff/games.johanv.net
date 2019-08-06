from flask import render_template
import sys, cgi, json, datetime, re, os, time, decimal, subprocess, random

from nav import nav #file in same dir

LOGIN = 0
LOBBY = 1
JOIN_GAME = 2
VIEW_GAME = 3
PLAY_GAME = 4
GAME_OVER = 5

ROOT_DIR = "/srv/Boggle"
GAMES_FILE = os.path.join(ROOT_DIR, "games.json")
GAME_DURATION = 3 * 60 * 1000 #3 minutes in milliseconds
formMethod = "get"

def header():
    return render_template("header.html", nav=nav, active="Boggle")

def footer():
    return render_template("footer.html")

#replace quotes
def rq(s):
  return cgi.escape(s).replace("'", "&apos;").replace('"', '&quot;')

def create(size=5):
    #all the dice found in boggle deluxe
    dice = [
        ['O','O','O','T','T','U'],
        ['D','H','H','N','O','T'],
        ['N','O','U','T','O','W'],
        ['A','A','A','S','F','R'],
        ['A','E','E','M','U','G'],
        ['A','E','N','N','M','G'],
        ['A','D','E','N','N','N'],
        ['D','D','N','R','L','O'],
        ['C','C','T','S','N','W'],
        ['F','S','I','P','R','Y'],
        ['A','E','E','E','E','M'],
        ['I','R','R','P','H','Y'],
        ['E','O','T','T','T','M'],
        ['A','A','F','I','S','R'],
        ['D','O','L','H','N','R'],
        ['C','E','S','P','T','I'],
        ['A','A','E','E','E','E'],
        ['E','I','I','I','T','T'],
        ['A','F','I','S','R','Y'],
        ['C','E','P','I','T','L'],
        ['E','N','S','S','S','U'],
        ['C','E','I','I','L','T'],
        ['D','H','H','O','L','R'],
        ['G','O','V','R','R','W'],
        ['K','Z','X','B','J','Qu']
    ]

    if size > 5:
        size = 5

    #the empty board
    board = []

    numbers = [] #the order of the dice
    for i in range(len(dice)): #randomize the dice order
        numbers.insert(random.randint(0, i),i)

    for i in range(size):
        row = []
        for j in range(size): #for each board spot
            letter = dice[numbers[i*size+j]][random.randint(0,size)] #roll the dice
            row.append(letter) #set the letter on the board
        board.append(row)
    return [board]


#x, y: the current position on the board
#word: the current word
#used: the spots the word has letters from 
def solve_aux(x, y, word, used, board, words, found, size):
    myused = []
    for item in used: #copy used to myused
        myused.append(item)

    myused.append([x,y]); #use the current spot
    myword = word + board[x][y].lower() #add on to the word

    if myword in words: #if the word is in the list of possible words
        found.append(myword)
        words.remove(myword)
    if not any(re.search("^" + myword, word) for word in words):
        return
    for newx in range(x-1,x+2):
        for newy in range(y-1,y+2):
            if (newx>=0 and newy>=0 and newx<size and newy<size and not [newx,newy] in myused):
                solve_aux(newx, newy, myword, myused, board, words, found, size)

def solve(game, minWordLength):
    board = game[0]
    size = len(board)

    minwordlength = 4
    if len(sys.argv) > 2 and sys.argv[2].isdigit():
        minwordlength = int(sys.argv[2])

    #the boggle alphabet
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
                'N','O','P','Qu','R','S','T','U','V','W','X','Y','Z']

    quantities = [] #the quantities of each letter

    excluded = [] #which letters are not on the board
    for letter in alphabet:
        excluded.append(letter) #copy the alphabet to excluded
        quantities.append(0) #fill quantities with 0's
        for letter2 in alphabet:
            excluded.append(letter + letter2)
    for x in range(size):
        for y in range(size):
            letter = board[x][y]
            quantities[alphabet.index(letter)] += 1 #increase the quantity of the letter
            if letter in excluded: #if the letter is in excluded
                excluded.remove(letter) #remove the letter from excluded
            if letter == 'Qu' and 'U' in excluded: #if the letter is in excluded
                excluded.remove('U') #remove the letter from excluded
            for newx in range(x-1,x+2):
                for newy in range(y-1,y+2):
                    if (newx>=0 and newy>=0 and newx<size and newy<size
                            and not (newx == x and newy == y)):
                        newletter = board[newx][newy]
                        seq = letter + newletter
                        if seq in excluded: #if the sequence is in excluded
                            excluded.remove(seq) #remove the sequence from excluded
                        if letter == 'Qu':
                            seq = 'U' + newletter
                        if seq in excluded: #if the sequence is in excluded
                            excluded.remove(seq) #remove the sequence from excluded

    #increase the number of U's by the number of Qu's
    quantities[alphabet.index('U')] += quantities[alphabet.index('Qu')]

    words = [] #the list of possible words

    for line in open(ROOT_DIR + "/lists/list.txt", 'r'): #sort through each word
        line = line.strip() #remove the newline
        if len(line) >= minwordlength: #if the word is long enough
            #if the word does not have too many of any letter
            if not any(line.count(alphabet[i].lower()) > quantities[i] for i in range(len(alphabet))):
                #if there are no letters not on the board in this word
                if not any(letter.lower() in line for letter in excluded):
                    words.append(line); #add the word to the list of possible words

    score = 0
    numwords = 0
    found = []

    for x in range(size):
        for y in range(size):
            used = []
            word = ""
            solve_aux(x, y, word, used, board, words, found, size)
    return [board, found]

def tableRow(row, tableItem='td'):
    text = ''
    for item in row:
        text += '<'+tableItem+'>' + item + '</'+tableItem+'>'
    return '<tr>' + text + '</tr>'

def table(rows, properties, head=True):
    text = '<table '+properties+'>\n'
    if head:
        text += '<thead>'
        text += tableRow(rows[0], 'th') + '\n'
        text += '<thead>'
        rows = rows[1:]
    text += '<tbody>'
    for row in rows:
        text += tableRow(row) + '\n'
    text += '<tbody>'
    return text + '</table>'

def page(form):
    text = ""
    games = json.load(open(GAMES_FILE, 'r'))

    #form = cgi.FieldStorage()

    if "action" in form:
        action = int(form["action"])
    else:
        action = LOBBY

    if not "username" in form:
        text += header()
        text += '<h1>Boggle</h1>'
        text += '<p>Boggle is a word game with a grid of random letters. The goal is to find letters next to each other that form words. The game lasts 3 minutes and the person with the highest score (longer words are worth more) at the end wins.</p>'
        text += '<h3>Enter your nickname</h3>'
        text += '<form method="' + formMethod + '">'
        text += '<input type="text" name="username" required>'
        text += '<input type="submit" value="Enter" required>'
        text += '<input type="hidden" name="action" value="'+str(LOBBY)+'">'
        text += '</form>'
        text += footer()
        return text

    username = form["username"]
    if action == VIEW_GAME:
        text += header()
        text += '<h1>Boggle</h1>'
        text += '<h3>Past Game</h3>'

        myGameID = 0
        username = ""
        if len(sys.argv) == 3:
            myGameID = sys.argv[1]
            username = sys.argv[2]
        else:
            myGameID = int(form["gameID"])
            username = form["username"]

        myGame = []
        for game in games:
            gameID = game[0]
            if myGameID == gameID:
                break
        myGame = game

        board = myGame[5]

        size = myGame[2]
        size2 = int(size[0])

        players = myGame[7]
        playerWords = myGame[8]
        host = myGame[1][0]

        text += '<a href="/boggle?username=' + rq(username) + '">Back to Lobby</a>'
        text += "<h4>Game hosted by " + rq(host)  + ".</h4>"
        text += "<table cellpadding=10><tr><td>"
        text += display(board, 0)
        text += "</td><td>"

        text += """<table border=1 cellpadding=7>
        <tr><td>Players:</td>"""

        for player in players:
            text += '<td>' + rq(player) + '</td>'
        text += '</tr><tr><td valign="top" style="vertical-align:top">Words:</td>'

        allPlayerWords = []
        for words in playerWords:
            text += '<td valign="top" style="vertical-align:top">'
            words.sort()
            score = 0
            numwords = 0
            for word in words:
                allPlayerWords.append(word)
                points = calculatePoints(word)
                text += ("%2d" %(points)) + " " + word + "<br>"
                score += points
                numwords += 1
            text += "Word Count:  " + str(numwords) + "<br>"
            text += "Total Score: " + str(score) + "<br>"
            text += '</td>'


        text += "</tr></table></td></tr></table>"


        text += "<br>All possible words for this board:<br><br>"

        if(len(myGame) > 6):
            words = myGame[6]
            words.sort()
            found = 0
            total = len(words)
            score = 0
            numwords = 0
            for word in words:
                if word in allPlayerWords:
                    text += '<span style="color:green; font-weight:bold">'
                    found += 1
                points = calculatePoints(word)
                text += ("%2d" %(points)) + " " + word + "<br>"
                score += points
                numwords += 1
                if word in allPlayerWords:
                    text += "</span>"
            text += "Word Count:  " + str(numwords) + "<br>"
            text += "Total Score: " + str(score) + "<br>"
            percent = int(found*100.0/total+0.5)
            text += str(percent) + "% of all these words were found."

        text += footer()
    if action == JOIN_GAME:
        myGame = []
        myGameID = 0
        size = ""
        if "gameID" in form:
            myGameID = int(form["gameID"])
            for game in games:
                gameID = game[0]
                if myGameID == gameID:
                    myGame = game
                    size = myGame[2]
                    break
        else:
            size = form["size"]
            myGameID = 0;
            while any(myGameID == game[0] for game in games):
                myGameID += 1
            myGame = [myGameID, [username], size, 0]
            games.append(myGame)

            size2 = int(size[0])
            if len(myGame) < 6:
                minWordLength = 4
                if size == "4x4":
                    minWordLength = 3
                game = create(size2)
                game = solve(game, minWordLength)
                myGame.append(-1)
                myGame.extend(game)
                myGame.append([])
                myGame.append([])
                json.dump(games, open(GAMES_FILE, 'w'))

        if myGame == []:
            action = LOBBY

        players = myGame[1]
        host = players[0]
        if not myGame[3] == 0:
            if username in players:
                text += play(username, size, myGameID)
            else:
                action = LOBBY

        if not username in players:
            players.append(username)
            json.dump(games, open(GAMES_FILE, 'w'))

        minWordLength = "Four"
        if size == "4x4":
            minWordLength = "Three"
        text += header()
        text += """<h1>Boggle</h1><h4>New Game hosted by """ + rq(host) + ".<br><br>" + rq(size) + " Board, " + rq(minWordLength) + """ letter
    words or more.</h4>
    <p>Waiting for players...</p>
    <form action="">
    <input type="hidden" name="username" value='""" + username + """'>
    <input type="hidden" name="size" value='""" + size + """'>
    <input type="hidden" name="gameID" value='""" + str(myGameID) + """'>
    <input type="hidden" name="action" value='""" + str(JOIN_GAME) + """'>
    <input type="submit" value="Refresh">
    </form>
    <br>
    <table border=1 cellpadding=7>
    <tr><td>Players:</td></tr>"""

        for player in players:
            text += '<tr><td>' + player + '</td></tr>'
        text += "</table><br>"
        if username == host:
            text += """<form action="">
    <input type="hidden" name="username" value='""" + username + """'>
    <input type="hidden" name="action" value='""" + str(PLAY_GAME) + """'>
    <input type="hidden" name="size" value='""" + size + """'>
    <input type="hidden" name="gameID" value='""" + str(myGameID) + """'>
    <input value="Start Game" type="submit">
    </form>"""
        else:
            text += """<script>
    setTimeout(function(){
        window.location.reload(1);
    }, 3000);
    </script>"""
        text += footer()

    if action == PLAY_GAME:
        size = form["size"]
        myGameID = int(form["gameID"])

        myGame = []
        for game in games:
            gameID = game[0]
            if myGameID == gameID:
                break
        myGame = game

        if myGame[3] == 2:
            text += header()
            text += """Content-type: text/html

    <!DOCTYPE html>
    <html>
    <head>
    <script>
    window.location = '/boggle?username=""" + username + """';
    </script>
    <link rel="stylesheet" type="text/css" href="../stylesheet.css" media="all"/>
    </head>
    </html>"""
            return text

        myGame[3] = 1

        players = myGame[1]
        host = players[0]

        if username == host and myGame[4] == -1:
            myGame[4] = time.time() * 1000

        json.dump(games, open(GAMES_FILE, 'w'))

        minWordLength = "Four"
        if size == "4x4":
            minWordLength = "Three"
        text += header()
        text += """<h1>Boggle</h1><h4>Game hosted by """ + rq(host) + ".<br><br>" + size + " Board, " + minWordLength + """ letter
    words or more.</h4>
    <p>The game has started! Good luck, """ + rq(username) + '!</p><h4><p id="time"></p></h4>'
    #"""

        board = myGame[5]
        text += display(board, 1)
        text += """<form action="" id="words" name="words">
<input type="hidden" name="action" value='""" + str(GAME_OVER) + """'>
<input type="hidden" name="username" value='""" + username + """'>
<input type="hidden" name="size" value='""" + size + """'>
<input type="hidden" name="gameID" value='""" + str(myGameID) + """'>

<h1><table cellpadding=13 cellspacing=3>
<tr><td background="/static/boggle_img/space.bmp">
<a style="text-decoration:none;color:#000000" href="javascript:type(' ')">
Space</a></td>
<td background="/static/boggle_img/backspace.bmp">
<a style="text-decoration:none;color:#000000" href="javascript:backspace()">
Backspace</a></td></tr></table></h1>

<textarea rows="20" cols="75" name="words" id="wordBox">
</textarea>
</form>
<script>
var startTime = """ + str(myGame[4]) + """;
var endTime = startTime + """ + str(GAME_DURATION) + """;

countDown();

function type(letter){
    document.getElementById("wordBox").value += letter;
}

function backspace(){
    var box = document.getElementById("wordBox").value.slice(0, -1);
    document.getElementById("wordBox").value = box;
}

function countDown(){
    time = new Date().getTime();
    timeLeft = Math.ceil((endTime - time) / 1000);
    millis = timeLeft;
    minutes = Math.floor(millis / 60);
    seconds = millis % 60;
    if(minutes < 10){
        minutes = "0" + minutes;
    }
    if(seconds < 10){
        seconds = "0" + seconds;
    }
    document.getElementById("time").innerHTML = minutes + ":" + seconds;
    if(millis <= 0){
        clearTimeout(timer);
        document.getElementById("time").innerHTML = "Time's up!";
        document.forms.words.submit();
    }
    var timer = setTimeout("countDown()", 1000);
}
</script>"""
        text += footer()

    if action == GAME_OVER:
        size = form["size"]
        myGameID = int(form["gameID"])
        if "words" in form:
            wordBox = form["words"].lower()
            words = re.split("\s|\n|,", wordBox)
        else:
            words = []

        myGame = []
        for game in games:
            gameID = game[0]
            if myGameID == gameID:
                break
        myGame = game

        myGame[3] = 2

        size2 = int(size[0])

        players = myGame[1]
        host = players[0]

        if not username in myGame[7]:
            allWords = myGame[6]
            validWords = []
            for word in words:
                if word in allWords and not word in validWords:
                    validWords.append(word)
            myGame[7].append(username)
            myGame[8].append(validWords)
        json.dump(games, open(GAMES_FILE, 'w'))

        text += header()
        text += """<script>
function redirect() {
    window.location = '/boggle?action=""" + str(VIEW_GAME) + "&gameID=" + str(gameID) + "&username=" + username + """';
}
setTimeout(redirect, 5000);
</script>
<h2>
Redirect in 5 seconds...
</h2>"""
        text += footer()

    if action == LOBBY:
        lobbyStartTime = time.time()
        text += header()
        text += '<script type="text/javascript" src="/static/sorttable.js"></script>'

        text += '<h1>Boggle Lobby</h1>'
        text += '<p>Welcome, ' + username + '!'
        text += '<form method="' + formMethod + '">'
        text += '<input type="hidden" name="username" value="'+username+'">'
        text += '<input type="hidden" name="action" value="'+str(LOBBY)+'">'
        text += '<input type="hidden" name="skip" value="'+str(True)+'">'
        text += '<input type="submit" value="Refresh" required>'
        text += '</form><br/>'

        text += '<p>You can join one of these games:</p>'
        text += '<form method="' + formMethod + '">'
        text += '<input type="hidden" name="action" value="'+str(JOIN_GAME)+'">'
        text += '<input type="hidden" name="username" value="'+username+'">'

        rows = []

        disabled = "disabled "
        checked = "checked "
        for game in games:
            state = game[3]
            if state == 0:
                gameID = game[0]
                host = game[1][0]
                size = game[2]
                players = len(game[1])
                if checked == "checked ":
                    rows.append(["Select", "Host", "Size", "Players"])
                rows.append(['<input type="radio" ' + checked    + 'name="gameID" value="' + str(gameID) + '">',
                                                                    host, size, str(players)])
                checked = ""
                disabled = ""
        if disabled == "disabled ":
            text += '<p><b>No games are waiting for players.</b></p>'
        else:
            text += table(rows, 'border=1 cellpadding=7 id="waiting" class="sortable"')

        text += '<br/>'
        text += '<input value="Join Game" type="submit" ' + disabled + '>'
        text += '</form><br/><br/>'
        text += '<p>Or you can create a new game:</p>'
        text += '<form method="' + formMethod + '">'
        text += '<input type="hidden" name="action" value="'+str(JOIN_GAME)+'">'
        text += '<input type="hidden" name="username" value="'+username+'">'
        text += """<select name="size">
    <option>5x5</option>
    <option>4x4</option>
    </select>"""
        text += '<input value="Create Game" type="submit" id="create">'
        text += '</form><br/>'
        text += '<p>Games in progress:</p>'

        any1 = 0
        for game in games:
            state = game[3]
            startTime = game[4]
            if state == 1 and time.time() * 1000 > startTime + GAME_DURATION:
                game[3] = 2
                any1 = 1
        if any1 == 1:
            json.dump(games, open(GAMES_FILE, 'w'))

        rows = []

        any1 = 0
        for game in games:
            state = game[3]
            if state == 1:
                gameID = game[0]
                host = game[1][0]
                size = game[2]
                players = len(game[1])
                if any1 == 0:
                    rows.append(["Host", "Size", "Players"])
                rows.append([host, size, str(players)])
                any1 = 1
        if any1 == 0:
            text += '<p><b>No games are in progress.</b></p>'
        else:
            text += table(rows, 'border=1 cellpadding=7 id="playing" class="sortable"')
        text += '<br/><br/>'
        text += '<p>Games that are over:</p>'
        text += '<p>Click on a column to sort by that column</p>'

        rows = []
        rows.append(["Game #", "Host", "Size", "Players", "Total # of Words", "# of Words Found", "% of Words Found"])

        length = len(games)
        for i in range(length-1, -1, -1):
            game = games[i]
            state = game[3]
            if state == 2:
                gameID = game[0]
                host = game[1][0]
                size = game[2]
                players = len(game[1])
                allWords = game[6]
                allPlayerWords = []
                allPlayerWordLists = game[8]
                found = 0
                for playerWords in allPlayerWordLists:
                    for word in playerWords:
                        if not word in allPlayerWords:
                            allPlayerWords.append(word)
                            found += 1
                percent = int(found*10000.0/len(allWords)+0.5)/100.0
                percentStr = str(decimal.Decimal(percent).quantize(decimal.Decimal('0.01')))+"%"
                rows.append(['<a href="/boggle?gameID=' + str(gameID) + '&username=' + username + '&action=' + str(VIEW_GAME) + '">' + str(gameID) + '</a>', host,
                                        size, str(players), str(len(allWords)), str(found), percentStr])
        text += table(rows, 'border=1 cellpadding=7 id="over" class="sortable"')
        text += '<p>It took ' + str(time.time() - lobbyStartTime) + ' seconds to load the lobby.</p>'
        text += footer()
    return text



def display(board, buttons):
    text = ""
    size = len(board)

    text += '<h1><font color="black"><table style="background-color:black" bgcolor="black">'
    for i in range(size):
        text += "<tr>"
        for j in range(size):
            letter = board[i][j]
            if letter == "Qu":
                space = ""
            else:
                space = "&nbsp;"
            if buttons == 1:
                letter = '<a style="text-decoration:none;color:#000000" href="javascript:type(\'' + letter.lower() + '\')">' + letter + '</a>'
            text += '<td width="62" height="62" background="/static/boggle_img/letter.bmp">&thinsp;' + space + letter + "</td>"
        text += "</tr>"
    text += "</table></font></h1>"
    return text


def calculatePoints(word):
    length = len(word)
    if length < 7:
        points = length - 3
    elif length == 7:
        points = 5
    else:
        points = 11
    if points < 1:
        points = 1;
    return points



def lobby(username):
    return """Content-type: text/html

<!DOCTYPE html>
<html>
<head>
<script>
window.location = '/boggle?username=""" + username + """';
</script>
<link rel="stylesheet" type="text/css" href="../stylesheet.css" media="all"/>
</head>
</html>"""

def play(username, size, myGameID):
    return """Content-type: text/html

<!DOCTYPE html>
<html>
<head>
<script>
window.location = '/boggle?username=""" + str(username) + "&action=" + str(PLAY_GAME) + "&size=" + str(size) + "&gameID=" + str(myGameID) + """';
</script>
<link rel="stylesheet" type="text/css" href="../stylesheet.css" media="all"/>
</head>
</html>"""


