import sys
import csv
import platform
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#Colors
redColor = "DB162F"
yellowColor = "FFBA08"
greenColor = "00A676"
foregroundColor = "CABAC8"
backgroundColor = "E8E1EF"

mySystem = ""

if platform.system() == "Darwin":
    mySystem = "macOS":
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

window = QMainWindow()
window.setWindowTitle("Planner")
window.setWindowIcon(QIcon(r"C:\Users\whatk\Downloads\planner.png"))
window.setFixedHeight(600)
window.setFixedWidth(900)

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

with open(filePath, 'w', newline = '') as file:
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

    newWindow = QMainWindow()
    newWindow.setWindowTitle("New")
    newWindow.setWindowIcon(QIcon(r"C:\Users\whatk\Downloads\planner.png"))
    newWindow.setFixedHeight(200)
    newWindow.setFixedWidth(600)
    newWindow.show()
    

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
window.setCentralWidget(main_widget)

# Show the window
window.show()

# Start the event loop
sys.exit(app.exec_())
