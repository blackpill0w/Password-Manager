import re
import sqlite3
import os
from hashlib import sha256
from settings import DB_DIR, USERS_DB_PATH, PASSWORDS_TABLE, USERS_TABLE
from PyQt6.QtWidgets import QTableWidgetItem


def sha256Encrypt(text) -> str:
    """SHA256 encryption made simple."""
    encoded_text = text.encode()
    return sha256(encoded_text).hexdigest()


def checkAppDir():
    """Check if the application directory (usually named npassword_manager) exists.
    If it doesn't, create it. Also, create a user.sqlite database that has a table (user, password).
    """
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)

        conn = sqlite3.connect(USERS_DB_PATH)
        cur = conn.cursor()

        cur.execute(f"CREATE TABLE {USERS_TABLE} (user TEXT, password TEXT)")

        conn.commit()
        conn.close()


def isUserExist(username):
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


def getPasswordsFromDatabase(dbPath) -> list:
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()

    data = list(cur.execute(f'SELECT * FROM {PASSWORDS_TABLE}'))

    conn.close()

    return data


def submitLogin(username, password, errorsLabel, itemBasedQTableView) -> bool:
    # Var to be returned
    validLogin = True
    if username == '' or password == '':
        validLogin = False
        errorsLabel.setText('Missing information')
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
            dbPath = f"{DB_DIR}/{username}.sqlite"
            data = getPasswordsFromDatabase(dbPath)
            for i, d in enumerate(data):
                # Increment the number of rows
                itemBasedQTableView.setRowCount(itemBasedQTableView.rowCount()+1)
                # Description
                itemBasedQTableView.setItem(i, 0, QTableWidgetItem(d[0]))
                # Password
                itemBasedQTableView.setItem(i, 1, QTableWidgetItem(d[1]))
    return validLogin


def isUsernameValid(username, errorsLabel) -> bool:
    """
    Check if username is valid.
    Usernames must be at least 4 characters long,
    and should include only letters, digits and underscores.
    They also have to begin with a letter.
    Returns a boolean value.
    """
    username = username.strip()
    result = re.search("^[a-zA-Z]\w{3,}$", username, flags=re.ASCII)
    if not result:
        errorsLabel.setText('Invalid username.\n')
        return False
    else:
        errorsLabel.setText('')
        return True


def isPasswordAndConfirmationValid(password, confirmation, errorsLabel) -> bool:
    """
    Simple function to check if password is valid (8 characters long) and
    wether the confirmation match.
    Returns a boolean value.
    """
    if (len(password) >= 8 and (password == confirmation)):
        errorsLabel.setText('')
        return True
    else:
        errorsLabel.setText('Invalid password.')
        return False


def makeUserDb(username):
    """Create a database for the user, and create a passwords table (description, password)."""

    dbPath = f"{DB_DIR}/{username}.sqlite"

    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()

    cur.execute(
        f"CREATE TABLE {PASSWORDS_TABLE} (description TEXT, password TEXT)")

    conn.commit()
    conn.close()


def addUser(username, password):
    """Add user to the users database."""

    encrypted_password = sha256Encrypt(password)

    conn = sqlite3.connect(USERS_DB_PATH)
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO {USERS_TABLE} VALUES (?, ?)",
        (username, encrypted_password),
    )
    conn.commit()
    conn.close()


def submitSignUp(username, password, confirmation, errorsLabel) -> bool:
    # Variable to be returned
    validSignUp = True
    if username == '' or password == '' or confirmation == '':
        validSignUp = False
        errorsLabel.setText('Missing information')
    else:
        if isUsernameValid(username, errorsLabel) and \
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
