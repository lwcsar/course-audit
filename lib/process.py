import logging
from lib.database import Database

'''

PROCESS

Our main processing methods will live here. These methods will aid the UI
and handle all the business logic including but not limited to report
generation, course planning, settings maintenance.


'''
class Process():
    def __init__(self, session):
        self.session = session
    def get_student(self, session, student_id):
        from lib.database_schema import Base, Student
        student = session.query(Student).filter(Student.id == student_id).one()
        return student

    def get_course(self, session, course_id):
        """Returns course from the database"""
        from lib.database_schema import Base, Course
        course = session.query(Course).filter(Course.id == course_id).one()
        return course

    def get_student_courses(self, session, student_id):
        """Returns the courses that a student has taken"""
        student = self.get_student(session, student_id)
        courses = student.courses
        return courses

    def process_student(self, session, first_name, last_name):
        """Returns array holding total credits of a student and credits in each department"""
        from lib.database_schema import Base, Student
        first_name_query = session.query(Student).filter(Student.first_name == first_name)
        last_name_query = session.query(Student).filter(Student.last_name == last_name)
        student = first_name_query.union(last_name_query).one()
        student_id = student.id
        courses = self.get_student_courses(session, student_id)
        credits = self.find_credits(courses)
        return credits

    def process_grade(self, session, grade):
        from lib.database_schema import Base, Student
        students = session.query(Student).filter(Student.grade_level == grade)
        student_courses = []
        for student in students:
            credits = self.find_credits(student.courses)
            student_courses.append(credits)
        return student_courses

    def process_all(self, session):
        from lib.database_schema import Base, Student
        students = session.query(Student)
        students = students.order_by(Student.last_name)
        student_courses = []
        for student in students:
            credits = self.find_credits(student.courses)
            student_courses.append(credits)
        return student_courses

    def find_credits(self, courses):
        """Credits = [core_total, elective_total, total_credits bible, mathematics, language_arts,
        social_studies, science, foreign_language, physical_education, oral_communications,
        fine_arts, practical_arts, technology, other]"""
        Credits = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for course in courses:
            credit = course.course_credit
            dept = course.course_department
            Credits[2] += credit
            if dept == "Bible":
                Credits[3] += credit
                Credits[0] += credit
            elif dept == "Mathematics":
                Credits[4] += credit
                Credits[0] += credit
            elif dept == "Language Arts" or dept == "English":
                Credits[5] += credit
                Credits[0] += credit
            elif dept == "Social Studies":
                Credits[6] += credit
                Credits[0] += credit
            elif dept == "Science":
                Credits[7] += credit
                Credits[0] += credit
            elif dept == "Foreign Language":
                Credits[8] += credit
                Credits[1] += credit
            elif dept == "Physical Education":
                Credits[9] += credit
                Credits[1] += credit
            elif dept == "Oral Communications":
                Credits[10] += credit
                Credits[1] += credit
            elif dept == "Fine Arts":
                Credits[11] += credit
                Credits[1] += credit
            elif dept == "Practical Arts":
                Credits[12] += credit
                Credits[1] += credit
            elif dept == "Technology":
                Credits[13] += credit
                Credits[1] += credit
            elif dept == "Other":
                Credits[14] += credit
                Credits[1] += credit
            else:
                logging.error(course.course_name + " has no department")

        return Credits

    def missing_credits(self, session, Credits):
        from lib.database_schema import Base, Setting
        missing = []
        settings = session.query(Setting)
        pos = 0
        for credit in Credits:
            compare_credits = credit - float((session.query(Setting).filter(Setting.id == pos + 6).first()).value)
            pos += 1
            if compare_credits > 0:
                compare_credits = 0
            missing.append(compare_credits)
        return missing
