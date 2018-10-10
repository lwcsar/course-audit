from reportlab.pdfgen import canvas

'''
OUTPUT

The program output will initially be in 2 forms.
    1) In-application display
    2) PDF saved to disk

'''

class OutputPDF:
    def __init__(self):
        c = canvas.Canvas("Student_Reports.pdf", pagesize=letter)
        c.drawString(30,750,"Student Reports:")
        
    
        
    def savePDF(self):
        c = save()
