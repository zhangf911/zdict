import os


VERSION = '2.0.4'

BASE_DIR_NAME = '.zdict'
BASE_DIR = os.path.join(os.path.expanduser("~"), BASE_DIR_NAME)

DB_NAME = 'zdict.db'
DB_FILE = os.path.join(BASE_DIR, DB_NAME)
