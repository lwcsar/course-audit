import os
import csv
import sys
import sqlite3
import logging
from . import database


"""Input Module

This module will read and process input data taken from CSV, ODBC, or other
input sources. Processed inputs will be stored in a database for later use.

"""

# TODO: Switch all functions to snake_case naming convention
"""Process a CSV file, turning into a SQLite database.

Keyword arguments:
    reader - a csv reader that translates the csv into usable data.

Return values:
    None.
"""
def processCSV(reader):
    last_id = 0

    """Walk through each line in the CSV file reader and process them
    one by one based on our processing rules.

    CSV Processing Rules:
        if grade level 1 < 9: ignore
        if credits == 0: discard from user
        create courses in SQL for everything in grade 9+
        Save First and Last names separate so the CSV field must be split.
        Discard the Status and Year columns.
    """
    for row in reader:
        """Skip all lines defining non-high school courses."""
        if int(row['Grade Level 1']) < 9:
            continue

        """Create the course"""
        course_id = database.create_course(row)
        if row['Course'].find('Principles'):
            logging.debug(row['Course']+' '+row['Department']+' '+row['Grade Level']+' '+row['Credits'])


        """Skip if zero credits were earned."""
        # TODO: check for zero credit and ignore
        if float(row['Credits']) == 0:
            continue

        """Create our student record"""
        # TODO: Add student to database
        if int(row['Student ID (System)']) != last_id:
            # Insert the new user into the DB.
            student_id = database.create_student(row)
            last_id = int(row['Student ID (System)'])

        """Associate the course with the student and store that."""
        # TODO: Add student/course association in db.
        database.create_student_course(student_id,course_id,float(row['Credits']))


"""Import a CSV file into the application.

Keyword arguments:
    filename - a string containing the full path to the CSV file to be imported.

Return values:
    None.
"""
def import_csv(filename):
    # TODO: 1) Make sure the file exists
    # TODO: 2) If not exist, error and exit.
    # TODO: 3) Open and process the file. The original example may not work as shown.
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        processCSV(csvreader)


"""Returns the Applications current distribute version.

Keyword arguments:
    None.

Return values:
    None.
"""
def get_version():
    return "0.1.0"
