# import socket 
# import sys
# import threading
# sys.path.append('C:\\Users\\adars\\PycharmProjects\\pythonProject\\application\\venv\\Lib\\site-packages')

# from PyQt5.QtCore import Qt, pyqtSignal # type: ignore
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSlider, QScrollArea # type: ignore
# from PyQt5.QtGui import QFont, QIcon, QPixmap # type: ignore
# import sqlite3


# class Receiver(QMainWindow):
#     dataReceived = pyqtSignal(str)
#     def __init__(self):
#         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.s.bind(('0.0.0.0', 9999))
#         self.s.listen(5)

#         super().__init__()

#         self.initUI()
        
#         self.dataReceived.connect(self.setData)

#     def initUI(self):
#         self.mainWidget = QWidget()
#         self.mainLayout = QVBoxLayout()
#         self.subLayout = QVBoxLayout()

#         self.mainLayout.addLayout(self.subLayout)
#         self.mainLayout.addStretch(1)
#         self.mainWidget.setLayout(self.mainLayout)
#         self.setCentralWidget(self.mainWidget)      
    
#     def setData(self, data):
#         dataLabel = QLabel()
#         dataLabel.setText(data)

#         self.subLayout.addWidget(dataLabel)
    
#     def rec(self):
#         def receiver():
#             self.conn, self.addr = self.s.accept()
#             print(f"Connected on {self.addr}")

#             while True:
#                 data = self.conn.recv(1024).decode()
#                 if data:
#                     self.dataReceived.emit(data)
        
#         r = threading.Thread(target=receiver, daemon=True)
#         r.start()

#     def showScreen(self):
#         self.showMaximized()

# app = QApplication([])        
# receive = Receiver()
# receive.rec()
# receive.showScreen()
# app.exec_()

import socket
import sys
import threading
import sqlite3
import os

sys.path.append('C:\\Users\\adars\\PycharmProjects\\pythonProject\\application\\venv\\Lib\\site-packages')
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QFont

DB_FILE = "received_messages.db"

class Receiver(QMainWindow):
    dataReceived = pyqtSignal(str)

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('0.0.0.0', 9999))
        self.s.listen(5)

        super().__init__()
        self.initDB()
        self.initUI()
        self.dataReceived.connect(self.setData)

    def initDB(self):
        self.conn_db = sqlite3.connect(DB_FILE)
        self.cursor = self.conn_db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT
            )
        """)
        self.conn_db.commit()

    def loadOldMessages(self):
        self.cursor.execute("SELECT content FROM messages")
        for row in self.cursor.fetchall():
            self.displayMessage(row[0])

    def saveMessage(self, content):
        self.cursor.execute("INSERT INTO messages (content) VALUES (?)", (content,))
        self.conn_db.commit()

    def initUI(self):
        self.setWindowTitle("Message Viewer")
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        self.scrollArea = QScrollArea()
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout()

        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.mainLayout.addWidget(self.scrollArea)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.loadOldMessages()

    def displayMessage(self, data):
        dataLabel = QLabel(data)
        dataLabel.setFont(QFont("Segoe UI", 12))
        dataLabel.setWordWrap(True)
        dataLabel.setStyleSheet("padding: 8px; background-color: #e0f7fa; border-radius: 10px; margin: 4px;")
        self.scrollLayout.addWidget(dataLabel)

    def setData(self, data):
        self.displayMessage(data)
        self.saveMessage(data)

    def rec(self):
        def receiver():
            self.conn, self.addr = self.s.accept()
            print(f"Connected on {self.addr}")
            while True:
                data = self.conn.recv(1024).decode()
                if data:
                    self.dataReceived.emit(data)

        r = threading.Thread(target=receiver, daemon=True)
        r.start()

    def showScreen(self):
        self.showMaximized()

app = QApplication([])
receive = Receiver()
receive.rec()
receive.showScreen()
app.exec_()
