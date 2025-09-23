#!/usr/bin/env python3

# import 'exit' for exit the program
from sys import exit

# main loop
while True:
    # user input for mode
    mode = input("add more words or print current words? (type 'exit' to exit)\n(add/print): ").strip().lower(); print("\n")

    # check if mode is avilable
    if mode not in ['print','add','p','a','exit']:
        print("invald option\nenter 'print' or 'add'.")
        continue

    # create database file
    create_file = open("words-ar-en", "a", encoding="utf-8")
    create_file.close()

    # opne file as read
    db = open("words-ar-en", "r", encoding="utf-8")
    # dict for store data from database file
    dct_db = {}

    # grab all data from the database file
    for kyval in db:

        # skip spaces lines
        if kyval.isspace():
            continue
        else:
            # convert a line to list
            kyval = kyval.strip().split()
        # check if file a correct ('EN word' '<space>' 'AR word'), 
        # if not correct or has a spaces in arabic words, add underscore to long arabic word.
        if len(kyval) != 2:
            tmpstr = " ".join(kyval[1:])
            kyval = kyval[0:2]
            del kyval[1]
            kyval.append(tmpstr)
        # capitalize the words for ignore duplicated
        kyval[0] = kyval[0].capitalize()
        kyval[1] = kyval[1].capitalize()
        # check a duplicated word if database file modifed manualy
        if kyval[0] in list(dct_db.keys()):
            print("Found a duplicated english word with arabic word: ")
            print(f"first: {kyval[0]} => {dct_db[kyval[0]]}\nsecond: {kyval[0]} => {kyval[1]}\n")
            continue
        # add to dict if all condtions is false
        dct_db[kyval[0]] = kyval[1]
    # close a file
    db.close()

    # 'print' mode
    if mode == "print" or mode == "p":
        # page number 
        page = 2
        print("-" * 50)
        print(f"\t\t\tPage {page}\n".expandtabs(7))
        print("-" * 50)
        for count, wordkv in enumerate(dct_db):
            print(f"{str(count + 1).zfill(4):<4} - \t{wordkv:<5} \t\t\t\t====> \t\t\t\t\t\t{dct_db[wordkv]}".expandtabs(2))
            if (count + 1) % 5 == 0:
                page += 1
                print("-" * 50)
                print(f"\t\t\tPage {page}\n".expandtabs(7))
                print("-" * 50,)

    # add mode
    elif mode == "add" or mode == "a":
        # open file as append
        db = open("words-ar-en", "a", encoding="utf-8")

        # add english word
        en_word = input("enter a english word (without including spaces): ").strip().capitalize()
        # check if word is already exist
        if en_word in list(dct_db.keys()):
            print(f"Wrong!: '{en_word}' is alredy exist in words file:\nexist: {en_word} => {dct_db[en_word]}")
            exit(1)
        else:
            # arabic word
            ar_word = input("enter a arabic word (you can including spaces): ").strip().capitalize()
            db.write(f"{en_word} {ar_word}\n")

        # close file
        db.close()
        print("done.")
    elif mode == "exit":
        print("good bye.")
        break

