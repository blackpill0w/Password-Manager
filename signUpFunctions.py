import re, sqlite3, os
from hashlib import sha256
from settings import DB_DIR, USERS_DB_PATH, PASSWORDS_TABLE, USERS_TABLE

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

        connection = sqlite3.connect(USERS_DB_PATH)
        cursor = connection.cursor()

        cursor.execute(f"CREATE TABLE {USERS_TABLE} (user TEXT, password TEXT)")

        connection.commit()
        connection.close()

def isUserExist(username):
    """Check if user has an account, returns a bool value."""

    connection = sqlite3.connect(USERS_DB_PATH)
    cursor = connection.cursor()

    result = list(
        cursor.execute(
            f"SELECT * FROM {USERS_TABLE} WHERE user = :username",
            {"username": username},
        ),
    )
    connection.close()

    return False if result == [] else True

def makeUserDb(username):
    """Create a database for the user, and create a passwords table (description, password)."""

    dbPath = f"{DB_DIR}/{username}.sqlite"

    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()

    cursor.execute(f"CREATE TABLE {PASSWORDS_TABLE} (description TEXT, password TEXT)")

    connection.commit()
    connection.close()

def addUser(username, password):
    """Add user to the users database."""

    encrypted_password = sha256Encrypt(password)

    connection = sqlite3.connect(USERS_DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO {USERS_TABLE} VALUES (?, ?)",
        (username, encrypted_password),
    )
    connection.commit()
    connection.close()

def submitSignUp(username, password, errorsLabel):
    checkAppDir()
    if not isUserExist(username):
        makeUserDb(username)
        addUser(username, password)
        return True
    else:
        errorsLabel.setText('Username already used')
        return False