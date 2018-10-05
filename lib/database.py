import os
import sqlite3
import logging

"""Database Module

This module will handle the creation, reading, and manipulation of our SQLite Database

"""

"""Connect to the SQLite database.

Keyword arguments:
    db - The location of the database.

Return values:
    conn-the connection to the SQLite database.
"""
def sqlite_connect(db):
    # QUESTION: Do we auto-create the database and schema if the database does not exist? If so, we just call our create_sqlite_tables method.
    if os.path.isfile(db):
        # Connect to DB and return
        conn = sqlite3.connect(db)
        return conn
    else:
        logging.info("Creating database at this location:" + db)
        create_sqlite_tables(os.path.dirname(os.path.realpath(db)))
        exit()


"""Creates the SQLite database.

Keyword arguments:
    directory - The location of the database output.

Return values:
    none.
"""
def create_sqlite_tables(directory):
    sqlfile = open(directory + "sql.txt", "r")
    sqltxt = sqlfile.read()
    c.executescript(sqltxt)
    c.commit()


"""Create a course in the SQLite database.

Keyword arguments:
    row - Which row in the table to create the course.

Return values:
    none.
"""
def create_course(row):
    logging.debug(row['Course']+' '+row['Department']+' '+row['Grade Level']+' '+row['Credits'])
    # TODO: Complete the database method.


"""Create a student in the SQLite database.

Keyword arguments:
    row - Which row in the table to create the student.

Return values:
    none.
"""
def create_student(row):
    (last_name, first_name) = row['LastName, FirstName'].split(',')
    logging.debug(row['Student ID (System)']+','+
        last_name.strip()+','+first_name.strip()+','+row['Grade Level'])
    # TODO: Complete the database method.

"""Create a student course in the SQLite database that links the student and courses together.

Keyword arguments:
    row - Which row in the table to create the student course.

Return values:
    none.
"""
def create_student_course(student_id,course_id,credits):
    logging.debug(student_id+' '+course_id+' '+credits)
    # TODO: Complete the database method.


# When our module is loaded, connect to the database and create a cursor
# object so we can use the connection.
db = os.path.dirname(os.path.realpath(__file__)) + '/../' + 'coursemap.db'
conn = sqlite_connect(db)
c = conn.cursor()
