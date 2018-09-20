import csv
import sqlite3

''' IMPORT

This function will read in our CSV file, discard what is unnecessary, and
save the remaining data into a SQLite database.

CSV Processing Rules:
if grade level 1 < 9: discard
if credits == 0: discard from user
create courses in SQL for everything in grade 9+
Save First and Last names separate so the CSV field must be split.
Discard the Status and Year columns.

'''

def sqlite_connect():
    # Check for default sqlite database
    # if not exist, create
    #   import sql.txt into new database
    # Connect to DB and return
    conn = sqlite3.connect('coursemap.db')
    return conn

def createSqliteTables():
    sqlfile = open("doc/sql.txt", "r")
    sqltxt = sqlfile.read()
    conn = sqlite_connect()
    c = conn.cursor()
    c.executescript(sqltxt)

def processCSV(reader):
    firstID = 0

    for row in reader:
        # Skip all Elementary, MS, and JH courses and
        # Skip any courses with zero credits
        if int(row['Grade Level 1']) < 9 or float(row['Credits']) == 0:
            continue

        # debug

        # only print our first person for debugging
        if firstID == 0:
            print(row['Student ID (System)']+','+row['LastName, FirstName'])
            firstID = int(row['Student ID (System)'])

        if int(row['Student ID (System)']) != firstID:
            break

        print(row['Grade Level 1']+','+row['Course']+','+row['Credits'])
        # debug


def chooseCSV():
    with open("CourseMap.csv", newline='') as csvfile:
      csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
      processCSV(csvreader)
