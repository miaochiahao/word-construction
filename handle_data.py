# -*- coding: UTF-8 -*-
import sqlite3
from mdict_query import *
# filename = "20000_Noun.txt"
# WORD_TYPE = 'n.'
mdx_builder = IndexBuilder("colins.mdx")
PAGE_NUM = 5

def insert_data(filename, word_type):
    f = open(filename, "r")
    conn = sqlite3.connect('database.db')
    conn.text_factory = str
    c = conn.cursor()
    print '[*] Inserting Data...'
    for line in f.readlines():
        if len(line) == PAGE_NUM or line == '\n':
            continue
        # print line
        words = line.strip().split()
        for i in range(0,len(words)-1,2):
            # print words[i] + '  ' + words[i+1]
            exp = mdx_builder.mdx_lookup(words[i+1])
            if exp == []:
                exp = "Not Found"
            else:
                exp = exp[0]
            d = (words[i],words[i+1],word_type, exp)
            # print d
            c.execute("INSERT INTO WORDS (FREQUENCY,WORD,TYPE, EXPLANATION) \
            VALUES (?,?,?,?)", d)
    conn.commit()
    conn.close()
    print '[+] Data of %s Insert Complete!' % filename



def create_database():
    conn = sqlite3.connect('database.db')
    print '[+] Database Connected!'
    c = conn.cursor()
    c.execute('''CREATE TABLE WORDS
                 (ID integer PRIMARY KEY AUTOINCREMENT,
                 FREQUENCY INT NOT NULL,
                 WORD CHAR(20) NOT NULL,
                 TYPE CHAR(20) NOT NULL,
                 EXPLANATION TEXT NOT NULL,
                 FLAG INT DEFAULT 0,
                 APPEAREANCE DATE );''')
    conn.commit()
    conn.close()
    print '[+] Table Created!'

if __name__ == '__main__':
    create_database()
    insert_data('20000_Noun.txt', 'n')
    insert_data('20000_Adjective.txt', 'adj')
    insert_data('20000_Adverb.txt', 'adv')
    # insert_data('20000_Func.txt', 'func')
    insert_data('20000_Verb.txt', 'v')
