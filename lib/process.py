import logging
from lib.database import Database

'''

PROCESS

Our main processing methods will live here. These methods will aid the UI
and handle all the business logic including but not limited to report
generation, course planning, settings maintenance.


'''
class Process():
    def process_setup():
        session = db.session
    def get_student(student_id):
        from lib.database_schema import Base, Course
        student = session.query(Student).filter(Student.id == student_id).one()
        return student

    def get_course(course_id):
        """Returns course from the database"""
        from lib.database_schema import Base, Course
        course = session.query(Course).filter(Course.id == course_id).one()
        return course

    def get_student_courses(student_id):
        """Returns the courses that a student has taken"""
        # TODO: get an array of courses that a student has taken
        return courses

    def process_student(student_id):
        """Returns array holding total credits of a student and credits in each department"""
        student = get_student(student_id)
        courses = get_student_courses(student_id)
        """Credits = [total_credits, core_total, elective_total, bible, mathematics, language_arts,
        social_studies, science, foreign_language, physical_education, oral_communications,
        fine_arts, practical_arts, technology, other]"""
        credits = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for course in courses:
            credit = course.course_credit
            dept = course.course_department
            Credits[0] += credit
            # QUESTION: Is there a more efficient way to do this???
            if dept == "Mathematics":
                Credits[5] += credit
                Credits[2] += credit
