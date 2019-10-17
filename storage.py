import sqlite3

SQL_INSERT_URL = '''
        INSERT INTO MONITORING(
        TS,
        URL,
        LABEL,
        RESPONSE_TIME,
        STATUS_CODE,
        CONTENT_LENGTH
        )
        VALUES(?,?,?,?,?,?)

'''

def connect(db_name=None):
	"""Устанавливает соединение с бд"""

	if db_name is None:
		db_name = ":Memory:"
	conn = sqlite3.connect(db_name)
	return conn

def 
