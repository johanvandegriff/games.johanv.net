#!/usr/bin/python

def test():
  from profanity_filter import ProfanityFilter
  pf = ProfanityFilter()
  return pf.censor("That's bullshit!")
