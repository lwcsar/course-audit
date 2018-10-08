import os
import csv
import sys
import sqlite3
import logging
from .database_schema import Base, Student, Course

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

"""Input Module

This module will read and process input data taken from CSV, ODBC, or other
input sources. Processed inputs will be stored in a database for later use.

"""
class Input():

    def __init__(self, session):
        self.session = session


    def course_handler(self, data):
        """Process course creation for input data."""

        """Skip all lines defining non-high school courses."""
        if int(data['Grade Level 1']) < 9:
            return None

        try:
            """Test if the course exists before attempting to create the course."""
            course = self.session.query(Course).filter(
                    Course.course_name == data['Course']).filter(
                    Course.course_department == data['Department']).filter(
                    Course.course_grade_level == data['Grade Level 1']).one()
        except NoResultFound:
            """Create the course"""
            course = Course(course_name=data['Course'],
                course_department=data['Department'],
                course_grade_level=data['Grade Level 1'],
                course_credit=data['Credits'])
            self.session.add(course)
            logging.debug(data['Course']+' '+data['Department']+' '+data['Grade Level 1']+' '+data['Credits'])

        return course


    def student_handler(self, data):
        """Process student creation for input data."""

        """Skip if zero credits were earned."""
        if float(data['Credits']) == 0:
            return None

        student_id = int(data['Student ID (System)'])
        try:
            """Test if the student exists before attempting to create the student."""
            student = self.session.query(Student).filter(Student.id == student_id).one()
        except NoResultFound:
            """Create our student record"""
            (last_name, first_name) = data['LastName, FirstName'].split(',')
            logging.critical(str(student_id)+','+first_name.strip())
            # Insert the new user into the DB.
            student = Student(id=student_id, last_name=last_name,
                first_name=first_name, grade_level=data['Grade Level'])
            student_id = self.session.add(student)

        return student


    def process(self, reader):
        """Process a CSV file, turning into a SQLite database.

        Keyword arguments:
            reader - a csv reader that translates the csv into usable data.

        Return values:
            None.
        """

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

            try:
                logging.debug("Process Course")
                course = self.course_handler(row)
                logging.debug("Process Student")
                student = self.student_handler(row)
                if student and course:
                    logging.debug("Connect Course and Student")
                    course.students.extend([student]) # Add the student to the course
                self.session.commit()
            except:
                self.session.rollback()
                raise
            # finally:
            #     session.close()


    def csv_file(self, filename):
        """Import a CSV file into the application.

        Keyword arguments:
            filename - a string containing the full path to the CSV file to be imported.

        Return values:
            None.
        """
        if os.path.isfile(filename):
            with open(filename, newline='') as csvfile:
                csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
                self.process(csvreader)
        else:
            logging.error("File does not exist: " + filename)
            exit()


"""Returns the Applications current distribute version.

Keyword arguments:
    None.

Return values:
    None.
"""
def get_version():
    return "0.1.0"
