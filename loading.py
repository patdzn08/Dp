import sqlite3
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets, uic, QtCore

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Design of a Node Avoidance Mechanism')
        self.setFixedSize(468, 204)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300 # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: #2F4454; color: rgb(220, 220, 220);")
        layout.addWidget(self.frame)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')
        self.labelTitle.setStyleSheet("font-size:25px; color:#93deed;")
        

        # center labels
        self.labelTitle.resize(self.width() - 20, 100)
        self.labelTitle.move(0, 40) # x, y
        self.labelTitle.setText('Design of a')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 30)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Initializing Components</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)
        self.labelDescription.setStyleSheet(" font-size: 15px; color: #c2ced1;")

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)
        self.progressBar.setStyleSheet(" background-color: #DA7B93;"
                                      "color: rgb(200, 200, 200);"
                                      "border-style: none;"
                                      "border-radius: 10px;"
                                      "text-align: center;"
                                      "font-size: 30px;")

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('loading...')
        self.labelLoading.setStyleSheet(" font-size: 30px; color: #e8e8eb;")

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong>Initializing Camera</strong>')
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText('<strong>Initializing Arduino</strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(1)

            self.myApp = MyWindow()
            self.myApp.show()

        self.counter += 1

class MyWindow(QtWidgets.QMainWindow,QPushButton):

    def __init__(self,*args, **kwargs):
        super(MyWindow,self).__init__(*args, **kwargs)
        uic.loadUi('lcd.ui', self)
        self.conn = sqlite3.connect("data.db")
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS Nodes(Id INTEGER PRIMARY KEY AUTOINCREMENT "
            ",Name TEXT NOT NULL,"
            "Date Numeric,"
            "Time Numeric)")
        self.c.close()
        self.loaddata()
        
    
    def loaddata(self):
        self.connection = sqlite3.connect("data.db")
        query = "SELECT * FROM Nodes"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        self.tableWidget.resizeRowsToContents()
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.connection.close()




if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    app.setStyleSheet('''
       

        QProgressBar::chunk {
            border-radius: 10px;
            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
        }
    ''')
    
    splash = SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')