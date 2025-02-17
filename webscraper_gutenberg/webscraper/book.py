import mysql.connector
import numpy as np
import re

class Book:
    def __init__(self, book_id, db_config): # , include_filtered=False, include_lemmatized=False
        self.book_id = book_id
        self.db_config = db_config

        # Initialize cached attributes to None
        self._title = None
        self._author = None
        self._language = None
        self._language_name = None
        self._release_date = None
        self._word_count = None
        self._character_count = None
        self._source_website = None
        self._text = None
        self._exclude = None
        self._line_break = None     # potential thing to add for later: list containing all indices containing linebreaks. This object should have an easy way to handle the book text both with and without the linebreaks. store the book twice (one with, one without)? decide later
        self._filtered_text = None
        self._lemmatized_text = None
        
        
    # Properties for book table values
    @property
    def title(self):
        if self._title is None:
            self._title = self._load_book_data()[3] if self._load_book_data() else None
        return self._title

    @property
    def author(self):
        if self._author is None:
            self._author = self._load_book_data()[5] if self._load_book_data() else None
        return self._author

    @property
    def language(self):
        if self._language is None:
            self._language = self._load_book_data()[4] if self._load_book_data() else None
        return self._language

    @property
    def release_date(self):
        if self._release_date is None:
            self._release_date = self._load_book_data()[8] if self._load_book_data() else None
        return self._release_date

    @property
    def word_count(self):
        if self._word_count is None:
            self._word_count = self._load_book_data()[6] if self._load_book_data() else None
        return self._word_count

    @property
    def character_count(self):
        if self._character_count is None:
            self._character_count = self._load_book_data()[7] if self._load_book_data() else None
        return self._character_count

    @property
    def source_website(self):
        if self._source_website is None:
            self._source_website = self._load_book_data()[1] if self._load_book_data() else None
        return self._source_website                   
  
    @property
    def text(self):
        if self._text is None:
            self._text = self._load_text()
        return self._text

    @property
    def filtered_text(self):
        if self._filtered_text is None: # REMOVED: Check if filtered text is enabled    and self.filtered_text is not None
            self._filtered_text = self._load_filtered_text()
        return self._filtered_text

    @property
    def lemmatized_text(self):
        if self._lemmatized_text is None: # REMOVED: Check if lemmatized text is enabled     and self.lemmatized_text is not None
            self._lemmatized_text = self._load_lemmatized_text()
        return self._lemmatized_text
    
    @property
    def exclude(self):
        if self._exclude is None:
            self._exclude = self._load_excluded_values()
        return self._exclude

    @property
    def line_break(self):
        if self._line_break is None:
            self._line_break = self._load_line_break()
        return self._line_break

    @property
    def language_name(self):
        if self._language_name is None:
            self._language_name = self._load_language_name()
        return self._language_name

    # connect to database and get the book data only if the values can't be found in the cache
    def _load_book_data(self):   
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()
            get_book_query = "SELECT * FROM book WHERE id = %s"
            cursor.execute(get_book_query, (self.book_id,))
            book_data = cursor.fetchone()
            return book_data  # Return the tuple of book data
        except mysql.connector.Error as err:
            print(f"Error loading book data: {err}")
            return None
        finally:
            if cnx:
                cnx.close()
                
    
    def _load_text(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()
            get_words_to_integer_query = "SELECT WordId FROM WordsToInteger WHERE BookId = %s"
            cursor.execute(get_words_to_integer_query, (self.book_id,))
            text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)
            return text
        except mysql.connector.Error as err:
            print(f"Error loading text: {err}")
            return None # Handle error, return None or empty array
        finally:
            if cnx:
                cnx.close()

    def _load_filtered_text(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()
            get_filtered_books_query = "SELECT WordId FROM FilteredBooks WHERE BookId = %s"
            cursor.execute(get_filtered_books_query, (self.book_id,))
            filtered_text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)
            return filtered_text
        except mysql.connector.Error as err:
            print(f"Error loading filtered text: {err}")
            return None
        finally:
            if cnx:
                cnx.close()

    def _load_lemmatized_text(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()
            get_lemmatized_books_query = "SELECT WordId FROM LemmatizedBooks WHERE BookId = %s"
            cursor.execute(get_lemmatized_books_query, (self.book_id,))
            lemmatized_text = np.array([row[0] for row in cursor.fetchall()], dtype=np.int32)
            return lemmatized_text
        except mysql.connector.Error as err:
            print(f"Error loading lemmatized text: {err}")
            return None
        finally:
            if cnx:
                cnx.close()

    def _load_excluded_values(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()
            query = f"SELECT Id, Word FROM {self.language_name}dictionary"  
            cursor.execute(query)
            words = cursor.fetchall()
            exclude = []
            for word_id, word in words:
                if not re.fullmatch(r"[a-zA-Z0-9]+", word):
                    exclude.append(word_id)
            return exclude
        except mysql.connector.Error as err:
            print(f"Error loading excluded values: {err}")
            return None
        finally:
            if cnx:
                cnx.close()
    
    def _load_language_name(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()
            query = f"SELECT Name FROM Languages WHERE id = %s"  
            cursor.execute(query, (self.language,))       
            language_name = cursor.fetchone()[0]
            return language_name
        except mysql.connector.Error as err:
            print(f"Error loading line break: {err}")
            return None
        finally:
            if cnx:
                cnx.close()

    def _load_line_break(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()
            query = f"SELECT Id FROM {self.language_name}dictionary WHERE Word = '\n'"  
            cursor.execute(query)
            line_break = cursor.fetchone()[0]
            return line_break
        except mysql.connector.Error as err:
            print(f"Error loading line break: {err}")
            return None
        finally:
            if cnx:
                cnx.close()

    
    # get all words in the text at parameter indices 
    def get_text_at_indices(self, indices):
        return [self.text[i] for i in indices]        
    def get_filtered_text_at_indices(self, indices):
        return [self.filtered_text[i] for i in indices]
    def get_lemmatized_text_at_indices(self, indices):
        return [self.lemmatized_text[i] for i in indices]
    
    # Setters 
    @text.setter
    def text(self, new_text):
        if isinstance(new_text, np.ndarray):
            self.text = new_text
        else:
            print("input is not a numpy array")
        
    @filtered_text.setter
    def filtered_books(self, new_filtered_text):
        if self.filtered_text is not None:
            if isinstance(new_filtered_text, np.ndarray):
                self.filtered_text = new_filtered_text
            else:
                print("input is not a numpy array")
        else:
            raise AttributeError("Filtered books data is not available for this object.")

    @lemmatized_text.setter
    def lemmatized_books(self, new_lemmatization):
        if self.lemmatized_text is not None:
            if isinstance(new_lemmatization, np.ndarray):
                self.lemmatized_text = new_lemmatization
            else:
                print("input is not a numpy array")
        else:
            raise AttributeError("Lemmatized books data is not available for this object.")
  
    @title.setter
    def title(self, new_title):
        self.title = new_title
    
    @author.setter
    def author(self, new_author):
        self.author = new_author

    @language.setter
    def language(self, new_language):
        self.language = new_language

    @release_date.setter
    def release_date(self, new_date):
        self.release_date = new_date
        
    @word_count.setter
    def word_count(self):
        self.word_count = self.text.size # add conditions here, like removing all entries that correspond to .,_-[/}!?< etc.

    @character_count.setter
    def character_count(self, new_character_count):
        self.character_count = new_character_count  # this requires you to convert the book to text before counting, so it will be done outside the object somewhere

    @source_website.setter
    def source_website(self, new_link):
        self.source_website = new_link
   
    @exclude.setter
    def excluded(self, excluded_values):
        self.exclude = excluded_values
        
    def add_excluded_value(self, add):
        self.exclude.append(add)
        
    def remove_excluded_value(self, value):
        if value in self.exclude:
            self.exclude.remove(value)

    # Remove word from text
    def remove_word_from_text(self, word_id):
        try:
            self._text = np.delete(self._text, np.where(self._text == word_id))   
            if self._filtered_text is not None:  
                self._filtered_text = np.delete(self._filtered_text, np.where(self._filtered_text == word_id))
            if self._lemmatized_text is not None:
                self._lemmatized_text = np.delete(self._lemmatized_text, np.where(self._lemmatized_text == word_id))
        except ValueError:
            pass  # Word not found
      
    # TODO - add method for removing text from index placement and method to add word where another word is found
