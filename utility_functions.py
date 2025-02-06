import mysql.connector
import numpy as np
import matplotlib.pyplot as plt 
import re
            
# Updates the NumberOfWordEntries column in the languages table with the actual number of word entries in the corresponding dictionary tables.  TODO: change db conection to parameter etc.          
def update_word_entry_counts():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'pass',
        'database': 'book_project',
        'use_pure' : 'True'
        }       
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        # Get all languages from the languages table
        get_languages_query = "SELECT id, Language FROM languages"
        cursor.execute(get_languages_query)
        languages = cursor.fetchall()
        
        for language_id, language_name in languages:
            dictionary_table_name = f"{language_name.lower()}dictionary"
            
            # Get number of entries in the dictionary table
            get_word_count_query = f"SELECT COUNT(*) FROM {dictionary_table_name}"
            cursor.execute(get_word_count_query)
            word_count = cursor.fetchone()[0]
            
            # Update NumberOfWordEntries in languages table
            update_query = "UPDATE languages SET NumberOfWordEntries = %s WHERE id = %s"
            cursor.execute(update_query, (word_count, language_id))
        
        cnx.commit()
    
    except mysql.connector.Error as err:
        print(f"Error updating word entry counts: {err}")
    finally:
        if cnx:
            cnx.close()

# Returns a list of books with input title as dictionaries.
def get_books_with_title(title, db_config):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)  

        query = "SELECT Id, SourceWebsite, Title, Author, Language, StoredAndProcessed FROM book WHERE Title = %s"
        cursor.execute(query, (title,))
        books = cursor.fetchall()
        
        # replace author and language IDs with their names
        for i in range(len(books)):
            books[i]['Author'] = _get_author(cursor, books[i]['Author'])
            books[i]['Language'] = _get_language(cursor, books[i]['Language'])
        return books   

    except mysql.connector.Error as err:
        print(f"Error retrieving books: {err}")
        return []   

    finally:
        if cnx:
            cnx.close()
                        
# Get author from the database based on input id.
def _get_author(cursor, author_id):
    get_author_id_query = "SELECT Name FROM author WHERE Id = %s"
    cursor.execute(get_author_id_query, (author_id,))
    author_name = cursor.fetchone()
    return author_name['Name']

# Get language from the database based on input id.
def _get_language(cursor, language_id):
    get_language_id_query = "SELECT Name FROM languages WHERE id = %s"
    cursor.execute(get_language_id_query, (language_id,))
    language_name = cursor.fetchone()
    return language_name['Name']

# a function that searches through a database dictionary table and returns the ID value of all words that contain nothing but symbols that are not to be counted as "regular words"
def get_non_alphanumerics(dictionary_name, db_config):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        query = f"SELECT Id, Word FROM {dictionary_name}"  
        cursor.execute(query)
        words = cursor.fetchall()

        non_alphanumeric_ids = []
        for word_id, word in words:
            if not re.fullmatch(r"[a-zA-Z0-9]+", word):  # Check for only non-alphanumeric
                non_alphanumeric_ids.append(word_id)

        return np.array(non_alphanumeric_ids, dtype=int)  # Convert to NumPy array

    except mysql.connector.Error as err:
        print(f"Error retrieving data: {err}")
        return np.array([], dtype=int)  # Return empty array on error

    finally:
        if cnx:
            cnx.close()    

