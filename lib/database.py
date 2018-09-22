import os
import sqlite3
import logging

# TODO: Add function definition comments
def sqlite_connect(db):
    # TODO: Check for default sqlite database. if not exist, error and exit
    # QUESTION: Do we auto-create the database and schema if the database does not exist? If so, we just call our create_sqlite_tables method.

    # Connect to DB and return
    conn = sqlite3.connect(db)
    return conn


# TODO: Add function definition comments
def create_sqlite_tables():
    sqlfile = open("doc/sql.txt", "r")
    sqltxt = sqlfile.read()
    c.executescript(sqltxt)
    c.commit()


# TODO: Add function definition comments
def create_course(row):
    logging.debug(row['Course']+' '+row['Department']+' '+row['Grade Level']+' '+row['Credits'])
    # TODO: Complete the database method.


# TODO: Add function definition comments
def create_student(row):
    (last_name, first_name) = row['LastName, FirstName'].split(',')
    logging.debug(row['Student ID (System)']+','+
        last_name.strip()+','+first_name.strip()+','+row['Grade Level'])
    # TODO: Complete the database method.

# TODO: Add function definition comments
def create_student_course(student_id,course_id,credits):
    logging.debug(student_id+' '+course_id+' '+credits)
    # TODO: Complete the database method.


# When our module is loaded, connect to the database and create a cursor
# object so we can use the connection.
conn = sqlite_connect(db)
c = conn.cursor()
