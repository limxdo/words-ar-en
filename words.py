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
    # error
    else:
        print("Unknown clear command for this system.")

clear()

def replace_key(dct, pagenum, old_key, new_key):
    try:
        dct[pagenum][new_key] = dct[pagenum].pop(old_key)
        return True
    except KeyError:
        return False

def dgt_chk(num):
    if str(num).isdigit():
        return str(num)
    else:
        return False

# sort a pages numbers
def sort_numeric_keys(dct): 
    sorted_data = dict(sorted(dct.items(), key=lambda x: int(x[0])))
    return sorted_data

# main loop
while True:
    # user input for mode
    mode = input("choose mode:\n- print / p:\n- add / a\n- remove / rm\n- replace / rp\n\n- clear (clear screen)\n- exit\n>: ").strip().lower()

    if not mode:
        print('input is empty.')
        time.sleep(0.5)
        clear()
        continue

    # check if mode is avilable
    if mode not in {'print','add','remove','replace','clear','p','a','rm','rp','exit'}:
        print("invald option.")
        time.sleep(0.5)
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

    # load json file and check formated file is correct
    with open(JSON_FILE, 'r', encoding='utf-8') as j:
        try:
            jdb = json.load(j)
            jdb = sort_numeric_keys(jdb)
        except json.decoder.JSONDecodeError:
            print("json file has problem!\nfix it please.")
            exit(1)

    with open(JSON_FILE, 'w', encoding='utf-8') as j:
        try:
            jdb = sort_numeric_keys(jdb)
            json.dump(jdb, j, indent=4, ensure_ascii=False)
        except:
            print("Unknown Error")
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
            for page in jdb:
                print("=" * 50, '\n')
                print(f"\t\t\tPage {page}\n".expandtabs(7))
                print("=" * 50)
                for count, kv in enumerate(jdb[page]):
                    count += 1
                    print(f"{str(count).zfill(2):<2} - {kv:<5} \t\t\t\t\t\t \t\t\t\t\t\t{jdb[page][kv]}".expandtabs(2))
                    # print(f"{str(count).zfill(4):<4} - \t{kv:<5} \t\t\t\t====> \t\t\t\t\t\t{jdb[page][kv]}".expandtabs(2))
            total_words = 0
            print("=" * 50)
            print(f"Total {len(jdb)} pages.")
            for i in jdb:
                for x in jdb[i]:
                    total_words += 1
            print(f"Total {total_words} words.")
            input("\npress enter to continue...")
            clear()
            continue

    # add mode
    elif mode == 'add' or mode == 'a':
        clear()
        print("What do you want to add? (1/2)\n\n1 - words\n2 - page\n")
        porw = input(">: ").strip()
        bang = 0
        while porw not in {'1','2'}:
            porw = input(f"enter '1' or '2' {'!'*bang}: ")
            bang += 1
        if porw == '1':
                # print exist pages
                print('Exist Pages: ')
                print(tuple(int(i) for i in jdb))
                print('\n')
                # page number
                print("(You can enter new page number)")
                page = dgt_chk(input("Enter Page Number: "))
                bang = 0
                while not dgt_chk(page):
                    page = dgt_chk(input(f"Enter Number{'!'*bang}: "))
                    bang += 1

                if page not in jdb:
                    jdb[page] = {} 

                # english word
                enwrd = input("Enter English Word: ").strip().capitalize()
                # check
                tmp = True
                bangn = 1
                while not enwrd:
                    if tmp:
                        print("input is empty").strip().capitalize()
                        enwrd = input("Please Enter English Word: ").strip().capitalize()
                    else:
                        enwrd = input(f"English Word{'!'*bangn}: ").strip().capitalize()
                        bangn += 1
                    tmp = False

                # arabic word
                arwrd = input("Enter Arabic Word: ").strip().capitalize()
                # check
                tmp = True
                bangn = 1
                while not arwrd:
                    if tmp:
                        print("input is empty")
                        arwrd = input("Please Enter Arabic Word: ").strip().capitalize()
                    else:
                        arwrd = input(f"Arabic Word{'!'*bangn}: ").strip().capitalize()
                        bangn += 1
                    tmp = False

                eexist = False
                pew = None # 'pew' => page exist word (:
                for tpage in jdb:
                    if enwrd in jdb[tpage]:
                        eexist = True
                        pew = tpage

                # check if word is exist
                if eexist:
                    # if english & arabic word is exist
                    if jdb[pew][enwrd] == arwrd:
                        print(f"('{enwrd}': '{arwrd}') is already exist in page {pew}.")
                        input("\npress enter to continue...")
                        clear()
                        continue
                    # ask if replace it if word is exist
                    print(f"The English word '{enwrd}' is aleady exist in page {pew} with '{jdb[pew][enwrd]}' Arabic word.\ndo you want replace it with '{arwrd}' in page {pew}? (y/n)")
                    arep = input(">: ").strip().lower()
                    # loop if ans not correct
                    tmp = True
                    bang = 1
                    while arep not in {'y','n'}:
                        if tmp:
                            print("invlid option.\nplease 'y' or 'n'")
                            arep = input(">: ").strip().lower()
                        else:
                            arep = input(f"'y' or 'n'{'!'*bang}: ").strip().lower()
                            bang += 1
                        tmp = False
                    # replace if ans is yes (y)
                    if arep == 'y':
                        jdb[pew][enwrd] = arwrd
                        print(f"a '{enwrd}' has been replased to '{arwrd}' .")
                    # skip if ans is no (n)
                    elif arep == 'n':
                        print("skipping...")
                        time.sleep(0.5)
                        continue

                # if word not exist, add word to dict
                else:
                    jdb[page][enwrd] = arwrd
                # sort keys
                sort_numeric_keys(jdb)
                # add new dict to json file with checking
                try:
                    with open(JSON_FILE, 'w', encoding='utf-8') as j:
                        json.dump(jdb, j, indent=4, ensure_ascii=False)
                except FileNotFoundError:
                    print(f"Error! file: '{JSON_FILE}' not found.")
                    exit(1)
        elif porw == '2':
            print(f"Exists pages: (dont choose exist page)\n{tuple(i for i in jdb)}\n")
            npage = input("Enter page number you want do add: ").strip()
            
            nbang = 0
            ebang = 0
            tmp = True
            while npage in jdb or not npage.isdigit():
                if not npage.isdigit():
                    npage = input(f"enter number{'!'*nbang}: ").strip()
                    nbang += 1
                    ebang = 0
                    tmp = True
                else:
                    nbang = 0
                    if tmp:
                        print(f"page {npage} already exists, please choose another.")
                        npage = input(">: ").strip()
                        nbang = 0
                        ebang = 0
                    else:
                        npage = input(f"enter unexsist page{'!'*ebang}: ").strip()
                        ebang += 1
                        if not npage.isdigit():
                            continue
                    tmp = False

            jdb[npage] = {}
            try:
                jdb = sort_numeric_keys(jdb)
                with open(JSON_FILE, 'w', encoding='utf-8') as j:
                    json.dump(jdb, j, indent=4, ensure_ascii=False)
                print(f"\nPage {npage} has been added to file.")
                input("\npress enter to continue...")
                clear()
                continue
            except json.decoder.JSONDecodeError:
                print("dictionary data has problem!")
                exit(1)
            except:
                print("Unknown Error!")
                exit(1)
                
    # replace mode
    elif mode == 'replace' or mode == 'rp':
        clear()
        print("\tWords:\n".expandtabs(11))
        print('-' * 30)
        for tpage in jdb:
            print(f"Page {tpage}:\n")
            for kv in jdb[tpage]:
                if not kv:
                    print("Empty")
                print(f"{kv}\t{jdb[tpage][kv]}")
            print('-' * 30,end='')
            print('\n',end='')
        
        # page number
        bang = 0
        page = input("\nEnter Page Number: ")
        while page not in jdb:
            if not dgt_chk(page):
                page = input(f"Please Enter Number{'!'*bang}: ")
                bang += 1
            else:
                print(f"page '{page}' not found.")
                page = input("please enter a exist page number: ")
                bang = 0


        # grab replace word from user
        orep = input("\nChoose a word (english) do you want to replace: ").strip().capitalize()
        # if word not found in dict
        ebang = 0
        nbang = 0
        while orep not in jdb[page]:
            if not orep:
                print(f"input is empty{'!'*ebang}")
                orep = input(f"Please enter a exist english word: ").strip().capitalize()
                ebang += 1
                nbang = 0
            else:
                print(f"'{orep}' not found in page {page} {'!'*nbang}")
                orep = input(f"Please enter a exist english word: ").strip().capitalize()
                nbang += 1
                ebang = 0
        # new word to replace with it
        print(f"replace (English) '{orep}' in page {page} to: ")
        # leave it
        print("(you can leave it as it is with type: 'LEAVEIT')")
        nrep = input('>: ').strip().capitalize()
        
        # # not empty
        # bang = 0
        # while not nrep:
        #     print(f"replace (English) '{orep}' to{'!'*bang}: ")
        #     nrep = input('>: ').strip().capitalize()
        #     

        # checking
        tmp = True
        bang = 0
        while not nrep:
            if tmp:
                print("input is empty")
                nrep = input(f"please enter word to replace (English): '{orep}' to: ").strip().capitalize()
            else:
                nrep = (f"replace (English) '{orep}' to{'!'*bang}: ")
                bang += 1
            tmp = False

        # leave it if LEAVEIT
        if nrep.upper() == 'LEAVEIT':
            print(f"OK! leaving it.")
            nrep = orep

        # replace arabic word
        print(f"Enter a new Arabic word for '{nrep}'")
        # print a old arabic word
        print(f"old word: {jdb[page][orep]}")
        # leave it
        print("(you can leave it as it is with type: 'LEAVEIT')")
        anrep = input('>: ').strip().capitalize()

        # checking
        tmp = True
        bang = 0
        while not anrep:
            if tmp:
                print("input is space")
                anrep = input(f"please enter a new Arabic word for '{nrep}': ").strip().capitalize()
            else:
                anrep = input(f"arabic word for {nrep}{'!'*bang}").strip().capitalize()
                bang += 1
            tmp = False

        # leave it if LEAVEIT
        if anrep.upper() == 'LEAVEIT':
            print(f"OK! leaving it.")
            anrep = jdb[page][orep]

        if not replace_key(jdb, page, orep, nrep):
            print("Unknown Error")
            exit(1)
        else:
            jdb[page][nrep] = anrep

        with open(JSON_FILE, 'w', encoding='utf-8') as j:
            json.dump(jdb, j, indent=4, ensure_ascii=False)

    elif mode == 'remove' or mode == 'rm':
        # print words & pages
        clear()
        print("\tWords / Pages:\n")
        print('-' * 30)
        for tpage in jdb:
            print(f"Page {tpage}:\n")
            for kv in jdb[tpage]:
                if not kv:
                    print("Empty")
                print(f"{kv}\t{jdb[tpage][kv]}")
            print('-' * 30,end='')
            print('\n',end='')
        # print('-' * 30)

        # choose pages or words
        print("\nremove pages or words?")
        print("1 - pages\n2 - words")
        rmmode = input(">: ").strip().lower()
        bang = 0
        while not rmmode in {'1','2'}:
            rmmode = input(f"please choose (1/2){'!'*bang}: ").strip().lower()
            bang += 1

        if rmmode == '1':
            pages = []
            print("avilable pages: ")
            for i in jdb:
                pages.append(i)
            print(tuple(int(i) for i in pages))
            dpage = input('\nchoose page you want to delete: ').strip()
            bang = 0
            tmp = True
            while dpage not in set(pages):
                if tmp:
                    dpage = input(f"please choose page you want to delete from list: \n{tuple([int(i) for i in pages])}: ").strip()
                else:
                    dpage = input(f"choose avilable page{'!'*bang}: ").strip()
                    bang += 1
                tmp = False
            try:
                del jdb[dpage]
                with open(JSON_FILE, 'w', encoding='utf-8') as j:
                    json.dump(jdb, j, indent=4, ensure_ascii=False)
                print(f"page {dpage} has been removed from file.")
                input("\npress enter to continue...")
                clear()
                continue
            except json.decoder.JSONDecodeError:
                print("dictionary data has problem!")
                exit(1)
            except:
                print("Unknown Error!")
                exit(1)

        elif rmmode == '2':
            pages = []
            for i in jdb:
                pages.append(i)
            print("Enter page number that contains the word you want to delete")
            pagetw = input(">: ").strip()
            bang = 0
            tmp = True
            while pagetw not in set(pages):
                if tmp:
                    pagetw = input(f"please choose page number contains the word you want to delete from list: \n{tuple([int(i) for i in pages])}: ").strip()
                else:
                    pagetw = input(f"choose exist page{'!'*bang}: ").strip()
                    bang += 1
                tmp = False
            pagetwrd = input(f"Enter word do you want delete from page {pagetw} (English): ").strip().capitalize()
            bang = 0
            tmp = True
            while pagetwrd not in jdb[pagetw]:
                if tmp:
                    pagetwrd = input(f"please enter an existing word in {pagetw}: ").strip().capitalize()
                else:
                    pagetwrd = input(f"enter existing word{'!'*bang}: ").strip().capitalize()
                    bang += 1
                tmp = False
            try:
                del jdb[pagetw][pagetwrd]
                with open(JSON_FILE, 'w', encoding='utf-8') as j:
                    json.dump(jdb, j, indent=4, ensure_ascii=False)
                print(f"word {pagetwrd} in page {pagetw} has been removed from file.")
                input("\npress enter to continue...")
                clear()
                continue
            except json.decoder.JSONDecodeError:
                print("dictionary data has problem!")
                exit(1)
            except:
                print("Unknown Error!")
                exit(1)

    elif mode == 'clear':
        clear()
        continue
    elif mode == 'exit':
        exit(0)

    with open(JSON_FILE, 'w', encoding='utf-8') as j:
        json.dump(jdb, j, indent=4, ensure_ascii=False)

