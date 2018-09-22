
"""
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
# QUESTION: ArgumentParser automatically generates a help file. Throws error if you try and do this yourself
-v, --version       display version information and exit.
-d, --debug         print out debugging information
--init              Initialize our SQLite database
--input=<file>      CSV file to import into the application
--outputdir=<dir>   Directory to output our PDF files
--grade=<grade>     The grade to process or 'all'
and...

'''
import os
import lib.input as datainput
import lib.database as database
import argparse

# TODO: Move this method and import to appropriate class
def get_version():
    # Tried coding this in. Works locally, but requires git to be installed. We could use a module such as pygit, but may need to be changed on release
    return "0.1.0"

def check_args(args=None):
    parser = argparse.ArgumentParser(description='Course Map report generating tool.')
    parser.add_argument('-v','--version', help='Print out the current version and exit.', action='store_true')
    parser.add_argument('-d','--debug', help='Print out debugging information.', action='store_true')
    parser.add_argument('--init', help='Initialize our SQLite database.', action='store_true')
    parser.add_argument('--input', nargs=1, type=str, default='CourseMap.csv', help='Initialize our SQLite database.')
    parser.add_argument('--outputdir', help='Directory to output PDF files', type=str)
    parser.add_argument('--grade', help='The grade to process or all', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    args = check_args()
    # TODO: Switch to numerous if statements. By using elif we can't process multiple arguments.
    if args.version:
        print(getVersion())
        exit()
    elif args.debug:
        debug += 1
        pass # TODO: Output debugging information
    elif args.init:
        # QUESTION: Do we allow for alternate locations for the database file? If so, we need a new cmd line argument.
        # QUESTION: If we allow an alternate db location, we should pass that location into our create function.
        database.create_sqlite_tables()
    elif args.input:
        # TODO: Determine the full path of the input filename and pass that into our method
        dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir, str(args.input[0]))
        datainput.import_csv(filename)
        pass
    elif args.outputdir:
        pass # TODO: Set output Directory
    elif args.grade:
        pass # TODO: Set grade to process
    else:
        # TODO: Find a better way to call our print_help function. This won't work once we remove all the elif statements
        parser.print_help()
