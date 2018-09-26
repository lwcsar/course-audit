import csv
import sqlite3
import os

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
        if int(row['Grade Level 1']) < 9:
            continue

        """Create the course"""
        database.create_course(row)

        """Skip if zero credits were earned."""
        # TODO: check for zero credit and ignore

        """Create our student record"""
        # TODO: Add student to database

        """Associate the course with the student and store that."""
        # TODO: Add student/course association in db.



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
    if os.path.isfile(filename)
    with open(os.path.dirname(os.path.realpath(__file__)) + '\..\CourseMap.csv', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        processCSV(csvreader)

"""Returns the Applications current distribute version.

Keyword arguments:
    None.

Return values:
    None.
"""
def get_version():
    # Tried coding this in. Works locally, but requires git to be installed. We could use a module such as pygit, but may need to be changed on release
    return "0.1.0"
