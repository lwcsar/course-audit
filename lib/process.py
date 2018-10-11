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
        Credits = {"total_credits":0, "core_total":0, "elective_total":0, "Bible":0, "Mathematics":0, "English":0,
                   "Social Studies":0, "Science":0, "Foreign Language":0, "Physical Education":0, "Oral Communications":0,
                   "Fine Arts":0, "Practical Arts":0, "Technology": 0, "Other":0}
        for course in courses:
            credit = course.course_credit
            Credits["total_credits"] += credit
            if course.course_department == "":
                Credits["Other"] += credit
                logging.info(course.course_department + " is missing a department. Added to Other")
            else:
                Credits[course.course_department] += credit
        for dept in Credits:
            if dept == "total_credits" or dept == "core_total" or dept == "elective_total":
                continue

            if dept == "Bible" or dept == "Mathematics" or dept == "English" or dept == "Social Studies" or dept == "Science": # and the rest
                Credits["core_total"] += Credits[dept]
            else:
                Credits["elective_total"] += Credits[dept]

        return Credits

    def missing_credits(self, session, Credits):
        from lib.database_schema import Base, Setting
        missing = {"total_credits":0, "core_total":0, "elective_total":0, "Bible":0, "Mathematics":0, "English":0,
                   "Social Studies":0, "Science":0, "Foreign Language":0, "Physical Education":0, "Oral Communications":0,
                   "Fine Arts":0, "Practical Arts":0, "Technology": 0, "Other":0}
        settings = session.query(Setting)
        pos = 0
        for credit in Credits:
            missing[credit] = Credits[credit] - float((session.query(Setting).filter(Setting.id == pos + 6).first()).value)
            pos += 1
        return missing
