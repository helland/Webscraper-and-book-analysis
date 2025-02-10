from functools import lru_cache
import mysql.connector

db_config = {
'host': 'localhost',
'user': 'helland',
'password': 'Ganymedes8787',
'database': 'book_project',
'use_pure': 'True'}

try:
    # Connect to the MySQL database
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    cursor.execute("SELECT * FROM wordstointeger")
    table_content = cursor.fetchall()
    print(table_content)
    
except mysql.connector.Error as err:
    print(f"Error inserting books into the database: {err}")

finally:
    if cnx:
        cnx.close()
















'''
import mysql.connector

def add_punctuation_to_table_mysql(cursor, table_name):

    punctuation_marks = ['.', ',', '_', '!', '?', ';', ':', '-', '—', '(', ')', '[', ']', '{', '}', '"', '\n']

    try:
        for mark in punctuation_marks:
            sql = f"INSERT INTO {table_name} (Word, WordCharacterLength) VALUES (%s, %s)"  # Use parameterized query
            val = (mark, 0)
            cursor.execute(sql, val)

    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
        # Important: Handle rollback outside the helper function.
        raise  # Re-raise after printing.

    # Commit handling should be done outside this helper function.


#Example usage (replace with your actual credentials):
mydb = mysql.connector.connect(
   host="localhost",
   user="helland",
   password="Ganymedes8787",
   database="book_project",
   use_pure=True
)

mycursor = mydb.cursor()

add_punctuation_to_table_mysql(mycursor, 'swedishdictionary')

mydb.commit()  # Commit the changes outside the helper function
mydb.close()

'''



  
