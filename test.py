import sys
import csv
import platform
import re
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


current_date = datetime.date.today()
currentMonth = current_date.month
currentDay = current_date.day
currentYear = current_date.year
#Colors
redColor = "DB162F"
yellowColor = "FFBA08"
greenColor = "00A676"
foregroundColor = "CABAC8"
backgroundColor = "E8E1EF"

mySystem = ""

if platform.system() == "Darwin":
    mySystem = "macOS"
elif platform.system() == "Windows": 
    mySystem = "Windows"
else:
    mySystem = "Something Else"

# Create the application
app = QApplication(sys.argv)

# Create a QTimer to periodically check if the application is responsive
check_timer = QTimer()

# Function to be called when the check timer times out
def check_application():
    if not app.applicationState() == Qt.ApplicationActive:
        # Application is unresponsive, force quit
        app.quit()

# Connect the check_application function to the timeout signal of the check timer
check_timer.timeout.connect(check_application)

# Start the check timer with a specified interval (in milliseconds)
check_timer.start(500)  # Adjust the interval as needed

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Planner")
        self.setWindowIcon(QIcon(r"C:\Users\whatk\Downloads\planner.png"))
        self.setFixedHeight(600)
        self.setFixedWidth(900)

        # Create a widget for the heading and scroll area
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Create a widget and a layout for the heading and button
        heading_widget = QWidget()
        heading_layout = QHBoxLayout(heading_widget)

        # Create the "Planner" label
        label = QLabel("Planner")
        heading_layout.addWidget(label)

        # Create the "New" button
        button = QPushButton("New")
        heading_layout.addWidget(button)

        # Add the heading widget to the main layout
        main_layout.addWidget(heading_widget)

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its widget

        # Create a widget and a layout for the scrollable content
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setAlignment(Qt.AlignTop)

        # Create a QGridLayout for new elements
        grid_layout = QGridLayout()
        scroll_layout.addLayout(grid_layout)

        # Set spacing between objects in a row
        grid_layout.setHorizontalSpacing(5)

        data = [
            ['ID', 'Due Date', 'Subject', 'Information', 'Notes', 'Importance']
        ]
        filePath = r"C:\Users\whatk\Desktop\planner\info.csv"

        with open(filePath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        print("Created CSV successfully.")

        # Function to be called when the button is clicked
        def new_button():
            new_labels = ["Due Date", "Subject", "Information", "Notes", "Importance"]
            column = 0
            row = grid_layout.rowCount()

            for label_text in new_labels:
                new_label = QLabel(label_text)
                new_label.setStyleSheet("background-color: lightblue;")
                new_label.setAlignment(Qt.AlignCenter)
                new_label.setFixedHeight(30)

                grid_layout.addWidget(new_label, row, column)
                column += 1
                if label_text == "Due Date":
                    new_label.setStyleSheet("background-color: lightblue; text-align: center; border-top-left-radius: 5px; border-bottom-left-radius: 5px")
                if label_text == "Importance":
                    new_label.setMaximumWidth(45)

            # Create the "Edit" button at the end of the row
            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet("background-color: lightblue; text-align: center;")
            edit_button.setFixedHeight(30)
            grid_layout.addWidget(edit_button, row, column)

            # Create the "Close" button at the end of the row
            close_button = QPushButton("Close")
            close_button.setStyleSheet("background-color: lightblue; text-align: center; border-top-right-radius: 5px; border-bottom-right-radius: 5px")
            close_button.setFixedHeight(30)
            grid_layout.addWidget(close_button, row, column + 1)
            close_button.clicked.connect(lambda _, row=row: delete_row(row))

            # Add spacing between rows
            if row > 0:
                row_spacer = QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Fixed)
                scroll_layout.addItem(row_spacer)

            self.new_window = QMainWindow()  # Store the new window as an instance variable
            self.new_window.setWindowTitle("New")
            self.new_window.setWindowIcon(QIcon(r"C:\Users\whatk\Downloads\planner.png"))
            self.new_window.setFixedHeight(150)
            self.new_window.setFixedWidth(900)
            self.new_window.show()

            central_widget = QWidget(self.new_window)
            self.new_window.setCentralWidget(central_widget)

            layout = QHBoxLayout(central_widget)
            layout.setAlignment(Qt.AlignTop)

            new_labels = ["Due Date", "Subject", "Information", "Notes", "Importance"]

            for label_text in new_labels:
                row_widget = QWidget()
                row_layout = QVBoxLayout(row_widget)
                row_layout.setAlignment(Qt.AlignTop)
                
# LOOK AT ME it is late right now but i think you should make it so there are like 6 different inputs for dateTime and put it in one widget and then throw that into the row layout or whatever


#MM/DD/YYYY HH:MM AM/PM
                if label_text == "Due Date":
                    
                    labelContainer = QWidget()
                    labelLayout = QVBoxLayout(labelContainer)
                    label = QLabel(label_text+ " (defaults to current date)")
                    formatLabel = QLabel("MM  /   DD   /    YYYY      HH  :  MM   AM/PM")

                    labelLayout.addWidget(label )
                    labelLayout.addWidget(formatLabel)
                    labelLayout.setAlignment(Qt.AlignTop)



                    dateContainer = QWidget()
                    containerLayout = QHBoxLayout(dateContainer)
                    month = QSpinBox()
                    slash1 = QLabel()
                    day = QSpinBox()
                    slash2 = QLabel()
                    year = QSpinBox()
                    space = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                    hour = QSpinBox()
                    colon = QLabel()
                    minute = QSpinBox()
                    AMPM = QComboBox()
                    AMPM.addItem("AM")
                    AMPM.addItem("PM")

                    slash1.setText("/")
                    slash2.setText("/")
                    colon.setText(":")

                    slash1.setAlignment(Qt.AlignBottom)
                    slash2.setAlignment(Qt.AlignBottom)
                    colon.setAlignment(Qt.AlignBottom)

                    month.setValue(currentMonth)
                    day.setValue(currentDay)

                    year.setMinimum(0)
                    year.setMaximum(9999)
                    year.setValue(currentYear)
                    hour.setValue(12)
                    
                    minute.setValue(00)
                    
                    
                    
                    containerLayout.addWidget(month, alignment=Qt.AlignTop)
                    containerLayout.addWidget(slash1, alignment=Qt.AlignTop)
                    containerLayout.addWidget(day, alignment=Qt.AlignTop)
                    containerLayout.addWidget(slash2, alignment=Qt.AlignTop)
                    containerLayout.addWidget(year, alignment=Qt.AlignTop)
                    containerLayout.addItem(space)
                    containerLayout.addWidget(hour, alignment=Qt.AlignTop)
                    containerLayout.addWidget(colon, alignment=Qt.AlignTop)
                    containerLayout.addWidget(minute, alignment=Qt.AlignTop)
                    containerLayout.addItem(space)
                    containerLayout.addWidget(AMPM, alignment=Qt.AlignTop)

                    
                    containerLayout.setAlignment(Qt.AlignTop)

                    row_layout.addWidget(labelContainer)
                    row_layout.addWidget(dateContainer)
                    
                else:
                    label = QLabel(label_text)
                    row_layout.addWidget(label, alignment=Qt.AlignTop)
                    
                    if label_text == "Information" or label_text == "Notes":
                        entry = QTextEdit()
                        entry.setMaximumHeight(70)
                        row_layout.addWidget(entry, alignment=Qt.AlignTop)
                    else:
                        entry = QLineEdit()
                        row_layout.addWidget(entry, alignment=Qt.AlignTop)

                layout.addWidget(row_widget)

            # Set spacing between rows
            layout.setSpacing(1)
            layout.setAlignment(Qt.AlignTop)

            confirmButton = QPushButton("Confirm")
            row_widget = QWidget()
            row_layout = QVBoxLayout(row_widget)
            row_layout.addWidget(confirmButton)
            layout.addWidget(row_widget)






            

        # Function to be called when the "Close" button is clicked
        def delete_row(row_index):
            # Remove widgets from the row
            for column_index in range(grid_layout.columnCount()):
                item = grid_layout.itemAtPosition(row_index, column_index)
                if item is not None:
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()  # Delete the widget

            # Delay the layout update to ensure widget deletion
            QTimer.singleShot(0, grid_layout.update)

            # Adjust the layout to remove the empty row
            for r in range(row_index + 1, grid_layout.rowCount()):
                for c in range(grid_layout.columnCount()):
                    item = grid_layout.itemAtPosition(r, c)
                    if item is not None:
                        grid_layout.addWidget(item.widget(), r - 1, c)

            # Reduce the row count of the layout
            grid_layout.setRowStretch(grid_layout.rowCount() - 1, 0)
            grid_layout.takeAt(grid_layout.rowCount() - 1)

            # Update the layout to reflect the changes
            grid_layout.update()

        # Connect the button's clicked signal to the new_button function
        button.clicked.connect(new_button)

        # Set the scroll widget as the content of the scroll area
        scroll_area.setWidget(scroll_widget)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        # Set the main widget as the central widget of the main window
        self.setCentralWidget(main_widget)

# Create the main window instance
main_window = MainWindow()
main_window.show()

# Start the event loop
sys.exit(app.exec_())



