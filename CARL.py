import json, os, sys, random, re

ROOT_DIR = "/srv/CARL"

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

def answer(carlAsked, userAnswered, allowProfanity):
    if allowProfanity:
        channel = "E2"
    else:
        channel = "default"
        from profanity_filter import ProfanityFilter
        pf = ProfanityFilter()

    storageFile=ROOT_DIR+"/channels/"+channel+".json"

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
        if allowProfanity or pf.is_clean(userAnswered):
            if askIdx != -1:
                links[askIdx].append(len(phrases))
            links.append([])
            phrases.append(userAnswered)
    json.dump(storage, open(storageFile, 'w'))
    return phrases[futureAskIdx]
