#!/usr/bin/env python3

"""
Export MTG Arena decks and collections

Usage: mtga_lister [options] [DECK]

Options:
    -h, --help              Print this help and exit
    -v, --version           Print version and exit
    -D, --database PATH     Path to the json database of card IDs
                            Default: ./mtga_db.json

Arguments:
    DECK    ID of the deck to print. If missing prints the list of decks.
"""
VERSION="0.1.0"

import json
import os
import sys
from docopt import docopt

def get_cards(log, db):
    cards = extract_json(log, "PlayerInventory.GetPlayerCards")

    result = {}

    for cid,quantity in cards.items():
        name = db[cid]["name"]
        result[name] = result.get(name, 0) + quantity

    return result


def get_deck(log, db, deck_id):
    deck = extract_json(log, "Deck.GetDeckLists")[deck_id]

    decklist = { "name": deck["name"], "main": {}, "side": {} }

    for card in deck["mainDeck"]:
        cname = db[card["id"]]["name"]
        main  = decklist["main"]
        main[cname] = main.get(cname, 0) + card["quantity"]

    for card in deck["sideboard"]:
        cname = db[card["id"]]["name"]
        side = decklist["side"]
        side[cname] = side.get(cname, 0) + card["quantity"]

    return decklist


def get_deck_list(log):
    return (["Collection"]
          + [deck["name"] for deck in extract_json(log, "Deck.GetDeckLists")])


def extract_json(log, flag):
    start_line = int([ num for num,content in enumerate(log)
                       if content.startswith("<== " + flag)
                     ][-1]) + 1

    end_token = {"{": "}", "[": "]"}

    end_line = (start_line
               + log[start_line:].index(end_token[log[start_line]])
               + 1)

    return json.loads('\n'.join(log[start_line:end_line]))


def main():
    args = docopt(__doc__, version=VERSION)
    db   = json.load(open(args["--database"] or "./mtga_db.json"))

    if args["DECK"] is None:
        deck = None
    elif args["DECK"].isnumeric():
        deck = int(args["DECK"])
    else:
        deck = -1

    logfile = os.path.expanduser("~/.wine/drive_c/users/"
                                + os.environ["USER"]
                                + "/AppData/LocalLow/Wizards Of The Coast"
                                + "/MTGA/output_log.txt")

    logcontent = open(logfile).read().splitlines()

    deck_list = get_deck_list(logcontent)

    if deck is None:
        for num,each in enumerate(deck_list):
            print("[{}]\t{}".format(num, each))
        return 0

    if deck == -1:
        print("The deck ID must be numeric", out=sys.stdout)
        return 1

    if deck > len(deck_list):
        print("No deck with ID {}".format(deck), out=sys.stdout)
        return 1

    if deck is 0:
        for name,quantity in get_cards(logcontent, db).items():
            print(quantity, name)
        return 0

    deck_content = get_deck(logcontent, db, deck-1)
    print("//", deck_content["name"])

    print("// Main deck_content")
    for name, quantity in deck_content["main"].items():
        print(quantity, name)

    print()
    print("// Sideboard")
    for name, quantity in deck_content["side"].items():
        print(quantity, name)


if __name__ == "__main__":
    main()
