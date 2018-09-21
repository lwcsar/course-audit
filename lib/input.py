import os
import sys
import csv
import sqlite3
import logging
from lib import database

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
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def process_csv(reader):
    last_id = 0

    for row in reader:
        # Skip all Elementary, MS, and JH courses and
        if int(row['Grade Level 1']) < 9:
            continue

        # Insert course information into DB.
        course_id = database.create_course(row)
        if row['Course'].find('Principles'):
            logging.debug(row['Course']+' '+row['Department']+' '+row['Grade Level']+' '+row['Credits'])


        # If credits == 0, save course to DB, but don't save to user record
        if float(row['Credits']) == 0:
            continue

        # Save our student to the database
        if int(row['Student ID (System)']) != last_id:
            # Insert the new user into the DB.
            student_id = database.create_student(row)
            last_id = int(row['Student ID (System)'])

        # Associate the student and the courses
        database.create_student_course(student_id,course_id,float(row['Credits']))



def import_csv(filename):
    logging.debug(filename)
    with open(filename, newline='') as csvfile:
      csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
      process_csv(csvreader)
