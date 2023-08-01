import sys
import csv
import platform
import re
import datetime
from dateutil.relativedelta import relativedelta
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

mainCSVFilePath = r"C:\Users\whatk\Desktop\planner\info.csv"

plannerPicturePath = r"C:\Users\whatk\Downloads\planner.png"

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

previousRadioButton = None
# Function to be called when the check timer times out

filePath = "info.csv"
existingData = []

# WITH WRITING STUFF I SHOULD USE APPEND
def get_last_entry_id(csv_file_path):
    last_entry_id = None

    # Open the CSV file in read mode
    with open(csv_file_path, mode="r", newline="") as file:
        reader = csv.reader(file)

        # Skip the header row
        header_row = next(reader)

        # Read and process each row of data from the CSV file
        for row in reader:
            last_entry_id = int(row[0])  # Assuming the ID is in the first column (index 0)

    return last_entry_id if last_entry_id is not None else 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Planner")
        self.setWindowIcon(QIcon(plannerPicturePath))
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
        newButton = QPushButton("New")
        heading_layout.addWidget(newButton)
        
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
        data2 = [ 
            ['ID', 'Month', 'Day', 'Year', 'Hour', 'Month', 'AMPM', 'Subject', 'Information', 'Notes', 'Importance']
        ]
        filePath = mainCSVFilePath

        """
        with open(filePath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data2)
        print("Created CSV successfully.")
        """

        # Function to be called when the button is clicked
        def new_button():

            if hasattr(self, "new_window") and self.new_window is not None:
                
                # Window already exists, bring it to the front
                self.new_window.showNormal()
                self.new_window.activateWindow()
            else:
                #NEW WINDOW
                self.new_window = QMainWindow()  # Store the new window as an instance variable
                self.new_window.setWindowTitle("New")
                self.new_window.setWindowIcon(QIcon(plannerPicturePath))

                self.new_window.setFixedHeight(215)
                self.new_window.setFixedWidth(1150)
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
                    labelIndex = new_labels.index(label_text)

    #MM/DD/YYYY HH:MM AM/PM
                    if label_text == "Due Date":
                        
                        class MinuteSpinBox(QSpinBox):
                            def textFromValue(self, value):
                                return  "{:02d}", format(value)
 
                        #labelContainer = QWidget()
                        #labelLayout = QVBoxLayout(labelContainer)
                        dueLabel = QLabel(label_text+ " (defaults to current date)")
                        
                        customDate = QWidget()
                        dateGrid = QGridLayout(customDate)

                        monthLabel = QLabel("MM")
                        slash1Label = QLabel("/")
                        dateLabel = QLabel("DD")
                        slash2Label = QLabel("/")
                        yearLabel = QLabel("YYYY")
                        hourLabel = QLabel("HH")
                        colonLabel = QLabel(":")
                        minuteLabel = QLabel("MM")
                        AMPMLabel = QLabel("AM/PM")
                        space = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                        dateLabels = [monthLabel,slash1Label, dateLabel, slash2Label,yearLabel,space, hourLabel,colonLabel,minuteLabel,space,AMPMLabel]

                        dateGrid.addWidget(dueLabel, 0,0,1, len(dateLabels))
                        dateGrid.setAlignment(dueLabel, Qt.AlignCenter)
                        for index in range(len(dateLabels)):
                            label = dateLabels[index]
                            if label == space:
                                dateGrid.addItem(label, 1, index)
                                
                            else:
                                dateGrid.addWidget(label, 1, index)
                                dateGrid.setAlignment(label, Qt.AlignCenter)

                        dateWidget = QWidget()
                        dateWidget.setLayout(dateGrid)

                        AMPMLabel.setMinimumHeight(20)
                        
                        #row_layout.addWidget(labelContainer)
                        row_layout.setAlignment(Qt.AlignTop)
                        row_layout.addWidget(dateWidget)

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
                        hour.setMaximum(12)
                        hour.setMinimum(1)

                        minute.setMinimum(0)
                        minute.setMaximum(5)
                        minute.setDisplayIntegerBase(10)
                        minute.setSuffix("0")
                        minute.setValue(0)

                        month.setMinimumWidth(25)
                        day.setMinimumWidth(25)
                        year.setMinimumWidth(37)
                        hour.setMinimumWidth(25)
                        minute.setMinimumWidth(25)

                        spinboxes = [month, day, year, hour, minute]
                        for items in spinboxes:
                            items.setButtonSymbols(QAbstractSpinBox.NoButtons)
                            line_edit = items.findChild(QLineEdit)
                            if line_edit:
                                line_edit.setAlignment(Qt.AlignCenter)
                        
                        minute.setButtonSymbols(QAbstractSpinBox.PlusMinus)

                        dateWidgets = [month,slash1,day,slash2,year, space, hour, colon, minute, space, AMPM]
                        for index in range(len(dateWidgets)):
                            label = dateWidgets[index]
                            
                            if label == space:
                                dateGrid.addItem(label, 2, index)
                                
                            else:
                                dateGrid.addWidget(label, 2, index)
                                dateGrid.setAlignment(label, Qt.AlignCenter)
                        


                        #Radio Buttons
                        customDueDate = QRadioButton("Custom Due Date") #Default
                        oneWeekDue = QRadioButton("Due in 1 Week")
                        oneMonthDue = QRadioButton("Due in 1 Month")
                        noDueDate = QRadioButton("No Due Date")
                        noDueDateBool = False
                        customDueDate.setChecked(True)
                        buttonChecked = "customDueDate"
                        global previousRadioButton
                        previousRadioButton = customDueDate.text()
                        dateGrid.addWidget(customDueDate, 3, 2, 1,3)
                        dateGrid.addWidget(oneWeekDue, 3, 6, 1,3)
                        dateGrid.addWidget(oneMonthDue, 4, 2, 1,3)
                        dateGrid.addWidget(noDueDate, 4, 6, 1,3)


                        
                        
                        tempMonthValue = 0
                        tempDayValue = 0
                        tempYearValue = 0
                        tempHourValue = 0
                        tempMinuteValue = 0
                        tempAMPMValue = 0
                        AMPMIndex = 0
                        def handle_radio_button_change(checked, text):
                            global previousRadioButton, tempMonthValue, tempDayValue, tempYearValue, tempHourValue, tempMinuteValue, tempAMPMValue, AMPMIndex, buttonChecked
                            
                            if checked and previousRadioButton == customDueDate.text():
                                print("was custom due date")    
                                tempMonthValue = month.value()
                                tempDayValue = day.value()
                                tempYearValue = year.value()
                                tempHourValue = hour.value()
                                tempMinuteValue = minute.value()
                                tempAMPMValue = AMPM.currentText()
                                buttonChecked = "customDueDate"
                                values = [tempMonthValue, tempDayValue, tempYearValue, tempHourValue, tempMinuteValue, tempAMPMValue]
                                if tempAMPMValue ==  "AM":
                                    AMPMIndex = 0
                                else:
                                    AMPMIndex = 1
                                for value in values:
                                    print(value)
                            if checked and previousRadioButton != text:
                                # Radio button state has changed
                                previousRadioButton = text
                                print(f"Radio button changed: {text}")
                            if checked  and text ==customDueDate.text():
                                month.setEnabled(True)
                                day.setEnabled(True)
                                year.setEnabled(True)
                                hour.setEnabled(True)
                                minute.setEnabled(True)
                                AMPM.setEnabled(True)
                                month.setValue(tempMonthValue)
                                day.setValue(tempDayValue)
                                year.setValue(tempYearValue)
                                hour.setValue(tempHourValue)
                                minute.setValue(tempMinuteValue)
                                AMPM.setCurrentIndex(AMPMIndex)
                                values = [tempMonthValue, tempDayValue, tempYearValue, tempHourValue, tempMinuteValue, tempAMPMValue]
                                for value in values:
                                    print(value)
                            if checked and text == noDueDate.text():
                                noDueDateBool = True
                                month.setEnabled(False)
                                day.setEnabled(False)
                                year.setEnabled(False)
                                hour.setEnabled(False)
                                minute.setEnabled(False)
                                AMPM.setEnabled(False)
                                buttonChecked = "noDueDate"
                            if checked and text == oneWeekDue.text():
                                
                                month.setEnabled(True)
                                day.setEnabled(True)
                                year.setEnabled(True)
                                hour.setEnabled(True)
                                minute.setEnabled(True)
                                AMPM.setEnabled(True)

                                buttonChecked = "oneWeekDue"

                                current_date = datetime.date.today()

                                # Add one week to the current date
                                one_week_later = current_date + datetime.timedelta(weeks=1)

                                oneWeekYear = one_week_later.year
                                oneWeekMonth = one_week_later.month
                                oneWeekDay = one_week_later.day
                                month.setValue(oneWeekMonth)
                                day.setValue(oneWeekDay)
                                year.setValue(oneWeekYear)

                            if checked and text == oneMonthDue.text():
                                month.setEnabled(True)
                                day.setEnabled(True)
                                year.setEnabled(True)
                                hour.setEnabled(True)
                                minute.setEnabled(True)
                                AMPM.setEnabled(True)

                                buttonChecked = "oneMonthDue"

                                current_date = datetime.date.today()

                                # Add one month to the current date
                                one_month_later = current_date + relativedelta(months=1)

                                oneMonthYear = one_month_later.year
                                oneMonthMonth = one_month_later.month
                                oneMonthDay = one_month_later.day
                                month.setValue(oneMonthMonth)
                                day.setValue(oneMonthDay)
                                year.setValue(oneMonthYear)

                        
                        customDueDate.toggled.connect(lambda checked: handle_radio_button_change(checked, "Custom Due Date"))
                        oneWeekDue.toggled.connect(lambda checked: handle_radio_button_change(checked, "Due in 1 Week"))
                        oneMonthDue.toggled.connect(lambda checked: handle_radio_button_change(checked, "Due in 1 Month"))
                        noDueDate.toggled.connect(lambda checked: handle_radio_button_change(checked, "No Due Date"))

                        
                        containerLayout.setAlignment(Qt.AlignTop)
                        if customDueDate.isChecked():
                            # Custom Due Date is checked
                            print("Custom Due Date is selected")
                        elif oneWeekDue.isChecked():
                            # Due in 1 Week is checked
                            print("Due in 1 Week is selected")
                        elif oneMonthDue.isChecked():
                            # Due in 1 Month is checked
                            print("Due in 1 Month is selected")
                        elif noDueDate.isChecked():
                            # No Due Date is checked
                            print("No Due Date is selected")





                        #row_layout.addWidget(labelContainer)
                        #row_layout.addWidget(dateContainer)
                        
                        
                        
                        
                        
                    else:
                        
                        label = QLabel(label_text)
                        dateGrid.addWidget(label, 0, labelIndex + 10+labelIndex)
                        #print(labelIndex+labelIndex+10)
                        
                        if label_text == "Information" or label_text == "Notes":
                            if label_text == "Information":
                                information = QTextEdit()
                                
                                information.setMinimumHeight(50)
                                dateGrid.addWidget(information, 1, labelIndex + 10+labelIndex,3,1)
                            else:
                                notes = QTextEdit()
                                
                                notes.setMinimumHeight(50)
                                dateGrid.addWidget(notes, 1, labelIndex + 10+labelIndex,3,1)
                            
                        elif label_text == "Importance":
                            importance = QDoubleSpinBox()
                            importance.setMaximum(10.0)
                            importance.setMinimum(0.0)
                            importance.setValue(5.0)
                            importance.setSingleStep(0.1)
                            importance.setDecimals(1)
                            dateGrid.addWidget(importance, 1, labelIndex + 10+labelIndex)
                        else:
                            subject = QLineEdit()
                            
                            dateGrid.addWidget(subject, 1, labelIndex + 10+labelIndex)

                    layout.addWidget(row_widget)
                spacer = QSpacerItem(30, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
                spacerIndex = 11
                for i in range(4):
                    dateGrid.addItem(spacer, 0, spacerIndex)
                    spacerIndex =  spacerIndex+2

                # Set spacing between rows
                layout.setSpacing(1)
                layout.setAlignment(Qt.AlignTop)

                #print(dateGrid.rowCount())
                #print(dateGrid.columnCount())
                def close_window():
                    information.setText("")
                    notes.setText("")
                    importance.setValue(5)
                    subject.setText("")
                    self.new_window.close()
                
                def new_row():
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

                def confirmInfo():
                    
                    global monthValue, dayValue, yearValue, hourValue, minuteValue, AMPMValue
                    monthValue = month.value()
                    dayValue = day.value()
                    yearValue = year.value()
                    hourValue = hour.value()
                    minuteValue = minute.value()
                    AMPMValue = AMPM.currentText()
                    confirmValues = [monthValue, dayValue, yearValue, hourValue, minuteValue, AMPMValue]
                    subjectValue = subject.text()
                    infoValue = information.toPlainText()
                    notesValue = notes.toPlainText()
                    importanceValue = importance.value()

                    print(buttonChecked)
                    if buttonChecked == "customDueDate" or buttonChecked == "oneWeekDue" or buttonChecked == "oneMonthDue":
                        monthValue = month.value()
                        dayValue = day.value()
                        yearValue = year.value()
                        hourValue = hour.value()
                        minuteValue = minute.value()
                        AMPMValue = AMPM.currentText()
                        
                    elif buttonChecked == "noDueDate":
                        monthValue = "N/A"
                        dayValue = "N/A"
                        yearValue = "N/A"
                        hourValue = "N/A"
                        minuteValue = "N/A"
                        AMPMValue = "N/A"
                    for value in confirmValues:
                        print(value)
                    lastID = get_last_entry_id(filePath)
                    newID = lastID + 1
                    with open(filePath, mode="a", newline="") as file:
                        # Create a CSV writer
                        writer = csv.writer(file)

                        # Write the data to the CSV file
                        writer.writerow([newID, monthValue, dayValue, yearValue, hourValue, minuteValue, AMPMValue, subjectValue, infoValue, notesValue, importanceValue])


                confirmButton = QPushButton("Confirm")
                #row_widget = QWidget()
                #row_layout = QVBoxLayout(row_widget)
                confirmButton.clicked.connect(confirmInfo)
                confirmButton.clicked.connect(new_row)
                confirmButton.clicked.connect(close_window)
                dateGrid.addWidget(confirmButton, 1, 21)
                confirmButton.setMinimumHeight(40)
                
                cancelButton = QPushButton("Cancel")
                dateGrid.addWidget(cancelButton, 3, 21)
                cancelButton.setMinimumHeight(40)
                dateGrid.addItem(QSpacerItem(20,20,QSizePolicy.Minimum, QSizePolicy.Expanding), 0,20)
                cancelButton.clicked.connect(close_window)
                #layout.addWidget(row_widget)

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
        newButton.clicked.connect(new_button)

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