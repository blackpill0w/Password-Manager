import os

DB_DIR = os.path.expanduser('~/.pyqt_password_manager')

USERS_DB_PATH = f'{DB_DIR}/users.sqlite'
PASSWORDS_TABLE = 'passwords_table'