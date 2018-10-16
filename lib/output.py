import kivy
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

'''
OUTPUT

The program output will initially be in 2 forms.
    1) In-application display
    2) PDF saved to disk

'''
background_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Background.png")
default_csv = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Display.txt")

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

        f = open(output_file, 'w')
        f.write('Student Reports:' + '\n')
        f.close()

    def addStudent(self, first_name, last_name, Credits, missing):
        f = open(output_file, 'a')
        self.c.drawString(self.STUDENT_INDENT, self.cursor, last_name + ", " + first_name + ":")
        f.write('     ' + last_name + ', ' + first_name + ':' + '\n')
        self.move_line()
        pos = 0
        for credit in Credits:
            self.c.drawString(self.CREDIT_INDENT, self.cursor, credit + ": " + str(Credits[credit]))
            f.write('     ' + '     ' + credit + ': ' + str(Credits[credit]) + '\n')
            self.move_line()
            self.c.drawString(self.MISSING_INDENT, self.cursor, "Missing " + str(abs(missing[credit])) + " credits")
            f.write('     ' + '     ' + '     ' + 'Missing ' + str(abs(missing[credit])) + ' credits' + '\n')
            self.move_line()
        f.close()

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
class DisplayScreen(Screen):
    text = StringProperty('')

    def load_display(self, **kwargs):
        self.text = "Test"
        with open(output_file, "r") as f:
            contents = f.read()
            self.text = contents
    pass
class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "main.kv"))

class OutputUI(App):
    def build(self):
        return presentation
