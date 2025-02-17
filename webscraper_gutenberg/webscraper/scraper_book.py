import datetime
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import mysql.connector
import re
import requests
from fake_useragent import UserAgent
import random
import time
import numpy as np
from functools import lru_cache

nltk.download('stopwords')
nltk.download('wordnet')

# Reads a Project Gutenberg txt file and extracts metadata and text.
def gutenberg_book_scraper(source_website):
    referer_sites = ['https://www.google.com','https://www.bing.com','https://www.yahoo.com']
    referer = random.choice(referer_sites)  # Set random referer on each request
    user_agent = UserAgent()
    
    header = {
    'User-Agent': user_agent.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': referer,
    'Connection': 'keep-alive'}
    
    try:
        print(f"Trying to fetch page: {source_website}")
        response = requests.get(source_website, headers=header, timeout=5)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
        # Pause for a bit between requests (in an attempt to not bother gutenberg/internet archive too much)
        time.sleep(2)

        text = response.text
        #print("Raw text fetched from website.")
        
        # Extract metadata
        title = extract_metadata(text, "Title:")
        author = extract_metadata(text, "Author:")
        release_date_str = extract_metadata(text, "Release date:")
        release_date = extract_date(release_date_str)
        language = extract_metadata(text, "Language:")
    
        # Extract book text
        start_marker = f"*** START OF THE PROJECT GUTENBERG EBOOK" #{title.upper()} ***
        end_marker = "END OF THE PROJECT GUTENBERG"
        start_index = text.find(start_marker) + len(start_marker)
        end_index = text.find(end_marker)
        book_text = text[start_index:end_index].strip()
    
        # Calculate word and character count
        word_count = len(book_text.split())
        character_count = len(book_text)

        return title, author, release_date, language, book_text, word_count, character_count

    except FileNotFoundError:
        print(f"File not found: {source_website}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Extracts metadata value from the given text.
def extract_metadata(text, key):
    try:
        start_index = text.index(key) + len(key)
        end_index = text.find("\n", start_index)
        return text[start_index:end_index].strip()
    except ValueError:
        return None
    
# Extracts date from the given string and formats it for MySQL.
def extract_date(date_str):
    try:
        date_parts = date_str.split()[0:3]  # Extract date parts (e.g., "August", "12", "2016")
        date_obj = datetime.datetime.strptime(" ".join(date_parts), "%B %d %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return None


"""
Stores a list of books in the database.
Args:
    books: A list of dictionaries, where each dictionary represents a book
           and contains the following keys: 
           'title', 'text', 'author', 'release_date', 'language', 
           'word_count', 'character_count', 'source_website'.
"""
def store_books_in_database(books, db_config):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(buffered=True)

        for book in books:
            store_book_in_database_single(cursor, book)
            
        cnx.commit()

    except mysql.connector.Error as err:
        print(f"Error storing books in database: {err}")
    finally:
        if cnx:
            cnx.close()

# Stores a single book in the database.
def store_book_in_database_single(cursor, book):
    book_id = _get_or_insert_book(cursor, book)
    encode_filter_and_lemmatize_book(book_id, book['text'], cursor)

# Gets the ID of the book from the database. If the book doesn't exist, inserts it and returns the new ID.
def _get_or_insert_book(cursor, book):
    check_source_query = "SELECT id FROM book WHERE SourceWebsite = %s"
    cursor.execute(check_source_query, (book['SourceWebsite'],))
    existing_book_id = cursor.fetchone()

    if existing_book_id:
        book_id = existing_book_id[0]
        #print(f"The book '{book['Title']}' found in the table of content.")
    else:
        insert_query = """
            INSERT INTO book (Title, Author, Language, ReleaseDate, 
                              WordCount, CharacterCount, StoredAndProcessed, SourceWebsite)
            VALUES (%s, %s, %s, %s, %s, %s, '0', %s)
        """
        insert_data = (book['Title'], _get_or_insert_author(cursor, book['Author']), 
                       _get_or_insert_language(cursor, book['Language']), 
                       book['ReleaseDate'], book['WordCount'], book['CharacterCount'], 
                       book['SourceWebsite'])
        cursor.execute(insert_query, insert_data)
        book_id = cursor.lastrowid
        #print(f"The book '{book['Title']}' has been added to the table of content.")
    return book_id

# Gets the ID of the author from the database. If the author doesn't exist, inserts it and returns the new ID.
def _get_or_insert_author(cursor, author_name):
    get_author_id_query = "SELECT id FROM author WHERE Name = %s"
    cursor.execute(get_author_id_query, (author_name,))
    author_id = cursor.fetchone()
    if author_id:
        return author_id[0]
    else:
        insert_author_query = "INSERT INTO author (Name) VALUES (%s)"
        cursor.execute(insert_author_query, (author_name,))
        return cursor.lastrowid

# Gets the ID of the language from the database. If the language doesn't exist, inserts it and returns the new ID.
def _get_or_insert_language(cursor, language_name):
    get_language_id_query = "SELECT id FROM languages WHERE Name = %s"
    cursor.execute(get_language_id_query, (language_name,))
    language_id = cursor.fetchone()
    if language_id:
        return language_id[0]
    else:
        insert_language_query = "INSERT INTO languages (Name) VALUES (%s)"
        cursor.execute(insert_language_query, (language_name,))
        #print(f"new language {language_name} added to the database.")
        return cursor.lastrowid

# fetch all words and IDs from relevant dictionary in the database - NOTE: delete this and import from analysis_functions? eh, decide maybe later
@lru_cache(maxsize=350000)
def _get_all_words_from_dict(cursor, dictionary_table_name):
    get_words_query = f"SELECT Word, Id FROM {dictionary_table_name}"
    cursor.execute(get_words_query)
    word_dict = dict(cursor.fetchall())
    return word_dict
    
# Encodes, filters, and lemmatizes the given book text and store it in a database.            
def encode_filter_and_lemmatize_book(book_id, text, cursor):
    if book_id > 0:
        try:
            # Get language ID 
            get_language_id_query = "SELECT Language FROM book WHERE id = %s"
            cursor.execute(get_language_id_query, (book_id,))
            language_id = cursor.fetchone()[0]  # Get the ID from the tuple

            # Get language name
            get_language_query = "SELECT Name FROM Languages WHERE id = %s"
            cursor.execute(get_language_query, (language_id,))
            language = cursor.fetchone()[0]

            #start_time = time.time()

            # Determine dictionary table name an get its content
            dictionary_table_name = f"{language.lower()}dictionary"
            word_dict = _get_all_words_from_dict(cursor, dictionary_table_name)

            # Tokenize, filter, lemmatize
            words = re.findall(r"[\w']+|[.,\_!?;:\-\—\(\)\[\]\{\}\"\n]", text)
            stop_words = set(stopwords.words(language))
            filtered_words = [word for word in words if word.lower() not in stop_words]
            lemmatizer = WordNetLemmatizer()
            lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

            # Find or insert new words and get IDs
            new_words = set(words) | set(filtered_words) | set(lemmatized_words) # Combine all words
            words_to_insert = set()
            for word in new_words:
                if word not in word_dict.keys():  # Check if the word exists in the dictionary
                    words_to_insert.add(word)

            if words_to_insert:  # Insert new words if any
                for word in words_to_insert:
                    insert_data = (word, len(word))                                                                     #insert_data = [(word, len(word)) for word in words_to_insert]
                    insert_query = f"INSERT INTO {dictionary_table_name} (Word, WordCharacterLength) VALUES (%s, %s)"
                    cursor.execute(insert_query, insert_data)                                                           #cursor.executemany(insert_query, insert_data)
                print(f"{len(words_to_insert)} new words added to {dictionary_table_name}")
                
                # Refresh the dictionary cache after inserting
                cursor.execute('commit')  # Commit before refreshing the cache
                _get_all_words_from_dict.cache_clear()
                word_dict = _get_all_words_from_dict(cursor, dictionary_table_name)  # Refresh cache
            
            word_ids = np.array([word_dict.get(word) for word in words], dtype=int)
            filtered_word_ids = np.array([word_dict.get(word) for word in filtered_words], dtype=int)
            lemmatized_word_ids = np.array([word_dict.get(word) for word in lemmatized_words], dtype=int)


            # Insert word IDs to the tables of encoded books
            #print(f"Encoding and lookups took: {round(time.time() - start_time, 2)} seconds") 
            #start_time = time.time()
            _insert_word_ids(cursor, book_id, word_ids, "wordstointeger")
            _insert_word_ids(cursor, book_id, filtered_word_ids, "filteredbooks")
            _insert_word_ids(cursor, book_id, lemmatized_word_ids, "lemmatizedbooks")
            
            #print(f"Database insert took: {round(time.time() - start_time, 2)} seconds")
            
            cursor.execute('commit') # to make sure everything is up to date before updating book status
            _update_language_word_count(cursor, dictionary_table_name, language_id)
            _update_status(cursor, book_id)

        except mysql.connector.Error as err:
            print(f"Error processing book: {err}")

# Gets the ID of a word from the dictionary table. If the word doesn't exist, inserts it and returns the new ID. NOTE: no longer in use
@lru_cache(maxsize=300000)  # Cache word IDs
def _get_or_insert_word(cursor, dictionary_table_name, word):
    get_word_id_query = f"SELECT Id FROM {dictionary_table_name} WHERE Word = %s"
    cursor.execute(get_word_id_query, (word,))
    existing_word_id = cursor.fetchone()
    if existing_word_id:
        return existing_word_id[0]
    else:
        insert_word_query = f"""
        INSERT INTO {dictionary_table_name} (Word, WordCharacterLength) 
        VALUES (%s, %s)
        """
        cursor.execute(insert_word_query, (word, len(word)))
        #print(f"{word} added to {dictionary_table_name}")
        return cursor.lastrowid

# Inserts word IDs into the specified word-encoding table.
def _insert_word_ids(cursor, book_id, word_ids, table_name):
    for word_id in word_ids:
        data = (int(word_id), book_id)                                                   #data = [(int(word_id), book_id) for word_id in word_ids]
        insert_query = f"INSERT INTO {table_name} (WordId, BookId) VALUES (%s, %s)"
        cursor.execute(insert_query, data)                                               #cursor.executemany(insert_query, data)    # executemany just doesn't want to work it seems

# Updates the word count of the language in the languages table.
def _update_language_word_count(cursor, dictionary_table_name, language_id):
    get_word_count_query = f"SELECT COUNT(*) FROM {dictionary_table_name}"
    cursor.execute(get_word_count_query)
    word_count = cursor.fetchone()[0]

    update_query = "UPDATE languages SET NumberOfWordEntries = %s WHERE id = %s"
    cursor.execute(update_query, (word_count, language_id))

# Updates status of a book to indicate it has been stored in the database
def _update_status(cursor, book_id):
    confirmation_query = "SELECT Id FROM wordstointeger WHERE BookId = %s"
    cursor.execute(confirmation_query, (book_id,))
    entries_with_book_id = cursor.fetchone()
    
    #only update the book to "stored and processed" if the book actually has entries in the encoded-text-table
    if entries_with_book_id is not None: 
        update_query = "UPDATE book SET StoredAndProcessed = 1 WHERE id = %s"
        cursor.execute(update_query, (book_id,))
        #print("Book status updated to 'Stored and Processed'.")