from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey, func
from sqlalchemy import Column, Date, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///coursemap.db', echo=True)

class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id =  Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)

class TimestampMixin(object):
    last_updated = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Course(TimestampMixin, Base):
    """"""
    __tablename__ = 'course'
    # Here we define columns for the table course
    # Notice that each column is also a normal Python instance attribute.
    course_name = Column(String(128), nullable=False)
    course_department = Column(String(64), nullable=False)
    course_grade_level = Column(Integer, nullable=False)
    course_credit = Column(Float, default=0.0)
    #students = relationship('Student', secondary='student_course', back_populates='courses')
    idx_course = Index('idx_course', course_name, course_department, course_grade_level, unique=True)



class Student(TimestampMixin, Base):
    """"""
    __tablename__ = 'student'
    # Here we define columns for the table student
    # Notice that each column is also a normal Python instance attribute.
    last_name = Column(String(64), nullable=False)
    first_name = Column(String(32), nullable=False)
    grade_level = Column(Integer, nullable=False)
    courses = relationship(
        'Course',
        secondary=Table('student_course', Base.metadata,
                Column('student_id', Integer, ForeignKey('student.id'), primary_key=True),
                Column('course_id', Integer, ForeignKey('course.id'), primary_key=True),
            ),
        backref='students'
        )


class Setting(TimestampMixin, Base):
    """"""
    __tablename__ = 'setting'

    key = Column(String(32), unique=True)
    value = Column(String(255))


def run(db_name):
    """Create all our the database tables"""
    Base.metadata.create_all(engine)
