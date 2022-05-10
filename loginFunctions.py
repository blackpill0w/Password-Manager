import re

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

