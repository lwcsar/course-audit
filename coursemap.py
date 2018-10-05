import lib.input as datainput
import lib.database as db
import os
import argparse
import logging

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
default_csv_path = os.path.dirname(os.path.realpath(__file__)) + '\CourseMap.csv'
default_database_directory = os.path.dirname(os.path.realpath(__file__)) + 'doc/'

"""Returns the arguments run on a command line process.

Keyword arguments:
    None.

Return values:
    args- the arguments that are called.
"""
def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--version', help='Print out the current version and exit.', action='store_true')
    parser.add_argument('-d','--debug', help='Print out debugging information.', action='store_true')
    parser.add_argument('--init', help='Initialize our SQLite database.', action='store_true')
    parser.add_argument('--input', help='Import CSV file to application. Follow with file path',nargs='?', const='Default', type=str)
    parser.add_argument('--outputdir', help='Directory to output PDF files', type=str)
    parser.add_argument('--dbdir', help='Directory to store the database file', type=str)
    parser.add_argument('--grade', help='The grade to process or all', type=str)

    args = parser.parse_args()
    return args

"""Runs the Arguments using the args from argparse module.

Keyword arguments:
    args- the arguments that are called from the arguments() function.

Return values:
    args- the arguments that are called.
"""
def RunArguments():
    if args.debug:
        #Set up logger
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
        pass
    else:
        logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s')
        pass
    if args.version:
        print(datainput.get_version())
        exit()
    if args.dbdir:
        default_database_directory = args.dbdir
        pass
    if args.init:
        database.create_sqlite_tables(default_database_directory)
    if args.input:
        if(args.input == 'Default'):
            datainput.import_csv(default_csv_path)
        else:
            datainput.import_csv(args.input)
    if args.outputdir:
        pass # TODO: Set output Directory
    if args.grade:
        pass # TODO: Set grade to process

#----#
#Main#
#----#
args = arguments() #Find Arguments
RunArguments() #Run Arguments
