

import mysql.connector
import numpy as np
import re
import webscraper.utility_functions as utils
from functools import lru_cache

class Book:
    def __init__(self, book_id, db_config, cursor, include_filtered=False, include_lemmatized=False):
        self.book_id = book_id
        self.title = ''
        self.author = None
        self.language = None
        self.language_name = ''
        self.release_date = None
        self.word_count = None
        self.character_count = None
        self.source_website = None
        self.text = None
        self.exclude = None
        self.line_break = None
        self.filtered_text = None if not include_filtered else np.array([], dtype=np.int32)
        self.lemmatized_text = None if not include_lemmatized else np.array([], dtype=np.int32)
        self.db_config = db_config
        
        #try:
        #    cnx = mysql.connector.connect(**db_config)
        #    cursor = cnx.cursor() 

        # Fetch book details from the database
        get_book_query = "SELECT * FROM book WHERE id = %s"
        cursor.execute(get_book_query, (book_id,))
        book_data = cursor.fetchone()

        if book_data:
            self.source_website = book_data[1]
            self.title = book_data[3]
            self.language = book_data[4]
            self.author = book_data[5]
            self.word_count = book_data[6]
            self.character_count = book_data[7]
            self.release_date = book_data[8]
            
            # Get language name. NOTE: this shouldn't be here. the book object should not deal with text like this. I just wrote myself into a small corner elsewhere and realized it would be so much easier to put this here... given time I'd have found a better solution, but decided on the easy path instead right here and now out of sheer laziness.
            get_language_query = "SELECT Name FROM Languages WHERE id = %s"
            cursor.execute(get_language_query, (self.language,))
            self.language_name = cursor.fetchone()[0]
            
            # Fetch word IDs from related tables
            get_words_to_integer_query = "SELECT WordId FROM WordsToInteger WHERE BookId = %s"
            cursor.execute(get_words_to_integer_query, (book_id,))
            self.text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)
            
            
            if include_filtered:
                get_filtered_books_query = "SELECT WordId FROM FilteredBooks WHERE BookId = %s"
                cursor.execute(get_filtered_books_query, (book_id,))
                self.filtered_text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)

            if include_lemmatized:
                get_lemmatized_books_query = "SELECT WordId FROM LemmatizedBooks WHERE BookId = %s"
                cursor.execute(get_lemmatized_books_query, (book_id,))
                self.lemmatized_text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)
            
            # define a set of values that will not be used when running certain analyses on the book text (default = non-alphanumerics). Change with set/add/remove methods below
            query = f"SELECT Id, Word FROM {self.language_name}dictionary"  
            cursor.execute(query)
            words = cursor.fetchall()
    
            self.exclude = []
            for word_id, word in words:
                if not re.fullmatch(r"[a-zA-Z0-9]+", word):  # Check for only non-alphanumeric
                    self.exclude.append(word_id)         
            #self.exclude = utils.get_non_alphanumerics(f"{self.language_name}dictionary", self.db_config) # decided to just copy the code from utility functions to avoid setting up extra database connections
            
            # Find line break (\n) in the relevant dictionary table and save it locally
            query = f"SELECT Id FROM {self.language_name}dictionary WHERE Word = '\n'"  
            cursor.execute(query)
            self.line_break = cursor.fetchone()[0]
                
        #except mysql.connector.Error as err:
        #    print(f"Error fetching book data: {err}")
        #finally:
        #    if cnx:
        #        cnx.close()      

    
    # Getters
    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_language(self):
        return self.language

    def get_release_date(self):
        return self.release_date

    def get_word_count(self):
        return self.word_count

    def get_character_count(self):
        return self.character_count

    def get_source_website(self):
        return self.source_website

    def get_text(self):
        return self.text

    def get_filtered_text(self):
        if self.filtered_text is not None:
            return self.filtered_text
        else:
            raise AttributeError("Filtered books data is not available for this object.")

    def get_lemmatized_text(self):
        if self.lemmatized_text is not None:
            return self.lemmatized_text
        else:
            raise AttributeError("Lemmatized books data is not available for this object.")
    def get_excluded_values(self):
        return self.exclude
    
    # get all words in the text at parameter indices 
    def get_text_at_indices(self, indices):
        return [self.text[i] for i in indices]        
    def get_filtered_text_at_indices(self, indices):
        return [self.filtered_text[i] for i in indices]
    def get_lemmatized_text_at_indices(self, indices):
        return [self.lemmatized_text[i] for i in indices]
    
    # Setters 
    def set_title(self, new_title):
        self.title = new_title

    def set_author(self, new_author):
        self.author = new_author

    def set_language(self, new_language):
        self.language = new_language

    def set_release_date(self, new_date):
        self.release_date = new_date

    def set_word_count(self):
        self.word_count = self.text.size # add conditions here, like removing all entries that correspond to .,_-[/}!?< etc.

    def set_character_count(self, new_character_count):
        self.character_count = new_character_count  # this requires you to convert the book to text before counting, so it will be done outside the object somewhere

    def set_source_website(self, new_link):
        self.source_website = new_link

    def set_words_to_integer(self, new_text):
        if isinstance(new_text, np.ndarray):
            self.text = new_text
        else:
            print("input is not a numpy array")

    def set_excluded_values(self, excluded_values):
        self.exclude = excluded_values
        
    def set_filtered_books(self, new_filtered_text):
        if self.filtered_text is not None:
            if isinstance(new_filtered_text, np.ndarray):
                self.filtered_text = new_filtered_text
            else:
                print("input is not a numpy array")
        else:
            raise AttributeError("Filtered books data is not available for this object.")

    def set_lemmatized_books(self, new_lemmatization):
        if self.lemmatized_text is not None:
            if isinstance(new_lemmatization, np.ndarray):
                self.lemmatized_text = new_lemmatization
            else:
                print("input is not a numpy array")
        else:
            raise AttributeError("Lemmatized books data is not available for this object.")
    
    def add_excluded_value(self, add):
        self.exclude.append(add)
        
    def remove_excluded_value(self, value):
        if value in self.exclude:
            self.exclude.remove(value)
            
      
    # Add word to text
    def add_word_to_text(self, word_id, index=None):
        if index is None:
            self.text = np.append(self.text, word_id)
            self.filtered_text = np.append(self.filtered_text, word_id)
            self.text = np.append(self.text, word_id)
        else:
            self.text = np.insert(self.text, index, word_id)
            self.filtered_text = np.insert(self.filtered_text, index, word_id)
            self.lemmatized_texttext = np.insert(self.lemmatized_texttext, index, word_id)
        
        
    # Remove word from text
    def remove_word_from_text(self, word_id):
        try:
            self.text = np.delete(self.text, np.where(self.text == word_id))
            self.filtered_text = np.delete(self.filtered_text, np.where(self.filtered_text == word_id))
            self.lemmatized_text = np.delete(self.lemmatized_text, np.where(self.lemmatized_text == word_id))
        except ValueError:
            pass  # Word not found
      
    # TODO - add method for removing text from index placement and method to add word where another word is found
    
    # Replace word in integer arrays
    def replace_word_in_text(self, old_word_id, new_word_id):
        self.text[self.text == old_word_id] = new_word_id
        
    # Find placement of a word in the text. defaults to regular text, unless filtered/lemmatized text is specified.
    def find_placement(self, word_id, array_type="text"):
        if array_type == "text":
            try:
                return np.where(self.text == word_id)[0][0]
            except IndexError:
                raise ValueError("Word not found in text array.")
        elif array_type == "filtered_text" and self.filtered_text is not None:
            try:
                return np.where(self.filtered_text == word_id)[0][0]
            except IndexError:
                raise ValueError("Word not found in filtered_text array.")
        elif array_type == "lemmatized_text" and self.lemmatized_text is not None:
            try:
                return np.where(self.lemmatized_text == word_id)[0][0]
            except IndexError:
                raise ValueError("Word not found in lemmatized_text array.")
        else:
            raise ValueError("Invalid array_type or data not available.")

    # Find number of occurrences of word in text arrays
    def find_number_of(self, word_id, array_type="text"):
        if array_type == "text":
            return np.count_nonzero(self.text == word_id)
        elif array_type == "filtered_text" and self.filtered_text is not None:
            return np.count_nonzero(self.filtered_text == word_id)
        elif array_type == "lemmatized_text" and self.lemmatized_text is not None:
            return np.count_nonzero(self.lemmatized_text == word_id)
        else:
            raise ValueError("Invalid array_type or data not available.")

@lru_cache(maxsize=350000)   
def _get_all_word_lengths_from_dict(cursor, dictionary_table_name):
    get_word_lengths_query = f"SELECT Id, WordCharacterLength FROM {dictionary_table_name}"
    cursor.execute(get_word_lengths_query)
    word_lengths_dict = dict(cursor.fetchall())
    return word_lengths_dict

'''  
# unused methods      
def get_longest_words(self, filtered_text=False, lemmatized_text=False):
    try:
        cnx = mysql.connector.connect(**self.db_config)
        cursor = cnx.cursor()

        dictionary_table_name = f"{self.language_name}dictionary"

        word_lengths = _get_all_word_lengths_from_dict(cursor, dictionary_table_name)
        
        # Decide which version of the text you want the longest word from
        if filtered_text and lemmatized_text:
            text = self.text # if both are set to true, use the regular text instead.
        elif filtered_text:
            text = self.filtered_text
        elif lemmatized_text:
            text = self.lemmatized_text
        else:
            text = self.text

        longest_length = 0
        for word_id in text:
            word_length = word_lengths.get(int(word_id))  # Direct lookup
            if word_length is not None:  #Handle cases where a word_id might not be in the dictionary
                longest_length = max(longest_length, word_length)

        longest_words_in_text = []
        for word_id in text:
            word_length = word_lengths.get(int(word_id)) # Direct Lookup
            if word_length == longest_length:
                longest_words_in_text.append(word_id)

        return longest_words_in_text

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if cnx:
            cnx.close()       

    # Reuploads the book data to the database, replacing existing entries.
    def reupload_to_database(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()

            # Delete existing entries in related tables
            delete_words_to_integer_query = "DELETE FROM WordsToInteger WHERE BookId = %s"
            cursor.execute(delete_words_to_integer_query, (self.book_id,))

            if self.filtered_text is not None:
                delete_filtered_books_query = "DELETE FROM FilteredBooks WHERE BookId = %s"
                cursor.execute(delete_filtered_books_query, (self.book_id,))

            if self.lemmatized_text is not None:
                delete_lemmatized_books_query = "DELETE FROM LemmatizedBooks WHERE BookId = %s"
                cursor.execute(delete_lemmatized_books_query, (self.book_id,))

            # Update book entry
            update_book_query = """
                UPDATE book
                SET 
                    Title = %s,
                    Author = %s,
                    Language = %s,
                    ReleaseDate = %s,
                    WordCount = %s,
                    CharacterCount = %s,
                    SourceWebsite = %s
                WHERE id = %s
            """
            update_data = (self.title, self.author, self.language, self.release_date, 
                           self.word_count, self.character_count, self.source_website, self.book_id)
            cursor.execute(update_book_query, update_data)

            # Insert new word IDs
            insert_book_text_query = """
                INSERT INTO WordsToInteger (WordId, BookId) 
                VALUES (%s, %s)
            """
            for word_id in self.text:
                cursor.execute(insert_book_text_query, (word_id, self.book_id))

            if self.filtered_text is not None:
                insert_filtered_text_query = """
                    INSERT INTO FilteredBooks (WordId, BookId) 
                    VALUES (%s, %s)
                """
                for word_id in self.filtered_text:
                    cursor.execute(insert_filtered_text_query, (word_id, self.book_id))

            if self.lemmatized_text is not None:
                insert_lemmatized_text_query = """
                    INSERT INTO LemmatizedBooks (WordId, BookId) 
                    VALUES (%s, %s)
                """
                for word_id in self.lemmatized_text:
                    cursor.execute(insert_lemmatized_text_query, (word_id, self.book_id))

            cnx.commit()

        except mysql.connector.Error as err:
            print(f"Error reuploading book to database: {err}")
        finally:
            if cnx:
                cnx.close()              

    #Compares the book object's attributes with the database and returns a list of booleans indicating whether each attribute differs from the database.
    def compare_with_database(self):  
        differs_list = [False] * 10  # Initialize with 10 False values

        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()

            # Fetch book details from the database
            get_book_query = "SELECT * FROM book WHERE id = %s"
            cursor.execute(get_book_query, (self.book_id,))
            db_book_data = cursor.fetchone()

            if db_book_data:
                # Compare attributes
                differs_list[0] = self.title != db_book_data['Title']
                differs_list[1] = self.author != db_book_data['Author']
                differs_list[2] = self.language != db_book_data['Language']
                differs_list[3] = self.release_date != db_book_data['ReleaseDate']
                differs_list[4] = self.word_count != db_book_data['WordCount']
                differs_list[5] = self.character_count != db_book_data['CharacterCount']
                differs_list[6] = self.source_website != db_book_data['SourceWebsite']

                # Compare text
                db_words_to_integer = []
                get_words_to_integer_query = "SELECT WordId FROM WordsToInteger WHERE BookId = %s"
                cursor.execute(get_words_to_integer_query, (self.book_id,))
                for row in cursor.fetchall():
                    db_words_to_integer.append(row[0])
                differs_list[7] = not np.array_equal(self.text, np.array(db_words_to_integer))

                # Compare filtered_text if available
                if self.filtered_text is not None:
                    db_filtered_books = []
                    get_filtered_books_query = "SELECT WordId FROM FilteredBooks WHERE BookId = %s"
                    cursor.execute(get_filtered_books_query, (self.book_id,))
                    for row in cursor.fetchall():
                        db_filtered_books.append(row[0])
                    differs_list[8] = not np.array_equal(self.filtered_text, np.array(db_filtered_books))

                # Compare lemmatized_text if available
                if self.lemmatized_text is not None:
                    db_lemmatized_books = []
                    get_lemmatized_books_query = "SELECT WordId FROM LemmatizedBooks WHERE BookId = %s"
                    cursor.execute(get_lemmatized_books_query, (self.book_id,))
                    for row in cursor.fetchall():
                        db_lemmatized_books.append(row[0])
                    differs_list[9] = not np.array_equal(self.lemmatized_text, np.array(db_lemmatized_books))

        except mysql.connector.Error as err:
            print(f"Error comparing book with database: {err}")
            return None
        finally:
            if cnx:
                cnx.close()
        return differs_list
    
    # Replaces the internal variables of the Book object with the corresponding values from the database.
    def replace_with_database_values(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()

            # Fetch book details from the database
            get_book_query = "SELECT * FROM book WHERE id = %s"
            cursor.execute(get_book_query, (self.book_id,))
            book_data = cursor.fetchone()

            if book_data:
                self.title = book_data['Title']
                self.author = book_data['Author']
                self.language = book_data['Language']
                self.release_date = book_data['ReleaseDate']
                self.word_count = book_data['WordCount']
                self.character_count = book_data['CharacterCount']
                self.source_website = book_data['SourceWebsite']

                # Fetch word IDs from related tables
                get_words_to_integer_query = "SELECT WordId FROM wordstointeger WHERE BookId = %s"
                cursor.execute(get_words_to_integer_query, (self.book_id,))
                self.text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)

                if self.filtered_text is not None:
                    get_filtered_text_query = "SELECT WordId FROM FilteredBooks WHERE BookId = %s"
                    cursor.execute(get_filtered_text_query, (self.book_id,))
                    self.filtered_text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)

                if self.lemmatized_text is not None:
                    get_lemmatized_text_query = "SELECT WordId FROM LemmatizedBooks WHERE BookId = %s"
                    cursor.execute(get_lemmatized_text_query, (self.book_id,))
                    self.lemmatized_text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)

        except mysql.connector.Error as err:
            print(f"Error fetching book data: {err}")
        finally:
            if cnx:
                cnx.close()
                
    # Uploads a new book entry to the database with the values found in the object (regardless of whether it already exist).
    def upload_as_separate_book(self, db_config):
        try:
            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor()

            # Determine new title (to differentiate it from the book already in the database)
            new_title = self.title
            match = re.search(r" v(\d+)$", new_title)
            if match:
                version_number = int(match.group(1))
                new_title = new_title[:-(len(match.group(0)))] + f" v{version_number + 1}"
            else:
                new_title += " v2"

            # Check if language exists in languages table
            get_language_id_query = "SELECT id FROM languages WHERE Language = %s"
            cursor.execute(get_language_id_query, (self.language,))
            language_id = cursor.fetchone()

            # Check if author exists in authors table
            get_author_id_query = "SELECT id FROM authors WHERE Name = %s"
            cursor.execute(get_author_id_query, (self.author,))
            author_id = cursor.fetchone()

            # Insert new book entry
            insert_query = """
                INSERT INTO book (Title, Author_id, Language, ReleaseDate, WordCount, CharacterCount, StoredAndProcessed, SourceWebsite)
                VALUES (%s, %s, %s, %s, %s, %s, 'TRUE', %s)
            """
            insert_data = (new_title, author_id[0], language_id[0], self.release_date, self.word_count, 
                           self.character_count, self.source_website)
            cursor.execute(insert_query, insert_data)
            new_book_id = cursor.lastrowid

            # Insert word IDs into WordsToInteger table
            insert_book_text_query = """
                INSERT INTO WordsToInteger (WordId, BookId) 
                VALUES (%s, %s)
            """
            for word_id in self.text:
                cursor.execute(insert_book_text_query, (word_id, new_book_id))

            if self.filtered_text is not None:
                insert_filtered_text_query = """
                    INSERT INTO FilteredBooks (WordId, BookId) 
                    VALUES (%s, %s)
                """
                for word_id in self.filtered_text:
                    cursor.execute(insert_filtered_text_query, (word_id, new_book_id))

            if self.lemmatized_text is not None:
                insert_lemmatized_text_query = """
                    INSERT INTO LemmatizedBooks (WordId, BookId) 
                    VALUES (%s, %s)
                """
                for word_id in self.lemmatized_text:
                    cursor.execute(insert_lemmatized_text_query, (word_id, new_book_id))

            cnx.commit()

        except mysql.connector.Error as err:
            print(f"Error uploading as separate book: {err}")
        finally:
            if cnx:
                cnx.close()
  '''

    
'''     
        #self.include_filtered = include_filtered # Store as instance variables
        #self.include_lemmatized = include_lemmatized
        self.book_id = book_id
        self.title = ''
        self.author = None
        self.language = None
        self.language_name = ''
        self.release_date = None
        self.word_count = None
        self.character_count = None
        self.source_website = None
        self.db_config = db_config
        self.text = None
        self.exclude = None
        self.line_break = None
        self.filtered_text = None if not include_filtered else np.array([], dtype=np.int32)
        self.lemmatized_text = None if not include_lemmatized else np.array([], dtype=np.int32)

                
        try:
            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor() 

            # Fetch book details from the database
            get_book_query = "SELECT * FROM book WHERE id = %s"
            cursor.execute(get_book_query, (book_id,))
            book_data = cursor.fetchone()

            if book_data:
                self.source_website = book_data[1]
                self.title = book_data[3]
                self.language = book_data[4]
                self.author = book_data[5]
                self.word_count = book_data[6]
                self.character_count = book_data[7]
                self.release_date = book_data[8]
                
         
        except mysql.connector.Error as err:
            print(f"Error fetching book data: {err}")
        finally:
            if cnx:
                cnx.close()        
        
                # Get language name. NOTE: this shouldn't be here. the book object should not deal with text like this. I just wrote myself into a small corner elsewhere and realized it would be so much easier to put this here... given time I'd have found a better solution, but decided on the easy path instead right here and now out of sheer laziness.
                get_language_query = "SELECT Name FROM Languages WHERE id = %s"
                cursor.execute(get_language_query, (self.language,))
                self.language_name = cursor.fetchone()[0]
                 
              # Fetch word IDs from related tables
                get_words_to_integer_query = "SELECT WordId FROM WordsToInteger WHERE BookId = %s"
                cursor.execute(get_words_to_integer_query, (book_id,))
                self.text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)
                
                
                if include_filtered:
                    get_filtered_books_query = "SELECT WordId FROM FilteredBooks WHERE BookId = %s"
                    cursor.execute(get_filtered_books_query, (book_id,))
                    self.filtered_text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)

                if include_lemmatized:
                    get_lemmatized_books_query = "SELECT WordId FROM LemmatizedBooks WHERE BookId = %s"
                    cursor.execute(get_lemmatized_books_query, (book_id,))
                    self.lemmatized_text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)
                
                # define a set of values that will not be used when running certain analyses on the book text (default = non-alphanumerics). Change with set/add/remove methods below
                query = f"SELECT Id, Word FROM {self.language_name}dictionary"  
                cursor.execute(query)
                words = cursor.fetchall()
        
                self.exclude = []
                for word_id, word in words:
                    if not re.fullmatch(r"[a-zA-Z0-9]+", word):  # Check for only non-alphanumeric
                        self.exclude.append(word_id)         
                #self.exclude = utils.get_non_alphanumerics(f"{self.language_name}dictionary", self.db_config) # decided to just copy the code from utility functions to avoid setting up extra database connections
                
                # Find line break (\n) in the relevant dictionary table and save it locally
                query = f"SELECT Id FROM {self.language_name}dictionary WHERE Word = '\n'"  
                cursor.execute(query)
                self.line_break = cursor.fetchone()[0]
                

    # Getters
    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_language(self):
        return self.language

    def get_release_date(self):
        return self.release_date

    def get_word_count(self):
        return self.word_count

    def get_character_count(self):
        return self.character_count

    def get_source_website(self):
        return self.source_website

    
    # get all words in the text at parameter indices 
    def get_text_at_indices(self, indices):
        return [self.text[i] for i in indices]        
    def get_filtered_text_at_indices(self, indices):
        return [self.filtered_text[i] for i in indices]
    def get_lemmatized_text_at_indices(self, indices):
        return [self.lemmatized_text[i] for i in indices]
    
    # Setters 
    def set_title(self, new_title):
        self.title = new_title

    def set_author(self, new_author):
        self.author = new_author

    def set_language(self, new_language):
        self.language = new_language

    def set_release_date(self, new_date):
        self.release_date = new_date

    def set_word_count(self):
        self.word_count = self.text.size # add conditions here, like removing all entries that correspond to .,_-[/}!?< etc.

    def set_character_count(self, new_character_count):
        self.character_count = new_character_count  # this requires you to convert the book to text before counting, so it will be done outside the object somewhere

    def set_source_website(self, new_link):
        self.source_website = new_link

    def set_words_to_integer(self, new_text):
        if isinstance(new_text, np.ndarray):
            self.text = new_text
        else:
            print("input is not a numpy array")

    def set_excluded_values(self, excluded_values):
        self.exclude = excluded_values
        
    def set_filtered_books(self, new_filtered_text):
        if self.filtered_text is not None:
            if isinstance(new_filtered_text, np.ndarray):
                self.filtered_text = new_filtered_text
            else:
                print("input is not a numpy array")
        else:
            raise AttributeError("Filtered books data is not available for this object.")

    def set_lemmatized_books(self, new_lemmatization):
        if self.lemmatized_text is not None:
            if isinstance(new_lemmatization, np.ndarray):
                self.lemmatized_text = new_lemmatization
            else:
                print("input is not a numpy array")
        else:
            raise AttributeError("Lemmatized books data is not available for this object.")
                    
                        
    def get_text(self):
        return self.text

    def get_filtered_text(self):
        if self.filtered_text is not None:
            return self.filtered_text
        else:
            raise AttributeError("Filtered books data is not available for this object.")

    def get_lemmatized_text(self):
        if self.lemmatized_text is not None:
            return self.lemmatized_text
        else:
            raise AttributeError("Lemmatized books data is not available for this object.")
    def get_excluded_values(self):
        return self.exclude
               
    # Reuploads the book data to the database, replacing existing entries.
    def reupload_to_database(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()

            # Delete existing entries in related tables
            delete_words_to_integer_query = "DELETE FROM WordsToInteger WHERE BookId = %s"
            cursor.execute(delete_words_to_integer_query, (self.book_id,))

            if self.filtered_text is not None:
                delete_filtered_books_query = "DELETE FROM FilteredBooks WHERE BookId = %s"
                cursor.execute(delete_filtered_books_query, (self.book_id,))

            if self.lemmatized_text is not None:
                delete_lemmatized_books_query = "DELETE FROM LemmatizedBooks WHERE BookId = %s"
                cursor.execute(delete_lemmatized_books_query, (self.book_id,))

            # Update book entry
            update_book_query = """
                UPDATE book
                SET 
                    Title = %s,
                    Author = %s,
                    Language = %s,
                    ReleaseDate = %s,
                    WordCount = %s,
                    CharacterCount = %s,
                    SourceWebsite = %s
                WHERE id = %s
            """
            update_data = (self.title, self.author, self.language, self.release_date, 
                           self.word_count, self.character_count, self.source_website, self.book_id)
            cursor.execute(update_book_query, update_data)

            # Insert new word IDs
            insert_book_text_query = """
                INSERT INTO WordsToInteger (WordId, BookId) 
                VALUES (%s, %s)
            """
            for word_id in self.text:
                cursor.execute(insert_book_text_query, (word_id, self.book_id))

            if self.filtered_text is not None:
                insert_filtered_text_query = """
                    INSERT INTO FilteredBooks (WordId, BookId) 
                    VALUES (%s, %s)
                """
                for word_id in self.filtered_text:
                    cursor.execute(insert_filtered_text_query, (word_id, self.book_id))

            if self.lemmatized_text is not None:
                insert_lemmatized_text_query = """
                    INSERT INTO LemmatizedBooks (WordId, BookId) 
                    VALUES (%s, %s)
                """
                for word_id in self.lemmatized_text:
                    cursor.execute(insert_lemmatized_text_query, (word_id, self.book_id))

            cnx.commit()

        except mysql.connector.Error as err:
            print(f"Error reuploading book to database: {err}")
        finally:
            if cnx:
                cnx.close()              

    #Compares the book object's attributes with the database and returns a list of booleans indicating whether each attribute differs from the database.
    def compare_with_database(self):  
        differs_list = [False] * 10  # Initialize with 10 False values

        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()

            # Fetch book details from the database
            get_book_query = "SELECT * FROM book WHERE id = %s"
            cursor.execute(get_book_query, (self.book_id,))
            db_book_data = cursor.fetchone()

            if db_book_data:
                # Compare attributes
                differs_list[0] = self.title != db_book_data['Title']
                differs_list[1] = self.author != db_book_data['Author']
                differs_list[2] = self.language != db_book_data['Language']
                differs_list[3] = self.release_date != db_book_data['ReleaseDate']
                differs_list[4] = self.word_count != db_book_data['WordCount']
                differs_list[5] = self.character_count != db_book_data['CharacterCount']
                differs_list[6] = self.source_website != db_book_data['SourceWebsite']

                # Compare text
                db_words_to_integer = []
                get_words_to_integer_query = "SELECT WordId FROM WordsToInteger WHERE BookId = %s"
                cursor.execute(get_words_to_integer_query, (self.book_id,))
                for row in cursor.fetchall():
                    db_words_to_integer.append(row[0])
                differs_list[7] = not np.array_equal(self.text, np.array(db_words_to_integer))

                # Compare filtered_text if available
                if self.filtered_text is not None:
                    db_filtered_books = []
                    get_filtered_books_query = "SELECT WordId FROM FilteredBooks WHERE BookId = %s"
                    cursor.execute(get_filtered_books_query, (self.book_id,))
                    for row in cursor.fetchall():
                        db_filtered_books.append(row[0])
                    differs_list[8] = not np.array_equal(self.filtered_text, np.array(db_filtered_books))

                # Compare lemmatized_text if available
                if self.lemmatized_text is not None:
                    db_lemmatized_books = []
                    get_lemmatized_books_query = "SELECT WordId FROM LemmatizedBooks WHERE BookId = %s"
                    cursor.execute(get_lemmatized_books_query, (self.book_id,))
                    for row in cursor.fetchall():
                        db_lemmatized_books.append(row[0])
                    differs_list[9] = not np.array_equal(self.lemmatized_text, np.array(db_lemmatized_books))

        except mysql.connector.Error as err:
            print(f"Error comparing book with database: {err}")
            return None
        finally:
            if cnx:
                cnx.close()
        return differs_list
    
    # Replaces the internal variables of the Book object with the corresponding values from the database.
    def replace_with_database_values(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()

            # Fetch book details from the database
            get_book_query = "SELECT * FROM book WHERE id = %s"
            cursor.execute(get_book_query, (self.book_id,))
            book_data = cursor.fetchone()

            if book_data:
                self.title = book_data['Title']
                self.author = book_data['Author']
                self.language = book_data['Language']
                self.release_date = book_data['ReleaseDate']
                self.word_count = book_data['WordCount']
                self.character_count = book_data['CharacterCount']
                self.source_website = book_data['SourceWebsite']

                # Fetch word IDs from related tables
                get_words_to_integer_query = "SELECT WordId FROM wordstointeger WHERE BookId = %s"
                cursor.execute(get_words_to_integer_query, (self.book_id,))
                self.text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)

                if self.filtered_text is not None:
                    get_filtered_text_query = "SELECT WordId FROM FilteredBooks WHERE BookId = %s"
                    cursor.execute(get_filtered_text_query, (self.book_id,))
                    self.filtered_text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)

                if self.lemmatized_text is not None:
                    get_lemmatized_text_query = "SELECT WordId FROM LemmatizedBooks WHERE BookId = %s"
                    cursor.execute(get_lemmatized_text_query, (self.book_id,))
                    self.lemmatized_text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)

        except mysql.connector.Error as err:
            print(f"Error fetching book data: {err}")
        finally:
            if cnx:
                cnx.close()
                
    # Uploads a new book entry to the database with the values found in the object (regardless of whether it already exist).
    def upload_as_separate_book(self, db_config):
        try:
            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor()

            # Determine new title (to differentiate it from the book already in the database)
            new_title = self.title
            match = re.search(r" v(\d+)$", new_title)
            if match:
                version_number = int(match.group(1))
                new_title = new_title[:-(len(match.group(0)))] + f" v{version_number + 1}"
            else:
                new_title += " v2"

            # Check if language exists in languages table
            get_language_id_query = "SELECT id FROM languages WHERE Language = %s"
            cursor.execute(get_language_id_query, (self.language,))
            language_id = cursor.fetchone()

            # Check if author exists in authors table
            get_author_id_query = "SELECT id FROM authors WHERE Name = %s"
            cursor.execute(get_author_id_query, (self.author,))
            author_id = cursor.fetchone()

            # Insert new book entry
            insert_query = """
                INSERT INTO book (Title, Author_id, Language, ReleaseDate, WordCount, CharacterCount, StoredAndProcessed, SourceWebsite)
                VALUES (%s, %s, %s, %s, %s, %s, 'TRUE', %s)
            """
            insert_data = (new_title, author_id[0], language_id[0], self.release_date, self.word_count, 
                           self.character_count, self.source_website)
            cursor.execute(insert_query, insert_data)
            new_book_id = cursor.lastrowid

            # Insert word IDs into WordsToInteger table
            insert_book_text_query = """
                INSERT INTO WordsToInteger (WordId, BookId) 
                VALUES (%s, %s)
            """
            for word_id in self.text:
                cursor.execute(insert_book_text_query, (word_id, new_book_id))

            if self.filtered_text is not None:
                insert_filtered_text_query = """
                    INSERT INTO FilteredBooks (WordId, BookId) 
                    VALUES (%s, %s)
                """
                for word_id in self.filtered_text:
                    cursor.execute(insert_filtered_text_query, (word_id, new_book_id))

            if self.lemmatized_text is not None:
                insert_lemmatized_text_query = """
                    INSERT INTO LemmatizedBooks (WordId, BookId) 
                    VALUES (%s, %s)
                """
                for word_id in self.lemmatized_text:
                    cursor.execute(insert_lemmatized_text_query, (word_id, new_book_id))

            cnx.commit()

        except mysql.connector.Error as err:
            print(f"Error uploading as separate book: {err}")
        finally:
            if cnx:
                cnx.close()
        
    # Add word to text
    def add_word_to_text(self, word_id, index=None):
        if index is None:
            self.text = np.append(self.text, word_id)
            self.filtered_text = np.append(self.filtered_text, word_id)
            self.text = np.append(self.text, word_id)
        else:
            self.text = np.insert(self.text, index, word_id)
            self.filtered_text = np.insert(self.filtered_text, index, word_id)
            self.lemmatized_texttext = np.insert(self.lemmatized_texttext, index, word_id)
        
        

    # Replace word in integer arrays
    def replace_word_in_text(self, old_word_id, new_word_id):
        self.text[self.text == old_word_id] = new_word_id
        
    # Find placement of a word in the text. defaults to regular text, unless filtered/lemmatized text is specified.
    def find_placement(self, word_id, array_type="text"):
        if array_type == "text":
            try:
                return np.where(self.text == word_id)[0][0]
            except IndexError:
                raise ValueError("Word not found in text array.")
        elif array_type == "filtered_text" and self.filtered_text is not None:
            try:
                return np.where(self.filtered_text == word_id)[0][0]
            except IndexError:
                raise ValueError("Word not found in filtered_text array.")
        elif array_type == "lemmatized_text" and self.lemmatized_text is not None:
            try:
                return np.where(self.lemmatized_text == word_id)[0][0]
            except IndexError:
                raise ValueError("Word not found in lemmatized_text array.")
        else:
            raise ValueError("Invalid array_type or data not available.")

    # Find number of occurrences of word in text arrays
    def find_number_of(self, word_id, array_type="text"):
        if array_type == "text":
            return np.count_nonzero(self.text == word_id)
        elif array_type == "filtered_text" and self.filtered_text is not None:
            return np.count_nonzero(self.filtered_text == word_id)
        elif array_type == "lemmatized_text" and self.lemmatized_text is not None:
            return np.count_nonzero(self.lemmatized_text == word_id)
        else:
            raise ValueError("Invalid array_type or data not available.")

@lru_cache(maxsize=350000)   
def _get_all_word_lengths_from_dict(cursor, dictionary_table_name):
    get_word_lengths_query = f"SELECT Id, WordCharacterLength FROM {dictionary_table_name}"
    cursor.execute(get_word_lengths_query)
    word_lengths_dict = dict(cursor.fetchall())
    return word_lengths_dict
        
def get_longest_words(self, filtered_text=False, lemmatized_text=False):
    try:
        cnx = mysql.connector.connect(**self.db_config)
        cursor = cnx.cursor()

        dictionary_table_name = f"{self.language_name}dictionary"

        word_lengths = _get_all_word_lengths_from_dict(cursor, dictionary_table_name)
        
        # Decide which version of the text you want the longest word from
        if filtered_text and lemmatized_text:
            text = self.text # if both are set to true, use the regular text instead.
        elif filtered_text:
            text = self.filtered_text
        elif lemmatized_text:
            text = self.lemmatized_text
        else:
            text = self.text

        longest_length = 0
        for word_id in text:
            word_length = word_lengths.get(int(word_id))  # Direct lookup
            if word_length is not None:  #Handle cases where a word_id might not be in the dictionary
                longest_length = max(longest_length, word_length)

        longest_words_in_text = []
        for word_id in text:
            word_length = word_lengths.get(int(word_id)) # Direct Lookup
            if word_length == longest_length:
                longest_words_in_text.append(word_id)

        return longest_words_in_text

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if cnx:
            cnx.close()       

'''
