#!/usr/bin/python
from multiprocessing import Process, Lock
import MySQLdb as mysql
from MySQLdb import escape_string as escape
from passlib.hash import pbkdf2_sha256
from passlib.hash import md5_crypt
import psutil
import sys
import time


# Get the chars we will be using.
chars = []
for i in range(0,255):
    chars.append(str(chr(i)))


def generateRange(*args):
    global chars
    db = mysql.connect(host='localhost',db='rainbow')
    cursor = db.cursor()

    # Some settings that this function uses. Will expose these in the future but not now.
    length = (len(args) -1)
    global charRangeStart
    global charRangeEnd
    odometer = [] # odometer.

    # The odometer works like an analog milage odometer. It's a list of integers.
    # It rolls over when a left-ern integer reaches the charRangeEnd, and rolls over to charRangeStart


    # For multi-threading, this line must be used.
    odometer = list(args)
    # For regular function calling, this line must be used.
    #odometer = list(starting_chars[0])



    # Here's where we get our hands dirty.
    done = False
    positionOne = length
    positionTwo = length - 1
    

    while not done:
        text = str('')
        # This loop is not special, it just builds the dictionary. A needed but un-interesting piece of this program.
        for i in xrange(len(odometer) - 1,-1,-1):
            text = text + chars[odometer[i]]

        text = text.strip()
        if text != '' and text != None:
            print text
            #hash_pbkdf2_sha256 = pbkdf2_sha256.hash(text)
            md5 = md5_crypt.hash(text)
            sql = "INSERT IGNORE INTO rainbow(md5,text) VALUES('" + escape(md5) + "','" + escape(text) + "')"
            try:
                cursor.execute(sql)
                db.commit()
            except:
                pass

        # Here, we add to our TRUE iterator.
        odometer[positionOne] = odometer[positionOne] + 1

        # Here, we process what we need after we have iterated. Just like an analog odometer
        for i in xrange(positionOne,-1,-1):

            if odometer[i] > charRangeEnd:
                odometer[i] = charRangeStart
                if i != 0 and i != positionTwo:
                    odometer[i - 1] = odometer[i - 1] + 1
                    continue
                else:
                    odometer[i] = charRangeEnd
                    done = True
            else:
                break

    cursor.close()
    db.close()
    return



def cpuWrangler():
    while True:
        time.sleep(0.01)
        cpu = psutil.cpu_percent()
        if cpu < 92:
            break



charRangeStart = 32
charRangeEnd = 126
jobs = []

for a in range(charRangeStart,charRangeEnd):
    for b in range(charRangeStart,charRangeEnd):
        for c in range(charRangeStart,charRangeEnd):
            for d in range(charRangeStart,charRangeEnd):
                for e in range(charRangeStart,charRangeEnd):
                    for f in range(charRangeStart,charRangeEnd):
                        for g in range(charRangeStart,charRangeEnd):

                            theArgs = [a,b,c,d,e,f,g,charRangeStart,charRangeStart]
                            p = Process(target=generateRange, args=theArgs)
                            jobs.append(p)
                            jobs[(len(jobs) - 1)].start()
                            cpuWrangler()




for job in jobs:
    job.join()

