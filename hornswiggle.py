#!/usr/bin/python
import random

"""
Dr. Hornswiggle's Trancendental Ideation Generator

person's X
person's X with X
person's X without X
person's X and X
X = noun
X = adj noun
X = adv adj noun
X = adv adj (and) adj noun
X = adv adj (and) adj descriptor
X = adv adj (and) adj noun descriptor
"""

raw = {
  "possessives":"""
Dr. Hornswiggle's
Dr. Hornswoggle's
Prof. Boomquaggle's
Sir Birdzobble's
Madam Drumdrooble's
Mr. Lensfoggle's
Mrs. Cangrooble's
Ms. Rocktobble's
Mx. Ferntibble's
""",
  "adverbs":"""
Aesthetically
Dimensionally
Intergalactically
Organically
Entirely
Absolutely
Magnificently
Aesthetically
Superficially
Seldom
Periodically
Pragmatically
Fully
Very
Extremely
Extraordinarily
""",
  "prefixes":"""
Anti-
Non-
Pre-
Post-
Semi-
Super-
""",
  "adjectives":"""
Fantabulous
Quintessential
Hypothetical
Pre-Owned
Alchemical
Null-Terminated
Skull-Shaped
Automagical
Forgettable
Non-Fungible
Inflammible
Inedible
5-Wheeled
Vacuum-Packed
Benign
Terrible
Supernatural
Quizzical
Cantankerous
Spontaneous
Maritime
Extraordinary
Royal
Alphabetical
Dapper
Dubious
Devious
Non-Binary
Grayscale
Momentous
Trancendental
Additional
Namby-Pamby
Solemn
Angy
Hungy
Precarious
Gargantuan
Monotone
Meddling
""",
  "nouns":"""
Calvacade
Cavalcade
Wibblewobble
Album
Albatross
Bean
Artifact
Pantaloon
Composure
Zeitgeist
Object of Interest
Meal Concept
Tincture
Acid
Abomination
Submarine
Telegraph
Vessel
Potion
Butter
Consciousness
Bounty Hunter
Swag
Cumquat
Ringtone
Ideation
Superposition
Machination
Cacophony
Brouhaha
Flibbertigibbet
Malarkey
Codswallop
Rigmarole
Shenanigan
Technobabble
Pandemonium
Tardigrade
Phantasm
Jargon
Mushroom
Buzzard
Marsupial
Hysterical
""",
  "descriptors":"""
Box
Generator
Sweeper
Transmogrifier
Grafter
Defragmenter
Governor
Facility
Game
Sandwich
Simulator
Parade
Festival
Contraption
Prototype
Accessory
""",
  "conjunctions":"""
, and
, Containing One
, Lacking One
, Sans One
, with Part of One
, Fused with
, with Optional
, with Bonus
""",
  "rare postfix":"""
& Knuckles
, Featuring Dante from the Devil May Cry Series
"""
}

lists = {}
for category in raw:
  lists[category] = [item for item in raw[category].split("\n") if item != ""]

def automagicalSuperposition(chance):
  return random.random() > 1-chance/100

class TrancendentalIdeationGenerator():
  def __init__(self):
    self.words = []
  def add(self, category):
    self.words.append(random.choice(lists[category]))
  def getStr(self):
    return " ".join(self.words).replace("- ", "-").replace(" ,", ",")

  def addDimensionallyHypotheticalObjectOfInterest(self):
    if automagicalSuperposition(95):
      if automagicalSuperposition(40):
        self.add("adverbs")
      if automagicalSuperposition(25):
        self.add("adjectives")
        if automagicalSuperposition(80):
          self.words.append("and")
      if automagicalSuperposition(15):
        self.add("prefixes")
      self.add("adjectives")
    if automagicalSuperposition(80):
      self.add("nouns")
      if automagicalSuperposition(20):
        self.add("descriptors")
        if automagicalSuperposition(25):
          self.add("descriptors")
    else:
      self.add("descriptors")
    if automagicalSuperposition(15):
      self.add("conjunctions")
      self.addDimensionallyHypotheticalObjectOfInterest()

  def generate(self):
    self.add("possessives")
    self.addDimensionallyHypotheticalObjectOfInterest()
    if automagicalSuperposition(2):
      self.add("rare postfix")
      if automagicalSuperposition(5):
        self.add("rare postfix")

def generate():
  words = TrancendentalIdeationGenerator()
  words.generate()
  return words.getStr()
