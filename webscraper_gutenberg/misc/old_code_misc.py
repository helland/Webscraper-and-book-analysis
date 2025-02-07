 from bs4 import BeautifulSoup
import requests
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')

#search_term = input("What product do you want to search for? ")

url = "https://www.gutenberg.org/browse/titles/"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}
pages = ["a.html.utf8", "b.html.utf8","c.html.utf8","d.html.utf8",
         "e.html.utf8","f.html.utf8","g.html.utf8","h.html.utf8",
         "i.html.utf8","j.html.utf8","k.html.utf8","l.html.utf8",
         "m.html.utf8","n.html.utf8","o.html.utf8","p.html.utf8",
         "q.html.utf8","r.html.utf8","s.html.utf8","t.html.utf8",
         "u.html.utf8","v.html.utf8","w.html.utf8","x.html.utf8",
         "y.html.utf8","z.html.utf8",]
for page in pages:
    url = f"https://www.gutenberg.org/browse/titles/{page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(search_term))

    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue

        link = parent['href']
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(",", "")), "link": link}
        except:
            pass

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("-----------------")
    print("")












# Stores a book (or large string) in the database, including filtered and lemmatized versions. NOTE: a version of this code was used in the scraper file
def store_book_in_database(text, language, host, user, password, database_name):
    try:
        # Connect to the database
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )
        cursor = cnx.cursor()

        # Get language ID from Languages table
        get_language_id_query = "SELECT Id FROM Languages WHERE Language = %s"
        cursor.execute(get_language_id_query, (language,))
        language_id = cursor.fetchone()

        if language_id:
            language_id = language_id[0]  # Get the ID from the tuple

            # Determine dictionary table name based on language
            dictionary_table_name = f"{language.lower()}Dictionary" 

            # Get all words from the text
            words = re.findall(r"[\w']+|[.,!?;:\_\-\—\(\)\[\]\{\}\"\']", text)
            
            stop_words = set(stopwords.words(language))                                     # Get stopwords for the given language
            filtered_words = [word for word in words if word.lower() not in stop_words]     # Filter stopwords

            # Lemmatize words
            lemmatizer = WordNetLemmatizer()
            lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

            # Lists to store word IDs
            word_ids = []
            filtered_word_ids = []
            lemmatized_word_ids = []

            # Insert words into dictionary and get IDs
            for i, word in enumerate(words):
                get_word_id_query = f"SELECT Id FROM {dictionary_table_name} WHERE Word = %s"
                cursor.execute(get_word_id_query, (word,))
                existing_word_id = cursor.fetchone()

                if existing_word_id:
                    word_ids.append(existing_word_id[0])
                else:
                    insert_word_query = f"""
                    INSERT INTO {dictionary_table_name} (Word, WordCharacterLength) 
                    VALUES (%s, %s)
                    """
                    cursor.execute(insert_word_query, (word, len(word)))
                    word_ids.append(cursor.lastrowid)

                # Get ID for filtered word
                filtered_word = filtered_words[i]
                get_filtered_word_id_query = f"SELECT Id FROM {dictionary_table_name} WHERE Word = %s"
                cursor.execute(get_filtered_word_id_query, (filtered_word,))
                existing_filtered_word_id = cursor.fetchone()

                if existing_filtered_word_id:
                    filtered_word_ids.append(existing_filtered_word_id[0])
                else:
                    insert_filtered_word_query = f"""
                    INSERT INTO {dictionary_table_name} (Word, WordCharacterLength) 
                    VALUES (%s, %s)
                    """
                    cursor.execute(insert_filtered_word_query, (filtered_word, len(filtered_word)))
                    filtered_word_ids.append(cursor.lastrowid)

                # Get ID for lemmatized word
                lemmatized_word = lemmatized_words[i]
                get_lemmatized_word_id_query = f"SELECT Id FROM {dictionary_table_name} WHERE Word = %s"
                cursor.execute(get_lemmatized_word_id_query, (lemmatized_word,))
                existing_lemmatized_word_id = cursor.fetchone()

                if existing_lemmatized_word_id:
                    lemmatized_word_ids.append(existing_lemmatized_word_id[0])
                else:
                    insert_lemmatized_word_query = f"""
                    INSERT INTO {dictionary_table_name} (Word, WordCharacterLength) 
                    VALUES (%s, %s)
                    """
                    cursor.execute(insert_lemmatized_word_query, (lemmatized_word, len(lemmatized_word)))
                    lemmatized_word_ids.append(cursor.lastrowid)

            # Get the next available BookId
            get_next_book_id_query = "SELECT MAX(BookId) FROM WordsToInteger"
            cursor.execute(get_next_book_id_query)
            max_book_id = cursor.fetchone()[0]
            if max_book_id is None:
                max_book_id = 0
            book_id = max_book_id + 1

            # Insert word IDs into WordsToInteger table
            insert_words_to_integer_query = f"""
            INSERT INTO WordsToInteger (WordId, BookId) 
            VALUES (%s, %s)
            """
            for word_id in word_ids:
                cursor.execute(insert_words_to_integer_query, (word_id, book_id))

            # Insert filtered word IDs into FilteredBooks table
            insert_filtered_books_query = f"""
            INSERT INTO FilteredBooks (WordId, BookId) 
            VALUES (%s, %s)
            """
            for filtered_word_id in filtered_word_ids:
                cursor.execute(insert_filtered_books_query, (filtered_word_id, book_id))

            # Insert lemmatized word IDs into LemmatizedBooks table
            insert_lemmatized_books_query = f"""
            INSERT INTO LemmatizedBooks (WordId, BookId) 
            VALUES (%s, %s)
            """
            for lemmatized_word_id in lemmatized_word_ids:
                cursor.execute(insert_lemmatized_books_query, (lemmatized_word_id, book_id))

            cnx.commit()
            print(f"Book successfully stored in database with BookId: {book_id}")

        else:
            print(f"Language '{language}' not found in the Languages table.")

    except mysql.connector.Error as err:
        print(f"Error storing book in database: {err}")

    finally:
        if cnx:
            cnx.close()





# Convert the book text to integers, filter it and lemmatize it and store these sets of numbers in the database.
def encode_filter_and_lemmatize_book(book_id, text, db_config):
    # make sure the book id is valid
    if book_id > 0:        
        try:
            # Connect to the database
            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor(buffered=True)
            
            # get language id based on book id
            get_language_id_query = "SELECT Language FROM book WHERE id = %s"
            cursor.execute(get_language_id_query, (book_id,))
            language_id = cursor.fetchone() 
            language_id = language_id[0]  # Get the ID from the tuple
                        
            # Get language name from Languages table with given id
            get_language_id_query = "SELECT Language FROM Languages WHERE id = %s"
            cursor.execute(get_language_id_query, (language_id[0],))
            language = cursor.fetchone()

            
            # Determine dictionary table name based on language
            dictionary_table_name = f"{language.lower()}dictionary" 
            print(f"dictionary found: {dictionary_table_name}")       
            
            if language_id:       
                words = re.findall(r"[\w']+|[.,\_!?;:\-\—\(\)\[\]\{\}\"]", text)             # Get all words from the text
                stop_words = set(stopwords.words(language))                                  # Get stopwords for the given language
                filtered_words = [word for word in words if word.lower() not in stop_words]  # Filter stopwords
                lemmatizer = WordNetLemmatizer()                                             
                lemmatized_words = [lemmatizer.lemmatize(word) for word in words]            # Lemmatize text
                 
                # Lists to store word IDs
                word_ids            = np.zeros(len(words))
                filtered_word_ids   = np.zeros(len(filtered_words))
                lemmatized_word_ids = np.zeros(len(lemmatized_words))
                
                # Here I want to fetch all words in the dictionary and their IDs.
                # the word_ids array should be filled out with the id value of the dictionary table row where "Word" is equal to the word found in the "words" list at the same index
                # the filtered_word_ids array should be filled out with the id value of the dictionary table row where "Word" is equal to the word found in the "filtered_words" list at the same index
                # the lemmatized_word_ids array should be filled out with the id value of the dictionary table row where "Word" is equal to the word found in the "lemmatized_words" list at the same index
                 
                # I'd like the remaining code to be altered so that it only handles the remaining words in "words", "filtered_words" and "lemmatized_words" at indexes where "word_ids", "filtered_word_ids" and "lemmatized_word_ids" are still equal to zero.
                # It should take the words in "words", "filtered_words" and "lemmatized_words" that did not have an entry in the "Word" column of the dictionary table equal to its text value and add them to the dictionary, then take their id values and replace the remaining zeroes in the ID arrays with the ID value of the new words added to the dictionary.
                # Once the id arrays have been filled with id values representing the text of the previous word lists, add all values of the word_ids to the table "wordstointeger" with "WordId" equal to the word_id value and "BookId" equal to book_id. Do the same for "filtered_word_ids" in the table "filteredbooks" and "lemmatized_word_ids" in the "lemmatizedbooks" table.
                
                # Insert words into dictionary and get IDs
                for i, word in enumerate(words):
                    get_word_id_query = f"SELECT Id FROM {dictionary_table_name} WHERE Word = %s"
                    cursor.execute(get_word_id_query, (word,))
                    existing_word_id = cursor.fetchone()
    
                    if existing_word_id:
                        word_ids.append(existing_word_id[0])
                    else:
                        insert_word_query = f"""
                        INSERT INTO {dictionary_table_name} (Word, WordCharacterLength) 
                        VALUES (%s, %s)
                        """
                        cursor.execute(insert_word_query, (word, len(word)))
                        word_ids.append(cursor.lastrowid)
                        #print(f"The word '{word}' ({len(word)}) has been added to {dictionary_table_name}.")
                           
                # Insert words from the stopword filtered text into dictionary and get IDs
                for i, word in enumerate(filtered_words):
                    # Get ID for filtered word
                    filtered_word = filtered_words[i]                                                       
                    get_filtered_word_id_query = f"SELECT Id FROM {dictionary_table_name} WHERE Word = %s"
                    cursor.execute(get_filtered_word_id_query, (filtered_word,))
                    existing_filtered_word_id = cursor.fetchone()
                    
                    # NOTE: delete after double check, assuming its redundant (as i expect it to be) - turned out not to be
                    if existing_filtered_word_id:
                        filtered_word_ids.append(existing_filtered_word_id[0])
                    else:
                        insert_filtered_word_query = f"""
                        INSERT INTO {dictionary_table_name} (Word, WordCharacterLength) 
                        VALUES (%s, %s)
                        """
                        cursor.execute(insert_filtered_word_query, (filtered_word, len(filtered_word)))
                        filtered_word_ids.append(cursor.lastrowid)
                        
                # Insert words from the lemmatized text into dictionary and get IDs
                for i, word in enumerate(lemmatized_words):
                    # Get ID for lemmatized word
                    lemmatized_word = lemmatized_words[i]
                    get_lemmatized_word_id_query = f"SELECT Id FROM {dictionary_table_name} WHERE Word = %s"
                    cursor.execute(get_lemmatized_word_id_query, (lemmatized_word,))
                    existing_lemmatized_word_id = cursor.fetchone()
                    
                    # NOTE: delete after double check, assuming its redundant (as i expect it to be) - turned out not to be
                    if existing_lemmatized_word_id:
                        lemmatized_word_ids.append(existing_lemmatized_word_id[0])
                    else:
                        insert_lemmatized_word_query = f"""
                        INSERT INTO {dictionary_table_name} (Word, WordCharacterLength) 
                        VALUES (%s, %s)
                        """
                        cursor.execute(insert_lemmatized_word_query, (lemmatized_word, len(lemmatized_word)))
                        lemmatized_word_ids.append(cursor.lastrowid)
                        #print(f"The word '{word}' has been added to the dictionary via lemmatizaton.") # NOTE: this code will likely be deleted. just need to double check first
                        
                # Insert word IDs into wordstointeger table
                insert_words_to_integer_query = f"""
                INSERT INTO wordstointeger (WordId, BookId) 
                VALUES (%s, %s)
                """
                print("inserting the encoded book into the database")
                for word_id in word_ids:
                    cursor.execute(insert_words_to_integer_query, (word_id, book_id))
                print("Encoded book added to database.")
                # Insert filtered word IDs into filteredbooks table
                insert_filtered_books_query = f"""
                INSERT INTO filteredbooks (WordId, BookId) 
                VALUES (%s, %s)
                """
                for filtered_word_id in filtered_word_ids:
                    cursor.execute(insert_filtered_books_query, (filtered_word_id, book_id))
                print("filtered book added to database.")
                # Insert lemmatized word IDs into lemmatizedbooks table
                insert_lemmatized_books_query = f"""
                INSERT INTO lemmatizedbooks (WordId, BookId) 
                VALUES (%s, %s)
                """
                for lemmatized_word_id in lemmatized_word_ids:
                    cursor.execute(insert_lemmatized_books_query, (lemmatized_word_id, book_id))
                print("Lemmatized book added to database.")
                
                # Update the word count of the book's language, in case new words were added to the dictionary
                get_word_count_query = f"SELECT COUNT(*) FROM {dictionary_table_name}" # Get number of entries in the dictionary table
                cursor.execute(get_word_count_query)
                word_count = cursor.fetchone()[0] 
        
                # Update NumberOfWordEntries in languages table
                update_query = "UPDATE languages SET NumberOfWordEntries = %s WHERE id = %s"
                cursor.execute(update_query, (word_count, language_id))
                print("language word count updated")
                
                cnx.commit()
        except mysql.connector.Error as err:
            print(f"Error storing book in database: {err}")
        finally:
            if cnx:
                cnx.close() 
                

# Stores book information in a MySQL database.
def store_book_in_database(title, text, author, release_date, language, word_count, character_count, source_website, db_config):
    book_id = -1
    
    try:
        # Connect to the database
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(buffered=True)
        
        # Check if book with the same title exists
        check_title_query = "SELECT * FROM book WHERE Title = %s"
        cursor.execute(check_title_query, (title,))
        existing_book = cursor.fetchone()

        
        # Check if language is correct
        get_language_id_query = "SELECT Name FROM languages WHERE id = %s"
        cursor.execute(get_language_id_query, (existing_book[4],))
        language_id = cursor.fetchone()
                          
        # Check if author exists in authors table
        get_author_id_query = "SELECT Name FROM author WHERE id = %s"
        cursor.execute(get_author_id_query, (existing_book[5],))
        author_id = cursor.fetchone()        

        # Check if a book by the same title is already stored in the database. NOTE: this should not be necessary, as checking the "source_website" is all we need to determine if the book is the same as input book  
        if existing_book:
            
            # Check if language and author match. If they do, assume it's the same book. NOTE: this should not be necessary, as checking the "source_website" is all we need to determine if the book is the same as input book
            if existing_book[4] != 0 and existing_book[5] != 0:                          
                
                # Update existing book
                update_query = """
                  UPDATE book
                  SET 
                    WordCount = %s,
                    CharacterCount = %s,
                    ReleaseDate = %s,
                    StoredAndProcessed = '1',
                    SourceWebsite = %s
                  WHERE Title = %s
                """
                update_data = (word_count, character_count, release_date, source_website, title)
                cursor.execute(update_query, update_data)
                book_id = existing_book[0]  # Get the ID of the updated book
                print(f"The book '{title}' already in the database has been updated.") 
            
            # A book with the same title was found, but by a different author or written in a differnet language. NOTE: this should not be necessary, as checking the "source_website" is all we need to determine if the book is the same as input book
            else:
                # Add new book entry
                insert_query = """
                  INSERT INTO book (Title, Author, Language, ReleaseDate, WordCount, CharacterCount, StoredAndProcessed, SourceWebsite)
                  VALUES (%s, %s, %s, %s, %s, %s, '1', %s)
                """
                insert_data = (title, existing_book[5], existing_book[4], release_date, word_count, character_count, source_website) #, author_id[0], language_id[0]
                cursor.execute(insert_query, insert_data)
                book_id = cursor.lastrowid  # Get the ID of the newly inserted book
                print(f"The book {title} ({book_id}) has been added to database.") 
        # No book matching the new entry was found. Add it as a new entry.
        else:
            print("book not found in database. storing...")
            # Check if the book's language exist in the database. if not, add it.
            if not language_id:
                insert_language_query = "INSERT INTO languages (Name) VALUES (%s)"
                cursor.execute(insert_language_query, (language,))
                cnx.commit()
                language_id = (cursor.lastrowid,)
                print(f"New language {language_id[1]} added to database.")
            # Check if the book's author exist in the database. if not, add them.
            if not author_id:
                insert_author_query = "INSERT INTO author (Name) VALUES (%s)"
                cursor.execute(insert_author_query, (author,))
                cnx.commit()
                author_id = (cursor.lastrowid,)
                print(f"New author  {author_id[1]} added to database.")    
            insert_query = """
                INSERT INTO book (Title, Author, Language, ReleaseDate, WordCount, CharacterCount, StoredAndProcessed, SourceWebsite)
                VALUES (%s, %s, %s, %s, %s, %s, '1', %s)
              """
            insert_data = (title, author_id[0], language_id[0], release_date, word_count, character_count, source_website)
            cursor.execute(insert_query, insert_data)
            book_id = cursor.lastrowid  # Get the ID of the newly inserted book
            print(f"Book ({book_id}) added to database.") 
        
        

        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error storing book in database: {err}")
    finally:
        if cnx:
            cnx.close()
    encode_filter_and_lemmatize_book(book_id, text, db_config)




# Stores book information in a MySQL database.
def store_book_in_database(title, text, author, release_date, language, word_count, character_count, source_website, db_config):
    book_id = -1

    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(buffered=True)

        # Check for existing book based on source_website
        check_source_query = "SELECT id FROM book WHERE SourceWebsite = %s"
        cursor.execute(check_source_query, (source_website,))
        existing_book_id = cursor.fetchone()

        if existing_book_id:
            # Book already exists, update existing entry
            update_query = """
                UPDATE book 
                SET Title = %s, Author = %s, Language = %s, ReleaseDate = %s, 
                    WordCount = %s, CharacterCount = %s 
                WHERE id = %s
            """
            update_data = (title, _get_or_insert_author(cursor, author), 
                           _get_or_insert_language(cursor, language), 
                           release_date, word_count, character_count, existing_book_id[0])
            cursor.execute(update_query, update_data)
            book_id = existing_book_id[0]
            print(f"Book with source_website '{source_website}' updated.")

        else:
            # Insert new book entry
            insert_query = """
                INSERT INTO book (Title, Author, Language, ReleaseDate, 
                                  WordCount, CharacterCount, StoredAndProcessed, SourceWebsite)
                VALUES (%s, %s, %s, %s, %s, %s, '0', %s)
            """
            insert_data = (title, _get_or_insert_author(cursor, author), 
                           _get_or_insert_language(cursor, language), 
                           release_date, word_count, character_count, source_website)
            cursor.execute(insert_query, insert_data)
            book_id = cursor.lastrowid
            print(f"New book added to database with ID: {book_id}")

        # Encode, filter, and lemmatize the book text
        encode_filter_and_lemmatize_book(book_id, text, cursor) 

        cnx.commit()

    except mysql.connector.Error as err:
        print(f"Error storing book in database: {err}")
    finally:
        if cnx:
            cnx.close()
            
            



'''
# takes a name "Title FirstName SecondName" and tangles it up to "SecondName, FirstName, Title"
def name_reformatter_tangle(name):
    partial_names = name.split(" ", 2)
    if len(partial_names) > 2:
         
        return formatted_name
    else:
         
        return formatted_name
'''
    
'''
        # Check if language exists in languages table
        get_language_id_query = "SELECT id FROM languages WHERE Language = %s"
        cursor.execute(get_language_id_query, (language,))
        language_id = cursor.fetchone()
        dictionary_table_name = f"{language.lower()}dictionary" # Determine dictionary table name based on the book's language
        print(f"dictionary table name: {dictionary_table_name}")
                         
        # Check if author exists in authors table
        get_author_id_query = "SELECT id FROM author WHERE Name = %s"
        cursor.execute(get_author_id_query, (author,))
        author_id = cursor.fetchone()
        print(author_id)
        # Create Dictionary table if it does not exist
        create_dictionary_table = f"""
                CREATE TABLE IF NOT EXISTS {dictionary_table_name} (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                Word TINYTEXT,
                WordCharacterLength INT,
                WordType INT 
                )"""
        cursor.execute(create_dictionary_table)
        
        
                        #note or tomorrow: print all here
                cursor.execute(f"SELECT * FROM {dictionary_table_name}")
                existing_words = cursor.fetchall()
                print(existing_words)
                print(dictionary_table_name)
                
                
                
        '''
'''
#stuff from setup_scraper:

db_config = {
    'host': 'localhost',
    'user': 'helland',
    'password': 'Ganymedes8787',
    'database': 'book_project',
    'use_pure': 'True'}
    
print(f"New language added to database. name = {book['Language']}, id = {language_id}")
    #print(f"New author added to database. id ={author_id}")  
            
            # Check database if book already exists based on Title, Author, Language
            #get_book_query = "SELECT * FROM book WHERE Title = %s AND Author = %s AND Language = %s"
            #values = (book['Title'], str(author_id), str(language_id))

            #cursor.execute(get_book_query, values)
            #duplicate_book = cursor.fetchone()
            #print(f"duplicate book: {duplicate_book}")
            #if duplicate_book:
            #    print(f"The book {book['Title']} has already been stored in the database.")
            #else:
            
            #print(f"Adding the book {book['Title']} ({book['Language']} - {language_id}) by {book['Author']} - {author_id} to the database - link: {book['SourceWebsite']}")
            


# links used to bypass the block on webscrapers (by looking at their previous entry in the internet archive)
bypass_url = ["https://web.archive.org/web/20241226212018/http://www.gutenberg.org/browse/titles/a.html.utf8",
              "https://web.archive.org/web/20240328023615/http://www.gutenberg.org/browse/titles/b.html.utf8",
              "https://web.archive.org/web/20241223131810/https://www.gutenberg.org/browse/titles/c.html.utf8",
              "https://web.archive.org/web/20240508133350/https://www.gutenberg.org/browse/titles/d.html.utf8",
              "https://web.archive.org/web/20240328023653/https://www.gutenberg.org/browse/titles/e.html.utf8",
              "https://web.archive.org/web/20241225190528/https://www.gutenberg.org/browse/titles/f.html.utf8",
              "https://web.archive.org/web/20241224142641/https://www.gutenberg.org/browse/titles/g.html.utf8",
              "https://web.archive.org/web/20240328023720/https://www.gutenberg.org/browse/titles/h.html.utf8",
              "https://web.archive.org/web/20240328023626/https://www.gutenberg.org/browse/titles/i.html.utf8",
              "https://web.archive.org/web/20241219215316/https://www.gutenberg.org/browse/titles/j.html.utf8",
              "https://web.archive.org/web/20240328023724/https://www.gutenberg.org/browse/titles/k.html.utf8",
              "https://web.archive.org/web/20240508133408/https://www.gutenberg.org/browse/titles/l.html.utf8",
              "https://web.archive.org/web/20240328023643/https://www.gutenberg.org/browse/titles/m.html.utf8",
              "https://web.archive.org/web/20240328023704/https://www.gutenberg.org/browse/titles/n.html.utf8",
              "https://web.archive.org/web/20240328023746/https://www.gutenberg.org/browse/titles/o.html.utf8",
              "https://web.archive.org/web/20240328023713/https://www.gutenberg.org/browse/titles/p.html.utf8",
              "https://web.archive.org/web/20240328023711/https://www.gutenberg.org/browse/titles/q.html.utf8",
              "https://web.archive.org/web/20240328023736/https://www.gutenberg.org/browse/titles/r.html.utf8",
              "https://web.archive.org/web/20240508134128/https://www.gutenberg.org/browse/titles/s.html.utf8",
              "https://web.archive.org/web/20241224230114/https://www.gutenberg.org/browse/titles/t.html.utf8",
              "https://web.archive.org/web/20241224210602/https://www.gutenberg.org/browse/titles/u.html.utf8",
              "https://web.archive.org/web/20241225082639/https://www.gutenberg.org/browse/titles/v.html.utf8",
              "https://web.archive.org/web/20240508133346/https://www.gutenberg.org/browse/titles/w.html.utf8",
              "https://web.archive.org/web/20240328023735/https://www.gutenberg.org/browse/titles/x.html.utf8",
              "https://web.archive.org/web/20241225183235/https://www.gutenberg.org/browse/titles/y.html.utf8",
              "https://web.archive.org/web/20240328023602/https://www.gutenberg.org/browse/titles/z.html.utf8"]

all_books = []
for url in bypass_url: 
    scraped_books = scrape_book_info(url)
    all_books.extend(scraped_books)
    
    # Pause for a bit between requests (in an attempt to not bother gutenberg/internet archive too much)
    time.sleep(5)


# Insert books into the database
insert_books_into_database(all_books)



        # Create the 'Book' table if it doesn't exist
        #create_table_query = """
        #CREATE TABLE IF NOT EXISTS book (
        #    Id INT AUTO_INCREMENT PRIMARY KEY,
        #    SourceWebsite TINYTEXT,
        #    StoredAndProcessed BOOLEAN DEFAULT FALSE,
        #    Title TEXT,
        #    Language INT,
        #    Author INT,
        #    WordCount INT DEFAULT 0,
        #    CharacterCount INT DEFAULT 0,
        #    ReleaseDate DATETIME
        #)
        #"""
        #cursor.execute(create_table_query)
        
                # add a table for the book's language if it's not already there
                #dictionary_table_name = f"{book['Language'].lower()}Dictionary" 
                #create_table_query = f"""
                #CREATE TABLE IF NOT EXISTS {dictionary_table_name} (
                #    Id INT AUTO_INCREMENT PRIMARY KEY,
                #    Word TEXT,
                #    WordCharacterLength INT,
                #    WordType INT )
                #"""
                
#for page in pages:
    #url = f"{url_base}{page}"                

# links to the actual sites that are to be scraped
url_base = "https://www.gutenberg.org/browse/titles/"
pages = ["a.html.utf8", "b.html.utf8", "c.html.utf8", "d.html.utf8",
         "e.html.utf8", "f.html.utf8", "g.html.utf8", "h.html.utf8",
         "i.html.utf8", "j.html.utf8", "k.html.utf8", "l.html.utf8",
         "m.html.utf8", "n.html.utf8", "o.html.utf8", "p.html.utf8",
         "q.html.utf8", "r.html.utf8", "s.html.utf8", "t.html.utf8",
         "u.html.utf8", "v.html.utf8", "w.html.utf8", "x.html.utf8",
         "y.html.utf8", "z.html.utf8"]


for i in range(0, len(all_books), 10):
    print(f"Author: {all_books[i]['Author']} - language: {all_books[i]['Language']}")  
    
            #if len(title) >= 64:
            #    title = title.rsplit(".", 1)[0] # if the title is too long, remove everything past the last punctuation
            #    if len(title) >= 64:
            #        title = title.rsplit(",", 1)[0] # if the title is still too long, remove everything past the last comma
  
'''
'''
# find the longest word (or words) in an inuput text
def find_longest_words(text, language_id, db_config):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Get language name from languages table
        get_language_query = "SELECT Name FROM languages WHERE id = %s"
        cursor.execute(get_language_query, (language_id,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Language with ID {language_id} not found.")
        language_name = result[0].lower() 

        # Create dictionary table name
        dictionary_table_name = f"{language_name}dictionary"

        # Find longest word character length
        longest_length = 0
        for word_id in text:
            get_word_length_query = f"SELECT WordCharacterLength FROM {dictionary_table_name} WHERE Id = %s"
            cursor.execute(get_word_length_query, (word_id,))
            result = cursor.fetchone()
            if result:
                word_length = result[0]
                longest_length = max(longest_length, word_length)

        # Find IDs of words with longest length
        longest_words_in_text = []
        for word_id in text:
            get_word_length_query = f"SELECT WordCharacterLength FROM {dictionary_table_name} WHERE Id = %s"
            cursor.execute(get_word_length_query, (word_id,))
            result = cursor.fetchone()
            if result and result[0] == longest_length:
                longest_words_in_text.append(word_id)

        return longest_words_in_text

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if cnx:
            cnx.close()

# Decodes an array of integers (word IDs) into a list of words by taking the whole dictionary from the database and comparing IDs (used for long encoded_texts)
def cipher_decoder(encoded_text, language_id, db_config):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        get_language_query = "SELECT Name FROM languages WHERE id = %s"
        cursor.execute(get_language_query, (language_id,))
        language_name = cursor.fetchone()[0].lower()
        dictionary_table_name = f"{language_name}dictionary"

        decoded_words = []

        # Get the entire dictionary
        word_dict = _get_all_words_from_dict(cursor, dictionary_table_name)

        # Convert encoded text to a list of ints if it's a NumPy array
        if isinstance(encoded_text, np.ndarray):
            encoded_text = encoded_text.tolist()
        
        # compare word IDs in the dictionary to the encoded text to find the word we're looking for
        for word_id in encoded_text:
            word = word_dict.get(int(word_id))  # dictionary lookup 
            if word:
                decoded_words.append(word)
            else:
                decoded_words.append(f"[ID {word_id} not found]")

        return decoded_words

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []

    finally:
        if cnx:
            cnx.close()       
'''            
'''
# find the word used most often in a text (converted to integer). excluding things like .,!?-_</
def find_most_frequent_word(text, exclude_values):
  
    # Create a mask to filter out excluded values
    mask = ~np.isin(text, exclude_values)
    filtered_arr = text[mask]
    
    if len(filtered_arr) == 0:
        return None  # No valid values remain after exclusion
    
    # Count occurrences of each value
    unique, counts = np.unique(filtered_arr, return_counts=True)
    
    # Find the index of the most frequent value
    most_frequent_index = np.argmax(counts)
    
    # Return the most frequent value
    return unique[most_frequent_index]

# Finds the 'number_of_words' most frequent words found in the text (converted to integer array)
def find_top_n_most_frequent(text, number_of_words):
    exclude_values = []
    top_n_values = []
    
    for _ in range(number_of_words):
        most_frequent = find_most_frequent_word(text, exclude_values)
        if most_frequent is None:
            break  # No more unique values found
        top_n_values.append(most_frequent)
        exclude_values.append(most_frequent)
    
    return top_n_values

# find words that only occur once in a text (converted to integers)
def find_unique_words(text, exclude_values):
   
    # Create a mask to filter out excluded values
    mask = ~np.isin(text, exclude_values)
    filtered_arr = text[mask]
    
    # Count occurrences of each value
    unique, counts = np.unique(filtered_arr, return_counts=True)
    
    # Find indices of unique values (occurring only once)
    unique_indices = np.where(counts == 1)[0]
    
    # Extract unique values that occur only once
    unique_values = unique[unique_indices]
    
    return unique_values

# generate a wordcloud from input text to filename file
def generate_wordcloud(text, filename):
    stopwords = STOPWORDS
    wc = WordCloud(background_color="white", stopwords=stopwords, height=600, width=400)
    wc.generate(text)
    wc.to_file(filename)

# split a text into sentences. Separator_array are values corresponding to sentence breakers (.!?:; and the ellipsis.) NOTE: separators can be hard coded... unless there really are other signs for ending sentences that I don't know about. possibly in other languages?
def split_text_by_sentences(text, separators):  
    sentences = []
    current_sentence = []
    
    for i in range(len(text)):
        current_value = text[i]
    
        if current_value in separators:
            if current_sentence:  # If current sentence is not empty
                sentences.append(np.array(current_sentence))
            current_sentence = [current_value]  # Start a new sentence with the separator
        else:
            current_sentence.append(current_value)
    
    # Add the last sentence if it's not empty
    if current_sentence:
        sentences.append(np.array(current_sentence))  
    return sentences

# Finds the longest sentences in a text 
def find_longest_sentences(text, separators):
    sentences = split_text_by_sentences(text, separators)
    longest_sentence_length = max([len(sentence) for sentence in sentences])
    longest_sentences = [sentence for sentence in sentences if len(sentence) == longest_sentence_length]   
    return longest_sentences

# Finds the shortest sentences in a text
def find_shortest_sentences(text, separators):  
    sentences = split_text_by_sentences(text, separators)
    
    # Filter out sentences with only a sentence separator 
    valid_sentences = [sentence for sentence in sentences if len(sentence) > 1] 
    if not valid_sentences:
        return []  # No valid sentences found
    
    shortest_sentence_length = min([len(sentence) for sentence in valid_sentences])
    shortest_sentences = [sentence for sentence in valid_sentences if len(sentence) == shortest_sentence_length]   
    return shortest_sentences

# find the average number of words in a sentence for input text
def calculate_average_sentence_length(text_array, separator_array):
    sentences = split_text_by_sentences(text_array, separator_array)
    sentence_lengths = [len(sentence) for sentence in sentences]
    
    if not sentence_lengths:
        return 0  # Handle the case of no sentences
    
    average_length = sum(sentence_lengths) / len(sentence_lengths)
    return average_length

# find all sentences that begins with a given word
def find_sentences_starting_with(text_array, separator_array, first_word_in_sentence):    
    sentences = split_text_by_sentences(text_array, separator_array)
    result_sentences = [sentence for sentence in sentences if sentence[0] == first_word_in_sentence]  
    return result_sentences


# find the longest word (or words) in an inuput text
def find_longest_words(text, language_id, db_config):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Get language name from languages table
        get_language_query = "SELECT Language FROM languages WHERE id = %s"
        cursor.execute(get_language_query, (language_id,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Language with ID {language_id} not found.")
        language_name = result[0].lower() 

        # Create dictionary table name
        dictionary_table_name = f"{language_name}dictionary"

        # Find longest word character length
        longest_length = 0
        for word_id in text:
            get_word_length_query = f"SELECT WordCharacterLength FROM {dictionary_table_name} WHERE Id = %s"
            cursor.execute(get_word_length_query, (word_id,))
            result = cursor.fetchone()
            if result:
                word_length = result[0]
                longest_length = max(longest_length, word_length)

        # Find IDs of words with longest length
        longest_words_in_text = []
        for word_id in text:
            get_word_length_query = f"SELECT WordCharacterLength FROM {dictionary_table_name} WHERE Id = %s"
            cursor.execute(get_word_length_query, (word_id,))
            result = cursor.fetchone()
            if result and result[0] == longest_length:
                longest_words_in_text.append(word_id)

        return np.array(longest_words_in_text)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if cnx:
            cnx.close()
'''
            
'''
# init db check
        if connection.is_connected():
            print("Connection to MySQL DB successful")
        else:
            print("Connection failed")
'''