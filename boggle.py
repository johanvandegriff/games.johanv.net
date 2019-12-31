from flask import render_template
import sys, cgi, json, datetime, re, time, decimal, subprocess, random

from nav import nav #file in same dir

ROOT_DIR = "/srv/Boggle"
GAMES_FILE = ROOT_DIR + "/games.json"

DEFINITIONS_FILE = ROOT_DIR + '/lists/CollinsScrabbleWords2019WithDefinitions.json'
WORD_LIST_FILE = ROOT_DIR + '/lists/CollinsScrabbleWords2019.json'

# definitions = json.load(open(DEFINITIONS_FILE,'r'))
# wordList = json.load(open(WORD_LIST_FILE,'r'))

#all the dice found in boggle deluxe
BOGGLE_DICE = [
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

#the boggle alphabet
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
            'N','O','P','Qu','R','S','T','U','V','W','X','Y','Z']

#replace quotes
def rq(s):
  return s.replace("'", "&apos;").replace('"', '&quot;')
  #return cgi.escape(s).replace("'", "&apos;").replace('"', '&quot;')

def create(size=5, letters=None, minutes=3):
    if letters is None:
        if size >=5:
            letters = 4
        elif size == 4:
            letters = 3
        else:
            letters = 2

    dice = [] #no dice

    #until we have enough dice for this board size
    while len(dice) < size*size:
        #add a complete set of standard dice
        dice.extend(BOGGLE_DICE[:])
    #if the size is 5 or less, only 1 set is required
    #if the size is 6 or 7, 2 sets are required, etc.

    random.shuffle(dice)

    #construct the board, nested item-by-item
    board = [[dice[i*size+j][random.randint(0,5)] for j in range(size)] for i in range(size)]

    #construct a dict with all the info
    game = {
        "size": size,
        "letters": letters,
        "minutes": minutes,
        "board": board,
        "isStarted": False,
        "isDone": False,
        "players": [],
        "timeCreatedSecond": int(time.time()),
        "secondsLeft": minutes*60
        #TODO: id
        #TODO: timeLeft, or change to startTime
    }
    return game

def calculatePoints(word):
    length = len(word)
    if length > 8: length = 8
    return [0,1,1,1,1,2,3,5,11][length]

#x, y: the current position on the board
#word: the current word
#used: the spots the word has letters from 
def solve_aux(x, y, word, used, board, words, found, size):
    myused = used[:]

    myused.append((x,y)); #use the current spot
    myword = word + board[x][y].lower() #add on to the word

    if myword in words: #if the word is in the list of possible words
        found.append(myword)
        # found[myword] = myused
        words.remove(myword)
    if not any(re.search("^" + myword, word) for word in words):
        return
    for newx in range(x-1,x+2): # +2 because range() is exclusive on the upper bound
        for newy in range(y-1,y+2):
            if (newx>=0 and newy>=0 and newx<size and newy<size and not [newx,newy] in myused):
                solve_aux(newx, newy, myword, myused, board, words, found, size)

def solve(game):
    start = time.time()
    board = game["board"]
    minWordLength = game["letters"]
    size = len(board)

    quantities = [] #the quantities of each letter

    excluded = [] #which letters are not on the board
    for letter in ALPHABET:
        excluded.append(letter) #copy the alphabet to excluded
        quantities.append(0) #fill quantities with 0's
        for letter2 in ALPHABET:
            excluded.append(letter + letter2)
    for x in range(size):
        for y in range(size):
            letter = board[x][y]
            quantities[ALPHABET.index(letter)] += 1 #increase the quantity of the letter
            if letter in excluded: #if the letter is in excluded
                excluded.remove(letter) #remove the letter from excluded
            if letter == 'Qu' and 'U' in excluded: #if the letter is in excluded
                excluded.remove('U') #remove the letter from excluded
            for newx in range(x-1,x+2): # +2 because range() is exclusive on the upper bound
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
    quantities[ALPHABET.index('U')] += quantities[ALPHABET.index('Qu')]

    words = [] #the list of possible words
    
    wordList = json.load(open(WORD_LIST_FILE,'r'))
    for line in wordList: #sort through each word
        if len(line) >= minWordLength: #if the word is long enough
            #if the word does not have too many of any letter
            if not any(line.count(ALPHABET[i].lower()) > quantities[i] for i in range(len(ALPHABET))):
                #if there are no letters not on the board in this word
                if not any(letter.lower() in line for letter in excluded):
                    words.append(line); #add the word to the list of possible words

    score = 0
    numwords = 0
    found = []
    # found = {}

    for x in range(size):
        for y in range(size):
            used = []
            word = ""
            solve_aux(x, y, word, used, board, words, found, size)
    
    score = 0
    for word in found:
        score += calculatePoints(word)
    
    game["board"] = board
    game["words"] = found
    # game["paths"] = found
    game["maxScore"] = score
    game["maxWords"] = len(found)
    game["secondsToSolve"] = time.time() - start
    return game

# print(create(size=4, letters=3, minutes=3))
# print(solve(create(size=7, letters=4, minutes=6)))
# print(solve({'board': [['U', 'E', 'T'], ['O', 'M', 'D'], ['S', 'D', 'Y']], 'letters': 3, 'minutes': 6}))


def saveGamesFile(games):
    json.dump(games, open(GAMES_FILE, 'w'), indent=2) # indentation for development and debugging
    # json.dump(games, open(GAMES_FILE, 'w'))

def loadGamesFile():
    try:
        games = json.load(open(GAMES_FILE, 'r'))
    except FileNotFoundError:
        # if the file doesn't exist, create it with an empty list
        games = []
        saveGamesFile(games)
    return games

def getGameByID(id):
    for game in loadGamesFile():
        if game["id"] == id:
            return game
    return None

# games = loadGamesFile()
# g = solve(create(size=3))
# g["id"] = 102
# games.append(g)
# saveGamesFile(games)

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
        text += '</thead>'
        rows = rows[1:]
    text += '<tbody>'
    for row in rows:
        text += tableRow(row) + '\n'
    text += '</tbody>'
    return text + '</table>'


"""
This method doesn't return html, but JSON data for JS to digest.
It is called with AJAX requests, and the data will be formatted
to update part of the page without reloading the whole thing.
"""
def request_data(form):
    request = form["request"]
    if request == "game":
        if "id" in form:
            id = int(form["id"])
            game = getGameByID(id)
            if game is None:
                print("game request with id {}, game not found".format(id))
                return {}
            else:
                print("game request with id {}, game found".format(id))
                return {"game": game}
        else:
            print("game request with no id")
            return {}
    if request == "games":
        return {"games": loadGamesFile()}

    return {}

def do_action(form):
    action = form["action"]

    if action == "cancel":
        #TODO: delete a game if you are the host, otherwise remove the player from it
        return form

    return form

def load_page(form):
    if not "username" in form:
        page = "login"
    elif "page" in form:
        page = form["page"]
    else:
        page = "lobby"

    if page == "login":
        return render_template("boggle/login.html", page=page, nav=nav, active="Boggle")

    username = form["username"]

    if page == "lobby":
        return render_template("boggle/lobby.html", username=username, nav=nav, active="Boggle")

    if page == "pregame":
        if "id" in form:
            id = form["id"]
        else:
            id = 100
        return render_template("boggle/pregame.html", id=id, username=username, nav=nav, active="Boggle")

    if page == "play":
        if "id" in form:
            id = form["id"]
        else:
            id = 101
        return render_template("boggle/play.html", id=id, username=username, nav=nav, active="Boggle")

    if page == "view":
        if "prev" in form:
            prev = form["prev"]
        else:
            prev = "lobby"

        return render_template("boggle/view.html", username=username, prev=prev, nav=nav, active="Boggle")

    if page == "stats":
        return render_template("boggle/stats.html", username=username, nav=nav, active="Boggle")

    return "404 - '" + str(page) + "' not found"


"""
This method processes all requests coming in, and passes
them to the correct function.

There are 3 important fields:
action - an action to be taken before loading the page,
    such as leaving a game or submitting a list of words
page - the page to be returned, such as the login, lobby,
    pregame, play, and stats pages
request - ask for a certain type of data, such as current
    games, past games, data on 1 particular game, or word
    definition. This overrides the page, so if a request,
    page, and action are all specified, the server will
    do the action, then return the requested data,
    ignoring the page variable.
"""
def app(form):
    if "action" in form:
        form = do_action(form)
    
    if "request" in form:
        return request_data(form)
    else:
        return load_page(form)
