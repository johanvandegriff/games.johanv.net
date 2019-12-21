#!/usr/bin/python

def test():
    from profanity_filter import ProfanityFilter
    pf = ProfanityFilter()
    return pf.censor("That's bullshit!")

def test2(channel):
    import time
    start = time.time()
    from profanity_filter import ProfanityFilter
    pf = ProfanityFilter()
    end = time.time()
    #import json
    #j = json.load(open("/srv/CARL/channels/"+channel+".json",'r'))
    #s = ""
    #n = 0
    #for phrase in j["phrases"]:
        #clean = pf.is_clean(phrase)
        #s += str(clean) + " " + phrase + "<br/>\n"
        #if not clean: n += 1
    #return s + str(n) + "<br/>\n" + str(end-start)
    return str(end-start)
