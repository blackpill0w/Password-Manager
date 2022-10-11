import sys
import os
from signUpLoginFunctions import submitSignUp, submitLogin, addPassword, updateTable
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QFrame,
        QPushButton, QLabel, QLineEdit, QTableView,
        QWidget
    )
    from PyQt6.uic.load_ui import loadUi
except ModuleNotFoundError:
    import subprocess
    print('Installing dependencies (PyQt5)...')
    reqs_file = os.path.join(__file__.split('src')[0], 'requirements.txt')
    try:
        subprocess.run(['pip3', '-r', reqs_file])
    except FileNotFoundError as e:
        if e.filename == 'pip3':
            print("Couldn't find the command 'pip',\
                  please make sure it is installed and try again.")
        elif e.filename == reqs_file:
            print("Couldn't find the requirements file 'requirements.txt',\
            try installing PyQt6 manually\
            or put 'pyqt6' in '/path/to/project/src/requirements.txt'")
        exit(1)

ROOT_DIR = __file__.split('src')[0] # project dir
UI_FILES_DIR = os.path.join(ROOT_DIR, 'UI')
MAIN_WIN_UI_FILE = os.path.join(UI_FILES_DIR, 'mainWindow.ui')
LOGIN_UI_FILE = os.path.join(UI_FILES_DIR, 'loginFrame.ui')
SIGN_UP_UI_FILE = os.path.join(UI_FILES_DIR, 'signUpFrame.ui')
LOGGED_IN_UI_FILE = os.path.join(UI_FILES_DIR, 'loggedInFrame.ui')
ADD_PASS_UI_FILE = os.path.join(UI_FILES_DIR, 'addPasswordWin.ui')

class AddPasswordWindow(QWidget):
    def __init__(self, username: str, passwordsTable: QTableView):
        self.username = username
        self.table = passwordsTable

        super().__init__()
        loadUi(ADD_PASS_UI_FILE, self)

        self.descriptionLE = self.findChild(QLineEdit, name='descriptionLE')
        self.passwordLE = self.findChild(QLineEdit, name='passwordLE')
        self.saveButton = self.findChild(QPushButton, name='saveButton')
        self.saveButton.clicked.connect(self._addPassword)

        self.show()

    def _clearLE(self):
        self.descriptionLE.setText('')
        self.passwordLE.setText('')

    def _addPassword(self):
        addPassword(self.username,
                    self.descriptionLE.text(),
                    self.passwordLE.text()
                    )
        self._clearLE()
        updateTable(self.username, self.table)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(MAIN_WIN_UI_FILE, self)

        self.loggedUser = None

        self.initialFrame = self.findChild(QFrame, name='initialFrame')
        # Login Button
        self.loginButton = self.findChild(QPushButton, name='loginButton')
        self.loginButton.clicked.connect(lambda: self._changeActiveFrame(
            self.initialFrame, self.loginFrame, 'Log In'))
        # Sign Up Button
        self.signUpButton = self.findChild(QPushButton, name='signUpButton')
        self.signUpButton.clicked.connect(lambda: self._changeActiveFrame(
            self.initialFrame, self.signUpFrame, 'Sign Up'))

        self._loadLoginWindowVars()
        self._loadSignUpWindowVars()
        self._loadLoggedInWindowVars()

        # Line Edits that get cleared
        # whenever we switch from login to signup, etc
        self.widgetsToClear = [
            self.loginUsernameLineEdit,
            self.loginPasswordLineEdit,
            self.loginErrorsLabel,
            self.signUpUsernameLineEdit,
            self.signUpPasswordLineEdit,
            self.signUpPasswordConfirmationLineEdit,
            self.signUpErrorsLabel,
        ]

        self.show()

    def _login(self, usernameLineEdit, passwordLineEdit, loginErrorsLabel):
        # Check that username and password are valid
        username = usernameLineEdit.text()
        password = passwordLineEdit.text()

        if submitLogin(username, password, loginErrorsLabel, self.dataTable):
            self.loggedUser = username
            self._changeActiveFrame(
                self.loginFrame, self.loggedInFrame,
                f'Password Manager - {username}',
            )


    def _loadLoginWindowVars(self):
        # Login Frame
        self.loginFrame = loadUi(LOGIN_UI_FILE)
        # Username Line Edit
        self.loginUsernameLineEdit = self.loginFrame.findChild(
            QLineEdit, name='usernameLineEdit')
        # Password Line Edit
        self.loginPasswordLineEdit = self.loginFrame.findChild(
            QLineEdit, name='passwordLineEdit')
        # Submit Button
        self.loginSubmitButton = self.loginFrame.findChild(
            QPushButton, name='submitLoginButton')
        self.loginSubmitButton.clicked.connect(
            lambda:
                self._login(
                    self.loginUsernameLineEdit,
                    self.loginPasswordLineEdit,
                    self.loginErrorsLabel
                )
        )
        # Go Back Button
        self.goBackButton = self.loginFrame.findChild(
            QPushButton, name='goBackButton')
        self.goBackButton.clicked.connect(
            lambda:
                self._changeActiveFrame(
                    self.loginFrame,
                    self.initialFrame,
                    'Password Manager'
                )
        )
        # Errors Label
        self.loginErrorsLabel = self.loginFrame.findChild(
            QLabel, name='errorsLabel')
        self.loginErrorsLabel.setText('')
        self.loginErrorsLabel.setStyleSheet('color: red')

    def _signUp(self, usernameLineEdit, passwordLineEdit, confirmationLineEdit):
        # Check that username and password are valid
        username = usernameLineEdit.text()
        password = passwordLineEdit.text()
        confirmation = confirmationLineEdit.text()

        if submitSignUp(username, password, confirmation, self.signUpErrorsLabel):
            self.loggedUser = username
            self._changeActiveFrame(
                self.signUpFrame, self.loggedInFrame,
                f'Password Manager - {username}'
            )

    def _loadSignUpWindowVars(self):
        # Sign Up Frame
        self.signUpFrame = loadUi(SIGN_UP_UI_FILE)
        # Username Line Edit
        self.signUpUsernameLineEdit = self.signUpFrame.findChild(
            QLineEdit, name='usernameLineEdit')
        # Password Line Edit
        self.signUpPasswordLineEdit = self.signUpFrame.findChild(
            QLineEdit, name='passwordLineEdit')
        # Password Confirmation Line Edit
        self.signUpPasswordConfirmationLineEdit = self.signUpFrame.findChild(
            QLineEdit, name='passwordConfimationLineEdit')
        # Submit Button
        self.signUpSubmitButton = self.signUpFrame.findChild(
            QPushButton, name='submitSignUpButton')
        self.signUpSubmitButton.clicked.connect(
            lambda: self._signUp(
                self.signUpUsernameLineEdit,
                self.signUpPasswordLineEdit,
                self.signUpPasswordConfirmationLineEdit
            ))
        # Go Back Button
        self.goBackButton = self.signUpFrame.findChild(
            QPushButton, name='goBackButton')
        self.goBackButton.clicked.connect(lambda: self._changeActiveFrame(
            self.signUpFrame, self.initialFrame, 'Password Manager'))
        # Errors Label
        self.signUpErrorsLabel = self.signUpFrame.findChild(
            QLabel, name='errorsLabel')

        self.signUpErrorsLabel.setText('')
        self.signUpErrorsLabel.setStyleSheet('color: red')

    def _logout(self):
        self.loggedUser = None
        self.dataTable.clear()
        self._changeActiveFrame(
            self.loggedInFrame, self.initialFrame, 'Password Manager'
        )
    def _addPasswordWin(self):
        self.tempwin = AddPasswordWindow(self.loggedUser, self.dataTable)
    def _loadLoggedInWindowVars(self):
        # Logged In Frame
        self.loggedInFrame = loadUi(LOGGED_IN_UI_FILE)
        # Add Password Button
        self.addPasswordButton = self.loggedInFrame.findChild(
            QPushButton, name='addPasswordButton')
        self.addPasswordButton.clicked.connect(self._addPasswordWin)
        # Log Out Button
        self.logOutButton = self.loggedInFrame.findChild(
            QPushButton, name='logOutButton')
        self.logOutButton.clicked.connect(
            lambda:
                self._changeActiveFrame(
                    self.loggedInFrame,
                    self.initialFrame,
                    'Password Manager'
                )
        )
        # Table To Show Passwords
        self.dataTable = self.loggedInFrame.findChild(QTableView, 'dataTable')
        self.dataTable.setColumnWidth(0, 380)
        self.dataTable.setColumnWidth(1, 300)

    def _changeActiveFrame(self, frameToHide, frameToShow, newWindowTitle=None):
        for i in self.widgetsToClear:
            i.setText('')
        if newWindowTitle is not None:
            self.setWindowTitle(newWindowTitle)
        frameToHide.hide()
        frameToShow.setParent(self)
        frameToShow.show()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
