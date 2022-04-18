#!/usr/bin/env python3
#This file will be used to make functions to manage database
#[on_true] if [expression] else [on_false]  this is also known as ternary statement

import sqlite3
import random
import pyperclip

PATH_TO_DB = 'passwd.db'

# Copy to clipboard
def copy_text(text:str):
	pyperclip.copy(text)

# Generate a random password
def gen_pass(caps:bool=True , smalls:bool=True , nums:bool=True , specials:bool=False , length_start:int=20 , length_end:int=32) -> str:
	length = random.randint(length_start, length_end+1)
	allowed_chars = []
	allowed_chars += list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') if caps else []      #CAPS
	allowed_chars += list('abcdefghijklmnopqrstuvwxyz') if smalls else []    #SMALLS
	allowed_chars += list('1234567890') if nums else []                      #NUMS
	allowed_chars += list('''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''') if specials else []   #SPECIALS
	passwd = ""
	if len(allowed_chars) == 0:
		return '0'
	else:
		for i in range(length):
			passwd += random.choice(allowed_chars)
		return passwd

# If the database and table do not exist create it
def make_if_not():
	sqlConnection = sqlite3.connect(PATH_TO_DB)
	sqlCursor = sqlConnection.cursor()
	sqlCursor.execute("""CREATE TABLE IF NOT EXISTS passwd(
		service TEXT,
		username TEXT,
		email TEXT,
		password TEXT,
		notes TEXT
	)""")

	# Commit everything and close connection
	sqlConnection.commit()
	sqlConnection.close()

# Give all the information
def give_all() -> list:
	sqlConnection = sqlite3.connect(PATH_TO_DB)
	sqlCursor = sqlConnection.cursor()
	sqlCursor.execute("SELECT rowid,* FROM passwd")
	data = sqlCursor.fetchall()

	for i in data:
		print(i)

	# Commit Everything and close connection
	sqlConnection.commit()
	sqlConnection.close()
	return data

# Add one entry
def new_entry(service:str , user:str , email:str , passwd:str , note:str):
	sqlConnection = sqlite3.connect(PATH_TO_DB)
	sqlCursor = sqlConnection.cursor()
	sqlCursor.execute("INSERT INTO passwd VALUES (?,?,?,?,?)",(service, user, email, passwd, note))

	# Commit Everything and close connection
	sqlConnection.commit()
	sqlConnection.close()

# Edit one entry
def edit_entry(id:int, entry:list):
	entry.append(id)
	sqlConnection = sqlite3.connect(PATH_TO_DB)
	sqlCursor = sqlConnection.cursor()
	sqlCursor.execute("""UPDATE passwd SET
		service ?,
		username ?,
		email ?,
		password ?,
		notes ?
		WHERE rowid = ?
	""", tuple(entry))

	# Commit Everything and close connection
	sqlConnection.commit()
	sqlConnection.close()

# Delete one entry
def del_entry(id:int):
	sqlConnection = sqlite3.connect(PATH_TO_DB)
	sqlCursor = sqlConnection.cursor()
	sqlCursor.execute("DELETE from passwd WHERE rowid = (?)", (str(id)))

	# Commit Everything and close connection
	sqlConnection.commit()
	sqlConnection.close()
