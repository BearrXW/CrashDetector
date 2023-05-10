import time
import os
import psutil
import requests
import json
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap  # Add this line to import QPixmap

# Discord webhook configuration
with open("webhook.txt", "r") as f:
    webhook_url = f.read().strip()

reopened_count = 0
checks_count = 0
last_restart_time = time.time()
message_id = None

# Set the restart interval and check interval
restart_interval = 20 * 60  # 20 minutes
check_interval = 5  # 5 seconds

# Logo
logo_color = '#4CAF50'
logo = r"""
   _____               _       _____       _            _             
  / ____|             | |     |  __ \     | |          | |            
 | |     _ __ __ _ ___| |__   | |  | | ___| |_ ___  ___| |_ ___  _ __ 
 | |    | '__/ _` / __| '_ \  | |  | |/ _ \ __/ _ \/ __| __/ _ \| '__|
 | |____| | | (_| \__ \ | | | | |__| |  __/ ||  __/ (__| || (_) | |   
  \_____|_|  \__,_|___/_| |_| |_____/ \___|\__\___|\___|\__\___/|_|   
"""

class CrashDetectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crash Detector")
        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("background.png"))  # Load the background image
        self.background_label.setGeometry(0, 0, 1000, 1000)

        self.logo_label = QLabel(self)
        self.logo_label.setText(logo)
        self.logo_label.setStyleSheet(f"QLabel {{ color: {logo_color}; font-size: 24px; }}")
        self.logo_label.setGeometry(40, 40, 920, 200)

        self.stats_button = QPushButton(self)
        self.stats_button.setText("Stats")
        self.stats_button.setStyleSheet("QPushButton { background-color: transparent; color: white; font-size: 18px; "
                                         "border: none; text-align: left; padding-left: 20px; }"
                                         "QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); }")
        self.stats_button.setGeometry(100, 300, 150, 50)
        self.stats_button.clicked.connect(self.open_stats)

        self.settings_button = QPushButton(self)
        self.settings_button.setText("Settings")
        self.settings_button.setStyleSheet("QPushButton { background-color: transparent; color: white; font-size: 18px; "
                                            "border: none; text-align: left; padding-left: 20px; }"
                                            "QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); }")
        self.settings_button.setGeometry(100, 400, 150, 50)
 import time
import os
import psutil
import requests
import json
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap  # Add this line to import QPixmap

# Discord webhook configuration
with open("webhook.txt", "r") as f:
    webhook_url = f.read().strip()

reopened_count = 0
checks_count = 0
last_restart_time = time.time()
message_id = None

# Set the restart interval and check interval
restart_interval = 20 * 60  # 20 minutes
check_interval = 5  # 5 seconds

# Logo
logo_color = '#4CAF50'
logo = r"""
   _____               _       _____       _            _             
  / ____|             | |     |  __ \     | |          | |            
 | |     _ __ __ _ ___| |__   | |  | | ___| |_ ___  ___| |_ ___  _ __ 
 | |    | '__/ _` / __| '_ \  | |  | |/ _ \ __/ _ \/ __| __/ _ \| '__|
 | |____| | | (_| \__ \ | | | | |__| |  __/ ||  __/ (__| || (_) | |   
  \_____|_|  \__,_|___/_| |_| |_____/ \___|\__\___|\___|\__\___/|_|   
"""

class CrashDetectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crash Detector")
        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("background.png"))  # Load the background image
        self.background_label.setGeometry(0, 0, 1000, 1000)

        self.logo_label = QLabel(self)
        self.logo_label.setText(logo)
        self.logo_label.setStyleSheet(f"QLabel {{ color: {logo_color}; font-size: 24px; }}")
        self.logo_label.setGeometry(40, 40, 920, 200)

        self.stats_button = QPushButton(self)
        self.stats_button.setText("Stats")
        self.stats_button.setStyleSheet("QPushButton { background-color: transparent; color: white; font-size: 18px; "
                                         "border: none; text-align: left; padding-left: 20px; }"
                                         "QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); }")
        self.stats_button.setGeometry(100, 300, 150, 50)
        self.stats_button.clicked.connect(self.open_stats)

        self.settings_button = QPushButton(self)
        self.settings_button.setText("Settings")
        self.settings_button.setStyleSheet("QPushButton { background-color: transparent; color: white; font-size: 18px; "
                                            "border: none; text-align: left; padding-left: 20px; }"
                                            "QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); }")
        self.settings_button.setGeometry(100, 400, 150, 50)
self.settings_button.clicked.connect(self.open_settings)

        self.close_button = QPushButton(self)
        self.close_button.setIcon(QIcon("close_icon.png"))
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }"
                                         "QPushButton:hover { background-color: rgba(255, 0, 0, 0.1); }")
        self.close_button.setGeometry(940, 40, 24, 24)
        self.close_button.clicked.connect(self.close)

    def open_stats(self):
        print("Stats button clicked")
        # Add your code to handle the "Stats" button functionality here

    def open_settings(self):
        print("Settings button clicked")
        # Add your code to handle the "Settings" button functionality here

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication([])
    window = CrashDetectorWindow()
    window.show()
    app.exec_()

