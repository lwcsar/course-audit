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
import lib.input as datainput
inport lib.database as db
import os
import argparse

#Global Variables
default_csv_path = os.path.dirname(os.path.realpath(__file__)) + '\CourseMap.csv'

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
    parser.add_argument('--input', help='Import CSV file to application', const="", type=str)
    parser.add_argument('--outputdir', help='Directory to output PDF files', type=str)
    parser.add_argument('--grade', help='The grade to process or all', type=str)

    args = parser.parse_args()
    return args

#----#
#Main#
#----#
args = arguments()
if args.version:
    print(datainput.get_version())
    exit()
if args.debug:
    pass # TODO: Output debugging information
if args.init:
    # QUESTION: Do we allow for alternate locations for the database file? If so, we need a new cmd line argument.
    # QUESTION: If we allow an alternate db location, we should pass that location into our create function.
    database.create_sqlite_tables()
if args.input:
    # TODO: Determine the full path of the input filename and pass that into our method
    if(args.input == ''):
        datainput.import_csv(default_csv_path)
    else:
        datainput.import_csv(args.input)
if args.outputdir:
    pass # TODO: Set output Directory
if args.grade:
    pass # TODO: Set grade to process
