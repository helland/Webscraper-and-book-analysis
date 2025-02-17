import mysql.connector
import numpy as np  
import re
            
# Updates the NumberOfWordEntries column in the languages table with the actual number of word entries in the corresponding dictionary tables.       
def update_word_entry_counts(db_config):  
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
def get_books_with_title(title, get_all, db_config):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)  
        
        if get_all: # get all books by title
            query = """SELECT Id, SourceWebsite, Title, Author, Language, 
            StoredAndProcessed, WordCount, CharacterCount FROM book 
            WHERE Title LIKE %s"""
        else:       # only get books stored and encoded
            query = """SELECT Id, SourceWebsite, Title, Author, Language, 
            StoredAndProcessed, WordCount, CharacterCount FROM book 
            WHERE StoredAndProcessed = 1 AND Title LIKE %s"""
        titles = ("%" + title + "%",) # all books containing the substring "title"
        cursor.execute(query, titles,)
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

# Returns a list of books with input title as dictionaries.
def get_book_ids_with_title(title, get_all, db_config):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)  
        
        if get_all: # get all books by title
            query = "SELECT Id FROM book WHERE Title LIKE %s"
        else:       # only get books stored and encoded
            query = "SELECT Id FROM book WHERE StoredAndProcessed = 1 AND Title LIKE %s" 
        titles = ("%" + title + "%",) # all books containing the substring "title"
        cursor.execute(query, titles)
        books = cursor.fetchall()
        book_ids = []
 
        for book in books:
            book_ids.append(book['Id'])
        return book_ids  

    except mysql.connector.Error as err:
        print(f"Error retrieving books: {err}")
        return []   

    finally:
        if cnx:
            cnx.close()
            
            
# Returns a list of books with input title as dictionaries.
def get_stored_and_processed_books(db_config):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)  

        query = "SELECT Id, SourceWebsite, Title, Author, Language, WordCount, CharacterCount FROM book WHERE StoredAndProcessed = 1"
        cursor.execute(query)
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
def get_non_alphanumerics(dictionary_name, db_config): # NOTE: this function was added to Book object init. It might not be useful anymore, but I'm keeping it in case it might be needed outside a book object
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

        return non_alphanumeric_ids

    except mysql.connector.Error as err:
        print(f"Error retrieving data: {err}")
        return []
    finally:
        if cnx:
            cnx.close()    
