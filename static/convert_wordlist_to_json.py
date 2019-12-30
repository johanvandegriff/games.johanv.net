"""
https://boardgames.stackexchange.com/questions/38366/latest-collins-scrabble-words-list-in-text-file
Both files have been converted into json.
CollinsScrabbleWords2019.json
    Collins Scrabble Words (2019). 279,496 words. Words only.
    A list of words, all caps
CollinsScrabbleWords2019WithDefinitions.json
    Collins Scrabble Words (2019). 279,496 words with definitions.
    A dict of word -> definition
"""
import json, re

words = open('Collins Scrabble Words (2019).txt', 'r')
wordList = [line.strip().lower() for line in words]
del wordList[0], wordList[0] # the first 2 lines of the file are metadata
json.dump(wordList, open('CollinsScrabbleWords2019.json','w'))

defs = open('Collins Scrabble Words (2019) with definitions.txt', 'r')
defsDict = {}
for line in defs:
    q = re.split(r'\t', line.strip()) #split by tab
    if len(q) == 2:
        defsDict[q[0].lower()] = q[1]
    else:
        print("@@@", line, q)

json.dump(defsDict, open('CollinsScrabbleWords2019WithDefinitions.json','w'))


"""
import json
wordList = json.load(open('CollinsScrabbleWords2019.json','r'))
defs = json.load(open('CollinsScrabbleWords2019WithDefinitions.json','r'))
"""
