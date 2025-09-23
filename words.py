#!/usr/bin/env python3

from sys import exit # import 'exit' for exit the program
import json # import 'json' for store data.
import os, time # import needed modules

JSON_FILE = 'words-ar-en.json'

# function for clear screen for cross-platforms
def clear():
    # UNIX \ Linux
    if os.name == 'posix':
        os.system('clear')
    # 🪟
    elif os.name == 'nt':
        os.system('cls')

def replace_key(dct, old_key, new_key):
    try:
        dct[new_key] = dct.pop(old_key)
        return True
    except KeyError:
        return False

# main loop
while True:
    # user input for mode
    mode = input("choose mode:\n- print / p:\n- add / a\n- remove / rm\n- replace / rp\n\n- clear (clear screen)\n- exit\n>: ").strip().lower()

    # check if mode is avilable
    if mode not in ['print','add','remove','replace','clear','p','a','rm','rp','exit']:
        print("invald option.")
        time.sleep(1)
        clear()
        continue

    # create json store file of not exists
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w', encoding='utf-8') as crt:
            json.dump({}, crt, indent=4, ensure_ascii=False)
    # check if file is empty
    else:
        try:
            with open(JSON_FILE, 'r+', encoding='utf-8') as is_empty:
                if is_empty.read().strip() == '':
                    json.dump({}, is_empty, indent=4, ensure_ascii=False)
        except json.decoder.JSONDecodeError:
            print("json file has problem!\nfix it please.")
            exit(1)

    # check formated file is correct
    with open(JSON_FILE, 'r', encoding='utf-8') as j:
        try:
            jdb = json.load(j)
        except json.decoder.JSONDecodeError:
            print("json file has problem!\nfix it please.")
            exit(1)

    # print mode
    if mode == 'print' or mode == 'p':
        # if not data in file
        if not jdb:
            print("nothing to print.")
            time.sleep(1)
            clear()
            continue
        # print file
        else:
            clear()
            page = 2
            print("=" * 50, '\n')
            print(f"\t\t\tPage {page}\n".expandtabs(7))
            print("=" * 50)
            for count, wordkv in enumerate(jdb):
                count += 1
                if (count) % 6 == 0:
                    page += 1
                    print("=" * 50, '\n')
                    print(f"\t\t\tPage {page}\n".expandtabs(7))
                    print("=" * 50)
                    print(f"{str(count).zfill(4):<4} - \t{wordkv:<5} \t\t\t\t====> \t\t\t\t\t\t{jdb[wordkv]}".expandtabs(2))
                    continue
                else:
                    print(f"{str(count).zfill(4):<4} - \t{wordkv:<5} \t\t\t\t====> \t\t\t\t\t\t{jdb[wordkv]}".expandtabs(2))
            print("=" * 50)
            print(f"Total {page-1} pages.")
            input("\npress enter to continue...")
            clear()
            continue
    # add mode
    elif mode == 'add' or mode == 'a':
        # english word
        enwrd = input("Enter English Word: ").strip().capitalize()
        # arabic word
        arwrd = input("Enter Arabic Word: ").strip().capitalize()

        # check if word is exist
        try:
            # ask if replace if word exist
            print(f"The English word '{enwrd}' is aleady exist with '{jdb[enwrd]}' Arabic word.\ndo you want replace it with '{arwrd}'? (y/n)")
            arep = input(": ").strip().lower()
            # loop if ans not correct
            while arep not in ['y','n']:
                print("invlid option.\nplease 'y' or 'n'")
                arep = input(": ").strip().lower()
            # replace if ans is yes (y)
            if arep == 'y':
                jdb[enwrd] = arwrd
                print(f"a '{enwrd}' has been replased to '{arwrd}' .")
            # skip if ans is no (n)
            elif arep == 'n':
                print("skipping...")
                time.sleep(0.5)
                continue

        # if word not exist, add word to dict
        except KeyError:
            jdb[enwrd] = arwrd
        # add new dict to json file with checking
        try:
            with open(JSON_FILE, 'w', encoding='utf-8') as j:
                json.dump(jdb, j, indent=4, ensure_ascii=False)
            print("seccesful added.")
        except FileNotFoundError:
            print(f"Error! file: '{JSON_FILE}' not found.")
            exit(1)
                
    # replace mode
    elif mode == 'replace' or mode == 'rp':
        clear()
        print("Words:\n")
        for i in jdb:
            print(f"{i} => {jdb[i]}")
        # grab replace word from user
        orep = input("\nChoose a word (english) do you want to replace: ").strip().capitalize()
        # if word not found in dict
        while orep not in jdb:
            print(f"'{orep}' not found.")
            orep = input(f"Please enter a exist english word: ").strip().capitalize()
        # new word to replace with it
        print(f"replace (English) '{orep}' to: ")
        # leave it
        print("(you can leave it as it is with type: 'LEAVEIT')")
        nrep = input('>: ').strip().capitalize()

        # leave it if LEAVEIT
        if nrep.upper() == 'LEAVEIT':
            print(f"OK! leaving it.")
            nrep = orep

        # replace arabic word
        print(f"Enter a new Arabic word for '{nrep}'")
        # print a old arabic word
        print(f"old word: {jdb[orep]}")
        # leave it
        print("(you can leave it as it is with type: 'LEAVEIT')")
        anrep = input('>: ').strip().lower()

        # leave it if LEAVEIT
        if anrep.upper() == 'LEAVEIT':
            print(f"OK! leaving it.")
            anrep = jdb[orep]

        if not replace_key(jdb, orep, nrep):
            print("Unknown Error")
            exit(1)
        else:
            jdb[nrep] = anrep

        with open(JSON_FILE, 'w', encoding='utf-8') as j:
            json.dump(jdb, j, indent=4, ensure_ascii=False)

    elif mode == 'clear':
        clear()
        continue
    elif mode == 'exit':
        exit(0)

    with open(JSON_FILE, 'w', encoding='utf-8') as j:
        json.dump(jdb, j, indent=4, ensure_ascii=False)

