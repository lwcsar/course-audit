import os
import sys
import argparse
import logging
from lib.input import Input
from lib.process import Process
from lib.database import Database
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
    parser.add_argument('-d','--debug', help='Print out debugging information.', action='store_true')
    parser.add_argument('--init', help='Initialize our SQLite database.', action='store_true')
    parser.add_argument('--input', help='Import CSV file to application. Follow with file path',nargs='?', const='Default', type=str)
    parser.add_argument('--outputdir', help='Directory to output PDF files', type=str)
    parser.add_argument('--DataBasedir', help='Directory to store the database file', type=str)
    parser.add_argument('--grade', help='The grade to process or all', type=str)

    args = parser.parse_args()
    return args


def run(session, default_database_directory):
    """Runs the application using the given arguments.

    Keyword arguments:
        args- the arguments that are called from the arguments() function.

    Return values:
        None.
    """
    if args.version:
        #from lib.database_schema import Base, Setting
        #ver = session.query(Setting).all() #.filter(Setting.key == 'version').one()
        #print("Version: "+ver.value)
        # TODO: Fix Version from settings
        print(myInput.get_version())
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
        Database.create_default_settings()
    if args.input:
        if args.input == 'Default':
            myinput.csv_file(default_csv_file)
        else:
            myinput.csv_file(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), str(args.input))
                )
    if args.outputdir:
        pass # TODO: Set output Directory


#----#
#Main#
#----#
if __name__ == '__main__':
    args = arguments() #Find Arguments
    Database = Database(default_database_directory)
    session = Database.session()
    myInput = Input(session)
    myProcess = Process(session)
    run(session, default_database_directory) #Run the application
