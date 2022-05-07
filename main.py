from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QLabel, QLineEdit
from PyQt6.uic import loadUi
import sys


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

        self.show()

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
        # Go Back Button
        self.goBackButton = self.loginFrame.findChild(
            QPushButton, name='goBackButton')
        self.goBackButton.clicked.connect(lambda: self._changeActiveFrame(
            self.loginFrame, self.initialFrame, 'Password Manager'))
        # Errors Label
        self.loginErrorsLabel = self.loginFrame.findChild(
            QLabel, name='errorsLabel')
        self.loginErrorsLabel.setText('')

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
        self.signUpPasswordLineEdit = self.signUpFrame.findChild(
            QLineEdit, name='passwordConfimationLineEdit')
        # Submit Button
        self.signUpSubmitButton = self.signUpFrame.findChild(
            QPushButton, name='submitSignUpButton')
        # Go Back Button
        self.goBackButton = self.signUpFrame.findChild(
            QPushButton, name='goBackButton')
        self.goBackButton.clicked.connect(lambda: self._changeActiveFrame(
            self.signUpFrame, self.initialFrame, 'Password Manager'))
        # Errors Label
        self.signUpErrorsLabel = self.signUpFrame.findChild(
            QLabel, name='errorsLabel')
        self.signUpErrorsLabel.setText('')

    def _changeActiveFrame(self, frameToHide, frameToShow, newWindowTitle):
        frameToHide.hide()
        frameToShow.setParent(self)
        frameToShow.show()
        self.setWindowTitle(newWindowTitle)


app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())
