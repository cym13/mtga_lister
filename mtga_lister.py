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
VERSION="0.2.0"

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
    return [deck["name"] for deck in extract_json(log, "Deck.GetDeckLists")]


def get_player_inventory(log):
    return extract_json(log, "PlayerInventory.GetPlayerInventory")


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
    elif args["DECK"] in ["c", "i"]:
        deck = args["DECK"]
    else:
        deck = -1

    logfile = os.path.expanduser("~/.wine/drive_c/users/"
                                + os.environ["USER"]
                                + "/AppData/LocalLow/Wizards Of The Coast"
                                + "/MTGA/output_log.txt")

    logcontent = open(logfile).read().splitlines()

    deck_list = get_deck_list(logcontent)

    if deck is None:
        print("[c]\tCard collection")
        print("[i]\tPlayer inventory")
        for num,each in enumerate(deck_list):
            print("[{}]\t{}".format(num, each))
        return 0

    if deck == "c":
        print("// Collection")
        for name,quantity in get_cards(logcontent, db).items():
            print(quantity, name)
        return 0

    if deck == "i":
        print("// Player inventory")
        inventory = get_player_inventory(logcontent)

        texts = {
                    "WC Mythic:\t":   "wcMythic",
                    "WC Rare:\t":     "wcRare",
                    "WC Uncommon:\t": "wcUncommon",
                    "WC Common:\t":   "wcUncommon",
                    "Total Gold:\t":  "gold",
                    "Total Gems:\t":  "gems"
                }

        for text,key in texts.items():
            print(text, inventory[key])

        print("Booster packs:\t",
              sum(b["count"] for b in inventory["boosters"]))
        return 0

    if deck < 0 or deck >= len(deck_list):
        print("No deck found with this ID".format(deck), file=sys.stderr)
        sys.exit(1)

    deck_content = get_deck(logcontent, db, deck)
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
