# mtgodecklists

## Goal

Automaticaly search, gather and classify decklists from any kind of online tournaments of Magic : The Gathering (MTGO).

## Utilisation with Local Python

### Installation

Python 3.7.4 is used.
`setupy.py` to install few needed librairies.

### Utilisation

Feed parameters in config.txt.
`python main.py`

### Available Paramaters

#Sealed, Standard, Pioneer, Modern, Pauper, Modern, Legacy, Vintage
FORMAT=Standard
#Challenge, Super Qualifier, League, Preliminary, anything else or <empty>
TYPE=
#mm/dd/yyyy
DATE_FROM=04/18/2020
#mm/dd/yyyy
DATE_TO=05/01/2020
#False or True
DROP_LEAGUES=True
#False or True
DROP_OTHER=True
#[0,1]
DROP_LOW_FREQ=0.7
#Metagame or Companion
RULES=Companion
#False, Metagame or Companion
EXPECTED_TARGETS=Companion
#True or False
STRING_CLEANER=True

## Scrapping

https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info

## Classifying by Expert Rules

### Building of Expert Rules

Expert rules are fixed rules to make classification, within the Magic : The Gathering context, following process will be built as :  
DECK <deck_name>  
RULES :  
MD :  
<rules_for_md>  
SB :  
<rules_for_sb>  
- search a card : <card_name> in  
- search n exemplars card : <n> <card_name> =  
- search at least n exemplars cards : <n> <card_name> <  
- search at maximum n exemplars cards : <n> <card_name> >  
  
### Prediction of archetype
  
Number of expert rules matched is counted to choose the deck, if number of matched rules is too low, deck is "Other" instead of the archetype with the higghest score.

## Classify by Machine Learning

Maybe one day.

## API

To use that easily.

## Feedback

Please feel free to critic and comment.

## Rights

Open-source code and tool for any Magic : The Gathering player or any Python friendly people !
Please at least cite the github if you use it in public.
