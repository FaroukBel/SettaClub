import qrcode
import cv2
from pyzbar.pyzbar import decode
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from mainWinPy import Ui_GymSec
from PyQt5.QtCore import QTime, Qt, QTimer
from datetime import datetime
from database import MyCursor
from dateutil.relativedelta import relativedelta
from settings import GymSett
import random



class MainWindowSetta(QMainWindow, Ui_GymSec):
    def __init__(self):
        super(MainWindowSetta, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Statistiques')
        self.ajouter.clicked.connect(self.addclient)
        self.calculer.clicked.connect(self.calculate)
        self.home.clicked.connect(lambda :self.mainStack.setCurrentIndex(0))
        self.actStat.triggered.connect(self.statis)
        self.actionParametres.triggered.connect(self.settingsopen)
        header = self.statTable.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.home.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.m = MyCursor()
        self.m.mycursor.execute("SELECT * FROM clients")
        f = self.m.mycursor.fetchall()
        self.checking_payout()
        self.statTable.setRowCount(0)
        for column_number, row_data in enumerate(f):
            self.statTable.insertRow(column_number)
            for row_number, data in enumerate(row_data):
                self.statTable.setItem(column_number, row_number, QtWidgets.QTableWidgetItem(str(data)))
        self.date.setText(datetime.now().date().strftime('%d/%m/%Y'))
        timer = QTimer(self)
        timer.timeout.connect(self.displaytime)
        timer.start(1000)

    def stat_show(self):
        self.mainStack.setCurrentIndex(0)
        self.checking_payout()

    def checking_payout(self):
        self.m = MyCursor()
        self.m.mycursor.execute("SELECT * FROM clients")
        f = self.m.mycursor.fetchall()

        for r in f:

            date_obj = datetime.strptime(str(r[4]), "%Y-%m-%d")
            if date_obj <= datetime.strptime((datetime.today().strftime("%Y-%m-%d")), "%Y-%m-%d"):
                self.m = MyCursor()
                self.m.mycursor.execute("""UPDATE clients SET payout="NP" WHERE id = "%s" """, (int(r[0]),))
                self.m.db.commit()
            else:
                self.m = MyCursor()
                self.m.mycursor.execute("""UPDATE clients SET payout="P" WHERE id = "%s" """, (int(r[0]),))
                self.m.db.commit()

    @QtCore.pyqtSlot(str)
    def test(self, assuPrice):
        self.assurPrice = assuPrice
        self.prix.setText(self.assurPrice)

    def displaytime(self):
        time = QTime.currentTime()
        self.time.setText(time.toString(Qt.DefaultLocaleLongDate))
    def settingsopen(self):
        self.set = GymSett()
        self.set.confirm.connect(self.test)
        self.set.show()
    def statis(self):
        self.mainStack.setCurrentIndex(1)
        self.m = MyCursor()
        self.m.mycursor.execute("SELECT * FROM clients")
        f = self.m.mycursor.fetchall()
        self.statTable.setRowCount(0)
        for column_number, row_data in enumerate(f):
            self.statTable.insertRow(column_number)
            for row_number, data in enumerate(row_data):
                self.statTable.setItem(column_number, row_number, QtWidgets.QTableWidgetItem(str(data)))




    def addclient(self):
        if self.calculate():
            if self.avcAssu.isChecked():
                if self.unMoi.isChecked():
                    self.assur = 'A'
                    self.expdate = datetime.today() + relativedelta(months=1)

                    self.m = MyCursor()
                    self.m.mycursor.execute(
                        "INSERT INTO clients (prenom,nom,expdate,price,assu)VALUES(%s,%s,%s,%s,%s)",
                        (self.prenom.text(), self.nom.text(), datetime.now(), 200, self.assur))
                    self.m.db.commit()
                else:

                    self.assur = 'A'
                    self.expdate = datetime.today() + relativedelta(months=3)
                    self.expdate.strftime('%Y-%m-%d')
                    print(self.expdate)
                    self.m = MyCursor()
                    self.m.mycursor.execute(
                        "INSERT INTO clients (prenom,nom,expdate,price,assu)VALUES(%s,%s,%s,%s,%s)",
                        (self.prenom.text(), self.nom.text(), self.expdate, 200, self.assur))
                    self.m.db.commit()

            elif self.sansAssu.isChecked():
                if self.unMoi.isChecked():
                    self.assur = 'NA'
                    self.expdate = datetime.today() + relativedelta(months=1)

                    self.m = MyCursor()
                    self.m.mycursor.execute(
                        "INSERT INTO clients (prenom,nom,expdate,price,assu)VALUES(%s,%s,%s,%s,%s)",
                        (self.prenom.text(), self.nom.text(), self.expdate, 200, self.assur))
                    self.m.db.commit()
                else:

                    self.assur = 'NA'
                    self.expdate = datetime.today() + relativedelta(months=3)
                    self.expdate.strftime('%Y-%m-%d %H:%M:%S')
                    print(self.expdate)
                    self.m = MyCursor()
                    self.m.mycursor.execute(
                        "INSERT INTO clients (prenom,nom,expdate,price,assu)VALUES(%s,%s,%s,%s,%s)",
                        (self.prenom.text(), self.nom.text(), self.expdate, 200, self.assur))
                    self.m.db.commit()
        self.checking_payout()


    def calculate(self):
        if self.prenom.text() != "" and self.nom.text() != "":
            if self.avcAssu.isChecked() or self.sansAssu.isChecked() and self.unMoi.isChecked() or \
                    self.troiMoi.isChecked():
                self.mtMoi.setText("")
                self.mtAssu.setText("")
                return True
            self.mtNom.setText("")
            self.mtPrenom.setText("")

            if self.avcAssu.isChecked() and self.unMoi.isChecked():
                self.prix.setText(self.assurPrice)

            elif self.sansAssu.isChecked() and self.unMoi.isChecked():
                self.prix.setText("150DH")
            elif self.avcAssu.isChecked() and self.troiMoi.isChecked():
                self.prix.setText("500DH")
            elif self.sansAssu.isChecked() and self.troiMoi.isChecked():
                self.prix.setText("350DH")
            elif not self.avcAssu.isChecked() and not self.sansAssu.isChecked():
                self.mtAssu.setText("*")
            elif not self.unMoi.isChecked() and not self.troiMoi.isChecked():
                self.mtMoi.setText("*")
        elif self.prenom.text() != "" and self.nom.text() == "":
            self.mtNom.setText("*")
            self.mtPrenom.setText("")

        elif self.prenom.text() == "" and self.nom.text() != "":
            self.mtPrenom.setText("*")
            self.mtNom.setText("")
        elif self.prenom.text() == "" and self.nom.text() == "":
            self.mtPrenom.setText("*")
            self.mtNom.setText("*")


# cap = cv2.VideoCapture(1)
#
# while True:
#     ret, frame = cap.read()
#     for codedata in decode(frame):
#         data = codedata.data.decode("utf-8")
#         print(data)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindowSetta()
    window.show()
    sys.exit(app.exec())

# qr = qrcode.make("2900")
# qr.save('qrtest.png')