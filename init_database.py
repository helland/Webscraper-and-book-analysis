import mysql.connector

 
# Creates a MySQL database if it doesn't exist.
def create_database(db_config):
    try:
        connection = mysql.connector.connect(**db_config) #auth_plugin='mysql_native_password' 
            
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        connection.commit()
       
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
       
        if connection:
            connection.close()
# Creates tables in the specified MySQL database.
def create_tables(db_config):
  
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Create Languages table
        create_languages_table = """
        CREATE TABLE IF NOT EXISTS languages (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            Name TINYTEXT,
            NumberOfWordEntries INT,
            GutenbergLinkId INT
        )
        """
        cursor.execute(create_languages_table)
    
        # Create EnglishDictionary table
        create_english_dictionary_table = """
        CREATE TABLE IF NOT EXISTS englishdictionary (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            Word TINYTEXT,
            WordCharacterLength INT,
            WordType INT 
        )
        """
        cursor.execute(create_english_dictionary_table)
    
        # Create SourceWebsites table
        #create_source_websites_table = """
        #CREATE TABLE IF NOT EXISTS SourceWebsites (
        #    Id INT AUTO_INCREMENT PRIMARY KEY,
        #    PageName TEXT,
        #    MainPageLink TEXT,
        #    BookContentLink TEXT
        #)
        #"""
        #cursor.execute(create_source_websites_table)
    
        # Create Author table
        create_author_table = """
        CREATE TABLE IF NOT EXISTS author (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            Name TINYTEXT)
        """
        cursor.execute(create_author_table)
    
        # Create Categories table
        #create_categories_table = """
        #CREATE TABLE IF NOT EXISTS Categories (
        #    Id INT AUTO_INCREMENT PRIMARY KEY,
        #    Name TEXT,
        #    SubcategoryOf INT
        #)
        #"""
        #cursor.execute(create_categories_table)
    
        # Create Book table
        create_book_table = """
        CREATE TABLE IF NOT EXISTS book (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            SourceWebsite TINYTEXT,
            StoredAndProcessed TINYINT DEFAULT 0,
            Title TINYTEXT,
            Language INT,
            Author INT,
            WordCount INT DEFAULT 0,
            CharacterCount INT DEFAULT 0,
            ReleaseDate DATETIME
        )
        """
        cursor.execute(create_book_table)
    
        # Create WordsToInteger table
        create_words_to_integer_table = """
        CREATE TABLE IF NOT EXISTS wordstointeger (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            WordId INT,
            BookId INT
        )
        """
        cursor.execute(create_words_to_integer_table)
    
        # Create FilteredBooks table
        create_filtered_books_table = """
        CREATE TABLE IF NOT EXISTS filteredbooks (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            WordId INT,
            BookId INT
        )
        """
        cursor.execute(create_filtered_books_table)
    
        # Create LemmatizedBooks table
        create_lemmatized_books_table = """
        CREATE TABLE IF NOT EXISTS lemmatizedbooks (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            WordId INT,
            BookId INT
        )
        """
        cursor.execute(create_lemmatized_books_table)
    
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
    finally:
        if connection:
            connection.close()

db_config = {
'host': 'localhost',
'user': 'root',
'password': 'pass',
'database': 'book_project',
'use_pure': 'True'}


create_database(db_config)
create_tables(db_config)

