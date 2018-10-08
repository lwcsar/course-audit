import logging

'''

PROCESS

Our main processing methods will live here. These methods will aid the UI
and handle all the business logic including but not limited to report
generation, course planning, settings maintenance.


'''
class Process():
    def totalCredit(student_id, session):
        """Finds the total credit that a student has"""
        from lib.database_schema import Base, Student, Course
        student = session.query(Student).filter(Student.id == student_id).one()
        logging.warning(student.last_name)
        course = session.query(Student).filter(Student.id == student_id).one()
        logging.warning(course.last_name)
