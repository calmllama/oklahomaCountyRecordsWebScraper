from PyQt5 import QtGui, QtCore, QtWidgets, uic
import sys

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = uic.loadUi('rent_creation.ui', self)
        #the widgets are called calendarWidget_start_date_2 and calendarWidget_end_date_2
        self.ui.activate_thescript.clicked.connect(self.activate_script)
        self.show()

    def activate_script(self):
        global start_date
        global end_date
        start_date = self.ui.calendarWidget_start_date_2.selectedDate().toString()
        end_date = self.ui.calendarWidget_end_date_2.selectedDate().toString()
        #print data in text browser
        text = "Start date: %s \n End date: %s \n" %(start_date, end_date)
        self.ui.textBrowser.setText(text)

start_date = QtCore.QDate.currentDate()
end_date = QtCore.QDate.currentDate()

def run():     
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()