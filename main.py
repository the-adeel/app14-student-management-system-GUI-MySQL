import sys
import mysql.connector
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (QMainWindow, QTableWidget, QStatusBar, QToolBar, QApplication, QTableWidgetItem, QDialog,
                             QMessageBox, QPushButton, QVBoxLayout, QLineEdit, QComboBox, QGridLayout, QLabel)

mysql_username=""
mysql_password=""

class DatabaseConnection:
    def __init__(self, host="localhost", user=mysql_username, password=mysql_password, database="school"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        return connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        #Setting the height and Width of the Program
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)

        #Creating instances for menu bar
        file_menu = self.menuBar().addMenu("&File")
        edit_menu = self.menuBar().addMenu("&Edit")
        help_menu = self.menuBar().addMenu("&Help")

        #Creating actions for the menu bars
        search_action = QAction(QIcon("icons/icons/search.png"),"Search", self)
        add_student_action = QAction(QIcon("icons/icons/add.png"),"Add Student", self)
        refresh_action = QAction(QIcon("icons/icons/refresh.png"), "Refresh", self)
        about_action = QAction("About", self)

        #Assigning actions to menu bars
        file_menu.addAction(add_student_action)
        file_menu.addAction(refresh_action)
        edit_menu.addAction(search_action)
        help_menu.addAction(about_action)

        #Actions Triggered
        add_student_action.triggered.connect(self.add_student)
        about_action.triggered.connect(self.about)
        search_action.triggered.connect(self.search)
        refresh_action.triggered.connect(self.load_data)

        #Creating toolbar
        tool_bar = QToolBar()
        tool_bar.setMovable(True)
        self.addToolBar(tool_bar)

        #Adding icons to toolbar
        tool_bar.addAction(search_action)
        tool_bar.addAction(add_student_action)
        tool_bar.addAction(refresh_action)

        #MAIN TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Phone Number"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

        #Creating status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.table.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        pass
        self.table.setRowCount(0)
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        results = cursor.fetchall()
        for row, row_data in enumerate(results):
            self.table.insertRow(row)
            for column, data in enumerate(row_data):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

    def cell_clicked(self):
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def add_student(self):
        dialog = InsertDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def search(self):
        dialog = Search()
        dialog.exec()

    def about(self):
        about_dialog = About()
        about_dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        layout = QVBoxLayout()

        self.setFixedWidth(300)
        self.setFixedHeight(300)


        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Name")
        layout.addWidget(self.name_edit)

        self.course_select = QComboBox()
        self.course_select.addItems(["Astronomy", "Biology", "Math", "Physics"])
        layout.addWidget(self.course_select)

        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Phone Number")
        layout.addWidget(self.phone_edit)

        insert_button = QPushButton("Insert")
        insert_button.clicked.connect(self.add_data)
        layout.addWidget(insert_button)

        self.setLayout(layout)

    def add_data(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        name = self.name_edit.text()
        course = self.course_select.currentText()
        number = self.phone_edit.text()
        cursor.execute("INSERT INTO students (name,course,mobile) VALUES(%s,%s,%s)", (name, course, number))
        connection.commit()
        connection.close()
        main_window.load_data()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")
        layout = QVBoxLayout()

        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.index = main_window.table.currentRow()

        name = main_window.table.item(self.index,1).text()
        self.name_edit = QLineEdit(name)
        self.name_edit.setPlaceholderText("Name")
        layout.addWidget(self.name_edit)

        course = main_window.table.item(self.index,2).text()
        self.course_select = QComboBox()
        self.course_select.addItems(["Astronomy", "Biology", "Math", "Physics"])
        self.course_select.setCurrentText(course)
        layout.addWidget(self.course_select)

        phone = main_window.table.item(self.index, 3).text()
        self.phone_edit = QLineEdit(phone)
        self.phone_edit.setPlaceholderText("Phone Number")
        layout.addWidget(self.phone_edit)

        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_data)
        layout.addWidget(update_button)

        self.setLayout(layout)

    def update_data(self):
        name = self.name_edit.text()
        course = self.course_select.currentText()
        number = self.phone_edit.text()
        id = main_window.table.item(self.index, 0).text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = %s,course = %s,mobile = %s WHERE ID = %s", (name, course, number, id))
        connection.commit()
        connection.close()
        main_window.load_data()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Confirmation")
        grid = QGridLayout()
        confirm_label = QLabel("Are you sure you want to delete this data ?")
        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.delete)
        no_button = QPushButton("No")
        no_button.clicked.connect(self.close)

        grid.addWidget(confirm_label,0,0,1,2)
        grid.addWidget(yes_button,1,0)
        grid.addWidget(no_button,1,1)

        self.setLayout(grid)

    def delete(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index,0).text()
        cursor.execute("DELETE FROM students WHERE id = %s",(student_id,))
        connection.commit()
        main_window.load_data()
        cursor.close()
        connection.close()
        self.close()

        message_box = QMessageBox()
        message_box.setWindowTitle("Success")
        message_box.setText("Student data has been deleted successfully.")
        message_box.exec()

class Search(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        layout = QVBoxLayout()

        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search")

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student)

        layout.addWidget(self.search_box)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search_student(self):
        name = self.search_box.text()
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

class About(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """"
        This app can be used to manage student data. People are allowed to use it and customize it for their own use.
        """
        self.setText(content)

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())