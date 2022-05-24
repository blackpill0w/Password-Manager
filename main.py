from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFrame, QPushButton, QLabel, QLineEdit, QTableView)
from PyQt6.uic import loadUi
import sys
from signUpFunctions import (checkAppDir, addUser, isUsernameValid, isPasswordAndConfirmationValid,
    submitSignUp, makeUserDb, submitLogin)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi('mainWindow.ui', self)

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

        self.show()

    def _login(self, usernameLineEdit, passwordLineEdit, loginErrorsLabel):
        # Check that username and password are valid
        username = usernameLineEdit.text()
        password = passwordLineEdit.text()
        
        if submitLogin(username, password, loginErrorsLabel):
            print('here')
            usernameLineEdit.setText('')
            passwordLineEdit.setText('')
            self._changeActiveFrame(
                    self.loginFrame, self.loggedInFrame, f'Password Manager - {username}'
                )

    def _loadLoginWindowVars(self):
        # Login Frame
        self.loginFrame = loadUi('loginFrame.ui')
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
        self.goBackButton.clicked.connect(lambda: self._changeActiveFrame(
            self.loginFrame, self.initialFrame, 'Password Manager'))
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
        
        if submitSignUp(username, password, self.signUpErrorsLabel):
            # Remove the credentials
            lineEditsToClear = []# [usernameLineEdit, passwordLineEdit, confirmationLineEdit,]
    
            self._changeActiveFrame(
                self.signUpFrame, self.loggedInFrame, f'Password Manager - {username}', lineEditsToClear
            )

    def _loadSignUpWindowVars(self):
        # Sign Up Frame
        self.signUpFrame = loadUi('signUpFrame.ui')
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

    def _loadLoggedInWindowVars(self):
        # Logged In Frame
        self.loggedInFrame = loadUi('loggedInFrame.ui')
        # Add Password Button
        self.addPasswordButton = self.loggedInFrame.findChild(
            QPushButton, name='addPasswordButton')
        # TODO
        # Log Out Button
        self.logOutButton = self.loggedInFrame.findChild(
            QPushButton, name='logOutButton')
        # TODO
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

    def _changeActiveFrame(self, frameToHide, frameToShow, newWindowTitle=None, lineEditsToClear=None):
        if type(lineEditsToClear) is list:
            for e in lineEditsToClear:
                e.setText('')
        if newWindowTitle is not None:
            self.setWindowTitle(newWindowTitle)
        frameToHide.hide()
        frameToShow.setParent(self)
        frameToShow.show()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
