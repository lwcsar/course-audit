import os
import sqlite3
import logging

def sqlite_connect():
    # Check for default sqlite database
    # if not exist, create
    #   import sql.txt into new database
    # Connect to DB and return
    conn = sqlite3.connect('coursemap.db')
    return conn

def create_sqlite_tables():
    sqlfile = open("doc/sql.txt", "r")
    sqltxt = sqlfile.read()
    c.executescript(sqltxt)

def create_course(row):
    #logging.debug(row['Course']+' '+row['Department']+' '+row['Grade Level']+' '+row['Credits'])
    c.execute("REPLACE INTO courses(course_name,course_department,course_grade_level,course_credit) VALUES (?,?,?,?)",
        (row['Course'],row['Department'],row['Grade Level 1'], row['Credits']))
    conn.commit()
    return c.lastrowid


def create_student(row):
    (last_name, first_name) = row['LastName, FirstName'].split(',')
    logging.debug(row['Student ID (System)']+','+first_name.strip())
    c.execute("REPLACE INTO students(id,last_name,first_name,grade_level) VALUES (?,?,?,?)",
        (row['Student ID (System)'],last_name.strip(),first_name.strip(),row['Grade Level']))
    conn.commit()
    return c.lastrowid


def create_student_course(student_id,course_id,credits):
    #logging.debug(student_id+' '+course_id+' '+row['Credits'])
    c.execute("REPLACE INTO student_courses(student_id,course_id,credits_earned) VALUES (?,?,?)",
        (student_id,course_id,credits))
    conn.commit()
    return c.lastrowid


conn = sqlite_connect()
c = conn.cursor()
