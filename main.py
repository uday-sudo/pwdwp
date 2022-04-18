#For gui and shit
import assets.data
import json
import sys
import random
# import PySide6
from PySide6.QtCore import * #QSize, Qt
from PySide6.QtWidgets import * #QApplication, QMainWindow, QPushButton, QHBoxLayout
from PySide6.QtGui import *


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        assets.data.make_if_not()
        self.setWindowTitle("PWDWP")
        self.setWindowIcon(QIcon('assets/icon.png'))
        button_layout = QHBoxLayout()
        layout = QVBoxLayout()
        self.setMinimumSize(QSize(500,500))

        self.CurrentRow = 1
        self.temp_info = []   #[service,username,email,password]

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Row ID", "Service", "Username", "Email"])
        self.AllInfo = assets.data.give_all()
        self.table.setRowCount(len(self.AllInfo))
        for i in range(0, len(self.AllInfo)):
            self.table.setItem(i,0,QTableWidgetItem(self.AllInfo[i][0]))
            self.table.setItem(i,1,QTableWidgetItem(self.AllInfo[i][1]))
            self.table.setItem(i,2,QTableWidgetItem(self.AllInfo[i][2]))
            self.table.setItem(i,3,QTableWidgetItem(self.AllInfo[i][3]))

        self.buttons = {
            "new_entry":QPushButton(),
            "edit_entry":QPushButton(),
            "delete_entry":QPushButton(),

            "copy_username":QPushButton(),
            "copy_account":QPushButton(),
            "copy_password":QPushButton(),

            "random_password":QPushButton()
        }

        for key in self.buttons:
            button_layout.addWidget(self.buttons[key])
            self.buttons[key].setFixedSize(QSize(45, 45))
            self.buttons[key].setIconSize(QSize(40, 40))

        self.buttons["new_entry"].setIcon(QIcon("assets/new_entry"))
        self.buttons["edit_entry"].setIcon(QIcon("assets/edit_entry"))
        self.buttons["delete_entry"].setIcon(QIcon("assets/delete_entry"))
        self.buttons["copy_username"].setIcon(QIcon("assets/user"))
        self.buttons["copy_account"].setIcon(QIcon("assets/at_symbol"))
        self.buttons["copy_password"].setIcon(QIcon("assets/password"))
        self.buttons["random_password"].setIcon(QIcon("assets/random"))

        self.buttons["new_entry"].clicked.connect(self.new_entry)
        self.buttons["edit_entry"].clicked.connect(self.edit_entry)
        self.buttons["delete_entry"].clicked.connect(self.delete_entry)
        self.buttons["copy_username"].clicked.connect(self.copy_username)
        self.buttons["copy_account"].clicked.connect(self.copy_account)
        self.buttons["copy_password"].clicked.connect(self.copy_password)
        self.buttons["random_password"].clicked.connect(self.random_password)

        button_layout.addStretch(10)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def new_entry(self):
        self.temp_info[0], done1 = QInputDialog.getText(self, 'Input Dialog', 'Enter your service:')
        self.temp_info[1], done2 = QInputDialog.getText(self, 'Input Dialog', 'Enter your Username:')
        self.temp_info[2], done3 = QInputDialog.getText(self, 'Input Dialog', 'Enter your Email')
        self.temp_info[3], done4 = QInputDialog.getText(self, 'Input Dialog', 'Enter your Password')
        if done1 and done2 and done3 and done4:
            assets.data.new_entry(self.temp_info[0],self.temp_info[1],self.temp_info[2],self.temp_info[3],"")
        self.AllInfo = assets.data.give_all()
        self.table.setRowCount(len(self.AllInfo))
        for i in range(0, len(self.AllInfo)):
            self.table.setItem(i,0,QTableWidgetItem(self.AllInfo[i][0]))
            self.table.setItem(i,1,QTableWidgetItem(self.AllInfo[i][1]))
            self.table.setItem(i,2,QTableWidgetItem(self.AllInfo[i][2]))
            self.table.setItem(i,3,QTableWidgetItem(self.AllInfo[i][3]))

    def edit_entry(self):
        self.CurrentRow = self.table.currentRow()
        self.temp_info[0], done1 = QInputDialog.getText(self, 'Input Dialog', 'Enter your service:')
        self.temp_info[1], done2 = QInputDialog.getText(self, 'Input Dialog', 'Enter your Username:')
        self.temp_info[2], done3 = QInputDialog.getText(self, 'Input Dialog', 'Enter your Email')
        self.temp_info[3], done4 = QInputDialog.getText(self, 'Input Dialog', 'Enter your Password')

        assets.data.edit_entry(self.AllInfo[self.CurrentRow][0],[self.temp_info[0],self.temp_info[1],self.temp_info[2],self.temp_info[3],""])
        self.AllInfo = assets.data.give_all()
        self.table.setRowCount(len(self.AllInfo))
        for i in range(0, len(self.AllInfo)):
            self.table.setItem(i,0,QTableWidgetItem(self.AllInfo[i][0]))
            self.table.setItem(i,1,QTableWidgetItem(self.AllInfo[i][1]))
            self.table.setItem(i,2,QTableWidgetItem(self.AllInfo[i][2]))
            self.table.setItem(i,3,QTableWidgetItem(self.AllInfo[i][3]))

    def delete_entry(self):
        self.CurrentRow = self.table.currentRow()
        assets.data.del_entry(self.AllInfo[self.CurrentRow][0])
        self.table.setHorizontalHeaderLabels(["Row ID", "Service", "Username", "Email"])
        self.AllInfo = assets.data.give_all()
        self.table.setRowCount(len(self.AllInfo))
        for i in range(0, len(self.AllInfo)):
            self.table.setItem(i,0,QTableWidgetItem(self.AllInfo[i][0]))
            self.table.setItem(i,1,QTableWidgetItem(self.AllInfo[i][1]))
            self.table.setItem(i,2,QTableWidgetItem(self.AllInfo[i][2]))
            self.table.setItem(i,3,QTableWidgetItem(self.AllInfo[i][3]))

    def copy_username(self):
        assets.data.copy_text(self.AllInfo[self.CurrentRow][2])
        print("Username Copied")
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Success")
        dlg.setText("Username Copied to clipboard")
        dlg.exec()

    def copy_account(self):
        assets.data.copy_text(self.AllInfo[self.CurrentRow][3])
        print("Account Copied")
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Success")
        dlg.setText("Account Copied to clipboard")
        dlg.exec()

    def copy_password(self):
        assets.data.copy_text(self.AllInfo[self.CurrentRow][4])
        print("Password Copied")
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Success")
        dlg.setText("Password Copied to Clipboard")
        dlg.exec()
        self.clipboard = assets.data.gen_pass(True, True, True, True)

    def random_password(self):
        assets.data.copy_text(self.clipboard)
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Success")
        dlg.setText("A very strong password has been Copied to Clipboard")
        dlg.exec()

# Boilerplate Code from here on out
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

# for i in range(5):
#     assets.data.new_entry("discord","uday","email","pass","not")
