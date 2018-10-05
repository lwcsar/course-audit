import os
import sqlite3
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class Database():
    """"""

    def __init__(self, db_name):
        """"""
        self.engine = create_engine('sqlite:///'+ db_name)
        self.session = sessionmaker(bind=self.engine)
        self.s = self.session()

    def session():
        return self.s

    def create_default_settings(self):
        from .database_schema import Base, Setting
        self.s.query(Setting).delete()
        settings = [
            Setting(key='last_import', value=''),
            Setting(key='color_ninth', value='red'),
            Setting(key='color_tenth', value='green'),
            Setting(key='color_eleventh', value='blue'),
            Setting(key='color_twelfth', value='yellow'),
            Setting(key='minimum_core_total', value=22.5),
            Setting(key='minimum_elective_total', value=6.5),
            Setting(key='minimum_total', value=29),
            Setting(key='minimum_dept_bible', value=4),
            Setting(key='minimum_dept_mathematics', value=4),
            Setting(key='minimum_dept_language_arts', value=4),
            Setting(key='minimum_dept_social_studies', value=4),
            Setting(key='minimum_dept_science', value=3),
            Setting(key='minimum_dept_foreign_language', value=2),
            Setting(key='minimum_dept_physical_education', value=1),
            Setting(key='minimum_dept_oral_communications', value=0.5),
            Setting(key='minimum_dept_fine_arts', value=0.5),
            Setting(key='minimum_dept_practical_arts', value=1),
            Setting(key='minimum_dept_technology', value=0.5),
            Setting(key='minimum_dept_other', value=0),
        ]
        self.s.bulk_save_objects(settings)
        self.s.commit()
