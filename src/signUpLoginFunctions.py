import re
import sqlite3
import os
from hashlib import sha256
from settings import DB_DIR, USERS_DB_PATH, PASSWORDS_TABLE, USERS_TABLE
from PyQt6.QtWidgets import QTableWidgetItem, QLabel, QTableView


def sha256Encrypt(text) -> str:
    """SHA256 encryption made simple."""
    encoded_text = text.encode()
    return sha256(encoded_text).hexdigest()


def checkAppDir() -> None:
    """
    Check if the application directory exists.

    If it doesn't, create it. Also, create a user.sqlite database
    that has a table (user, password).
    """
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)

        conn = sqlite3.connect(USERS_DB_PATH)
        cur = conn.cursor()

        cur.execute(f"CREATE TABLE {USERS_TABLE} (user TEXT, password TEXT)")

        conn.commit()
        conn.close()


def isUserExist(username: str) -> bool:
    """Check if user has an account, returns a bool value."""
    conn = sqlite3.connect(USERS_DB_PATH)
    cur = conn.cursor()

    result = list(
        cur.execute(
            f"SELECT * FROM {USERS_TABLE} WHERE user = :username",
            {"username": username},
        ),
    )
    conn.close()

    return False if result == [] else True


def getPasswordsFromDatabase(dbPath: str) -> list:
    """Get a user's passwords from database."""
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()

    data = list(cur.execute(f'SELECT * FROM {PASSWORDS_TABLE}'))

    conn.close()

    return data


def isPasswordValid(password: str) -> bool:
    '''Check if a password is valid.'''
    result = re.search(r'^[ -~]{8,}$', password)
    return False if result is None else True

def setPasswordsInTable(data: list,
                        itemBasedQTableView: QTableView
                        ) -> None:
    itemBasedQTableView.setRowCount(len(data))
    for i, d in enumerate(data):
        # Description
        itemBasedQTableView.setItem(i, 0, QTableWidgetItem(d[0]))
        # Password
        itemBasedQTableView.setItem(i, 1, QTableWidgetItem(d[1]))

def updateTable(username: str, itemBasedQTableView: QTableView) -> None:
    dbPath = f"{DB_DIR}/{username}.sqlite"
    data = getPasswordsFromDatabase(dbPath)
    setPasswordsInTable(data, itemBasedQTableView)
    data = None

def submitLogin(username: str,
                password: str,
                errorsLabel: QLabel,
                itemBasedQTableView: QTableView
                ) -> bool:
    """Login if credentials are valid."""
    validLogin = True
    if username == '' or password == '':
        validLogin = False
        errorsLabel.setText('Missing information')
    elif not isUsernameValid(username) \
         or not isPasswordValid(password) \
         or not os.path.exists(USERS_DB_PATH):
        validLogin = False
        errorsLabel.setText('Username or password is incorrect.')
    else:
        encrypted_password = sha256Encrypt(password)
        conn = sqlite3.connect(USERS_DB_PATH)
        cur = conn.cursor()

        result = list(
            cur.execute(
                f"SELECT * FROM {USERS_TABLE} WHERE user = :username AND password = :password",
                {"username": username, "password": encrypted_password},
            ),
        )
        conn.close()

        if result == []:
            errorsLabel.setText("Invalid username or password")
            validLogin = False
        else:
            updateTable(username, itemBasedQTableView)
    return validLogin


def isUsernameValid(username: str) -> bool:
    """
    Check if username is valid.

    Usernames must be at least 4 characters long,
    and should include only letters, digits and underscores.
    They also have to begin with a letter.
    Returns a boolean value.
    """
    username = username.strip()
    result = re.search(r'^[a-zA-Z]\w{3,}$', username, flags=re.ASCII)
    return False if result is None else True

def isPasswordAndConfirmationValid(password: str,
                                   confirmation: str,
                                   errorsLabel: QLabel) -> bool:
    """Check if password is valid and wether the confirmation match."""
    if isPasswordValid(password) and password == confirmation:
        errorsLabel.setText('')
        return True
    else:
        errorsLabel.setText('Invalid password.')
        return False

def makeUserDb(username: str) -> None:
    """Create a database for the user, and create a passwords table."""
    dbPath = f"{DB_DIR}/{username}.sqlite"

    try:
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()

        cur.execute(
            f"CREATE TABLE {PASSWORDS_TABLE} (description TEXT, password TEXT)")

        conn.commit()
    finally:
        conn.close()


def addUser(username: str, password: str) -> None:
    """Add user to the users database."""
    encrypted_password = sha256Encrypt(password)

    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO {USERS_TABLE} VALUES (?, ?)",
            (username, encrypted_password),
        )
        conn.commit()
    finally:
        conn.close()


def submitSignUp(username: str,
                 password: str,
                 confirmation: str,
                 errorsLabel: QLabel
                 ) -> bool:
    """Sign up if everything is valid."""
    validSignUp = True
    if username == '' or password == '' or confirmation == '':
        validSignUp = False
        errorsLabel.setText('Missing information')
    else:
        if isUsernameValid(username) and \
           isPasswordAndConfirmationValid(password, confirmation, errorsLabel):
            checkAppDir()
            if isUserExist(username):
                errorsLabel.setText('Username already taken')
                validSignUp = False
            else:
                makeUserDb(username)
                addUser(username, password)
        else:
            errorsLabel.setText('Invalid username or password')
            validSignUp = False
    return validSignUp


def addPassword(username: str, description: str, password: str) -> None:
    dbPath = f"{DB_DIR}/{username}.sqlite"
    if os.path.exists(dbPath):
        try:
            conn = sqlite3.connect(dbPath)
            cur = conn.cursor()

            cur.execute(
                f"INSERT INTO {PASSWORDS_TABLE} (description, password) VALUES ('{description}', '{password}')"
            )

            conn.commit()
        finally:
            conn.close()
