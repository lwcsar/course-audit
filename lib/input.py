import csv
import sqlite3
import os
import logging

"""Input Module

This module will read and process input data taken from CSV, ODBC, or other
input sources. Processed inputs will be stored in a database for later use.

"""

"""Process a CSV file, turning into a SQLite database.

Keyword arguments:
    reader - a csv reader that translates the csv into usable data.

Return values:
    None.
"""
def process_csv(reader):
    firstID = 0

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
        """If the pre 9th grade class doesn't have credits it is counted as high school"""
        if int(row['Grade Level 1']) < 9 and int(row['Credits']) != 0:
            continue

        """Create the course"""
        database.create_course(row)

        """Skip if zero credits were earned."""
        if int(row['Credits']) != 0:
            continue

        """Create our student record"""
        database.create_student(row)

        """Associate the course with the student and store that."""
        database.create_student_course(int(row['Student ID (System)']),int(row['Course']),int(row['Credits']))



"""Import a CSV file into the application.

Keyword arguments:
    filename - a string containing the full path to the CSV file to be imported.

Return values:
    None.
"""
def import_csv(filename):
    if os.path.isfile(filename):
        with open(filename, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            process_csv(csvreader)
    else:
        logging.error("File \"" + filename + "\" does not exist")
        exit()

"""Returns the Applications current distribute version.

Keyword arguments:
    None.

Return values:
    None.
"""
def get_version():
    return "0.1.0"
