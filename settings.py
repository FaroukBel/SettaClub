from gymsett_ui import Ui_GymSettings
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from database import MyCursor
from PyQt5.QtCore import QTime, Qt, QTimer

AssuPrice = 0
class GymSett(QMainWindow, Ui_GymSettings):
    confirm = QtCore.pyqtSignal(str)
    def __init__(self):
        super(GymSett, self).__init__()
        self.setupUi(self)
        self.conf.clicked.connect(self.pramconf)
        self.fermer.clicked.connect(self.close)
        self.m = MyCursor()
        self.m.mycursor.execute("SELECT * FROM settings")
        f = self.m.mycursor.fetchall()
        for r in f:
            self.assuPriceConfig.setValue(r[0])
            self.moiPriceConfig.setValue(r[1])
            self.troiMoiPriceConfig.setValue(r[2])

    def pramconf(self):
        self.confirm.emit(self.assuPriceConfig.text())
        self.m = MyCursor()
        self.m.mycursor.execute("INSERT INTO settings (assurPrice, moiPrice, troiMoiPrice) VALUES(%s,%s,%s)", (self.assuPriceConfig.text(),self.moiPriceConfig.text(),self.troiMoiPriceConfig.text()))
        self.m.db.commit()
        self.close()
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = GymSett()
    window.show()
    sys.exit(app.exec())