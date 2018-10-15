import kivy
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder

'''
OUTPUT

The program output will initially be in 2 forms.
    1) In-application display
    2) PDF saved to disk

'''
background_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Background.png")
default_csv = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")

class OutputPDF:
    def __init__(self, output):
        self.HEADER_INDENT = 30
        self.STUDENT_INDENT = 40
        self.CREDIT_INDENT = 60
        self.MISSING_INDENT = self.CREDIT_INDENT + 10
        self.TOP_MARGIN = 30
        self.BOTTOM_MARGIN = 30
        self.LINE_OFFSET = 15

        self.c = canvas.Canvas(output, pagesize=letter)
        self.width, self.height = letter
        self.cursor = self.height - 30
        self.c.drawString(self.HEADER_INDENT,self.cursor,"Student Reports:")
        self.move_line()

    def addStudent(self, first_name, last_name, Credits, missing):
        self.c.drawString(self.STUDENT_INDENT, self.cursor, last_name + ", " + first_name + ":")
        self.move_line()
        pos = 0
        for credit in Credits:
            self.c.drawString(self.CREDIT_INDENT, self.cursor, credit + ": " + str(Credits[credit]))
            self.move_line()
            self.c.drawString(self.MISSING_INDENT, self.cursor, "Missing " + str(abs(missing[credit])) + " credits")
            self.move_line()

    def move_line(self):
        self.cursor -= self.LINE_OFFSET
        if self.cursor < self.BOTTOM_MARGIN:
            self.cursor = self.height - self.TOP_MARGIN
            self.c.showPage()

    def savePDF(self):
        self.c.save()

#Screen Classes
class HomeScreen(Screen):
    pass
class InputScreen(Screen):
    pass
class StudentScreen(Screen):
    pass
class GradeScreen(Screen):
    pass
class AllScreen(Screen):
    pass
class SettingScreen(Screen):
    pass
class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "main.kv"))

class OutputUI(App):
    def build(self):
        return presentation
