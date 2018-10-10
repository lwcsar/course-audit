from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

'''
OUTPUT

The program output will initially be in 2 forms.
    1) In-application display
    2) PDF saved to disk

'''

class OutputPDF:
    def __init__(self):
        self.c = canvas.Canvas("Student_Reports.pdf", pagesize=letter)
        self.width, self.height = letter
        self.cursor = self.height - 30
        self.c.drawString(30,self.cursor,"Student Reports:")
        self.cursor -= 15

    def addStudent(self, first_name, last_name, credits, missing):
        self.c.drawString(30, self.cursor, first_name + " " + last_name + ":")
        self.cursor -= 15
        for credit in credits:
            dept = "Temp"
            self.c.drawString(30, self.cursor, dept + ": " + str(credit))
            self.cursor -= 15
            self.c.drawString(30, self.cursor, "Missing " + str(abs(credit)) + " credits")
            self.cursor -= 15


    def savePDF(self):
        self.c.save()
