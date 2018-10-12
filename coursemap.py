import os
import sys
import argparse
import logging
from lib.input import Input
from lib.process import Process
from lib.database import Database
from lib.output import OutputPDF
from logging.config import fileConfig

'''
This is the entrypoint into our application. This file will become largely
static once we establish some of the basics. We will bootstrap
the app and import the rest of the modules from here. Most work will be in
our custom modules.

--------------------

The application should operate in two distinct modes.
- With a GUI
- Without a GUI as a cli (command line interface)

We do this primarily for a few reasons.
1) As a CLI we can batch process with limited or no interaction.
2) We can easily test and debug the application without GUI distractions.

When we test the application in CLI mode, we should be able to specify various
arguments to operate the application from start to finish in one command or
run pieces of the application.

One of the first steps is to define what the command line arguments might be.
These arguments will be based on our application workflow, business requirements,
and some general best practices.

We whould utilize the argparse module to implement this functionality for us.
https://docs.python.org/3/library/argparse.html

Application arguments shall include the following:
-h, --help          to show a brief help message
-u, --userInterface run the user interface
-v, --version       display version information and exit.
-d, --debug         print out debugging information
--init              Initialize our SQLite database
--input=<file>      CSV file to import into the application
--outputdir=<dir>   Directory to output our PDF files
--grade=<grade>     The grade to process or 'all'
'''

#Global Variables
default_csv_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'CourseMap.csv')
default_database_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc")


def arguments():
    """Returns the arguments run on a command line process.

    Keyword arguments:
        None.

    Return values:
        args- the arguments that are called.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--version', help='Print out the current version and exit.', action='store_true')
    parser.add_argument('-u','--userInterface', help='Run the user interface', action='store_true')
    parser.add_argument('-d','--debug', help='Print out debugging information.', action='store_true')
    parser.add_argument('--init', help='Initialize our SQLite database.', action='store_true')
    parser.add_argument('--input', help='Import CSV file to application. Follow with file path', nargs='?', const='Default', type=str)
    parser.add_argument('--outputdir', help='Directory to output PDF files', type=str)
    parser.add_argument('--dbdir', help='Directory to store the database file', type=str)
    parser.add_argument('--all', help='Process all students', action='store_true')
    parser.add_argument('--grade', help='Process a grade', type=int)
    parser.add_argument('--student', help='Process a student', nargs=2, type=str)

    args = parser.parse_args(sys.argv[2:])
    return args


def run(session, default_database_directory):
    """Runs the application using the given arguments.

    Keyword arguments:
        args- the arguments that are called from the arguments() function.

    Return values:
        None.
    """
    if args.version:
        from lib.database_schema import Base, Setting
        print(myinput.get_version())
        exit()
    if args.userInterface:
        from lib.output import OutputUI
        OutputUI().run()
        exit()
    if args.debug:
        #Set up logger
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    else:
        logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s')
        pass
    if args.dbdir:
        default_database_directory = args.dbdir
        pass
    if args.init:
        import lib.database_schema as dbschema
        dbschema.run(default_database_directory)
        db.create_default_settings()
    if args.input:
        if args.input == 'Default':
            myinput.csv_file(default_csv_file)
        else:
            myinput.csv_file(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), str(args.input))
                )
    if args.outputdir:
        from lib.database_schema import Base, Setting
        Output = session.query(Setting).filter(Setting.id == 21).first()
        Output.value = args.outputdir
        session.commit()
        pass
    if args.all:
        from lib.database_schema import Base, Setting
        all_credits = myprocess.process_all(session)
        from lib.database_schema import Base, Student
        students = session.query(Student)
        students = students.order_by(Student.last_name)
        myoutput = OutputPDF(session.query(Setting).filter(Setting.id == 21).first().value + "\StudentReport")
        pos = 0
        for credits in all_credits:
            missing_credits = myprocess.missing_credits(session, credits)
            myoutput.addStudent(students[pos].first_name, students[pos].last_name, credits, missing_credits)
            pos += 1
        myoutput.savePDF()
    if args.grade:
        grade_credits = myprocess.process_grade(session, args.grade)
        pos = 0
        for credits in grade_credits:
            missing_credits = myprocess.missing_credits(session, credits)
            myoutput.addStudent(students[pos].first_name, students[pos].last_name, credits, missing_credits)
            pos += 1
    if args.student:
        credits = myprocess.process_student(session, args.student[0], args.student[1])
        missing_credits = myprocess.missing_credits(session, credits)
        myoutput.addStudent(args.student[0], args.student[1], credits, missing_credits)
        print(credits)
        print(missing_credits)



#----#
#Main#
#----#
if __name__ == '__main__':
    args = arguments() #Find Arguments
    db = Database(default_database_directory)
    session = db.session()
    myinput = Input(session)
    myprocess = Process(session)
    run(session, default_database_directory) #Run the application
