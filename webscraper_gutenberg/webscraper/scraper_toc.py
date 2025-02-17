import time
import requests
from bs4 import BeautifulSoup
import mysql.connector
import random
from fake_useragent import UserAgent
import re

# takes a name "SecondName, FirstName, Title" and straightens it out to "Title FirstName SecondName"
def name_rearranger(name):
    separated_name = name.split(",")
    # the name has only a first & surname
    if len(separated_name) == 2:                                     
        rearranged_name = separated_name[1]+" "+separated_name[0]
        rearranged_name.replace("  ", " ")  # remove double spaces 
        return rearranged_name
    # the name has a title, first and surname        
    elif len(separated_name) > 2:                                    
        title = separated_name[-1]
        separated_name.pop()
        separated_name = separated_name[::-1] # reverse order of first & second name (hopefully it will still make sense if the name had even more components)
        rearranged_name = title +' '.join(separated_name)
        return rearranged_name
    # name is singular
    else:                                                           
        return name

# Scrapes book information from a given URL and returns a dictionary of book details.
def scrape_book_info(url):
    referer_sites = ['https://www.google.com','https://www.bing.com','https://www.yahoo.com']
    referer = random.choice(referer_sites)  # Set random referer on each request
    user_agent = UserAgent()
    
    # A header to make the requests look more human
    header = {
    'User-Agent': user_agent.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': referer,
    'Connection': 'keep-alive'}
    
    
    try:
        print(f"Trying to fetch page: {url}")
        result = requests.get(url, headers=header, timeout=5)
        result.raise_for_status()  # Raise an exception for unsuccessful requests
        
        # Pause for a bit between requests (in an attempt to not bother gutenberg/internet archive too much)
        time.sleep(2)
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the website: {e}")
        return {}

    doc = BeautifulSoup(result.text, "html.parser")
    books = doc.find_all("h2") #class_="pgdbbytitle"
    book_data = []

    for i in range(len(books)):
        next_sibling = books[i].find_next_sibling()
        if next_sibling and next_sibling.name == "p":
            #author_paragraphs.append(next_sibling)
            books[i].append(next_sibling)
    
    
    for book in books:
        if not any(child.has_attr('title') and 'Audio Book' in child['title'] for child in book.find_all(recursive=True)): # filter out audiobooks 
            link_source = book.find("a")   # Find the first anchor tag within the <h2> tag
        
            # Check if the link element exists
            if link_source:
                link_number = link_source["href"].split("/")[-1]  # Get last part of the link
                link = f"https://www.gutenberg.org/cache/epub/{link_number}/pg{link_number}.txt"
               
                title_parts = book.text.strip().split("(")  # Extract title considering possible extra anchor tags within it
                title = title_parts[0].strip()              # Get text before parenthesis
                title = title.split("\n")[0]                # remove subtitles
                title = title.replace("$b", "")             # remove common addons that shouldn't be in the title
                if len(title) >= 64:
                    title = title[:64]                      # truncate too long titles
                          
                # get the language, which is found in the first parethesis of the <h2>
                if "(" in book.text and ")" in book.text:
                    if ")by" in book.text:
                        parts = book.text.strip().split(")by", 1)   # Split the text at the first occurrence of ")by"
                    elif ") by" in book.text:
                        parts = book.text.strip().split(") by", 1)   # Split the text at the first occurrence of ") by"
                    else:
                        parts = book.text.strip().split(")", 1)
                    language = parts[0].strip().split("(")[-1]  # Extract the part after the "(" 
                    language = language.split(")", 1)[0]        # in cases where ") by" occured instead of ")by", the text needs to be pruned 
                    language = language.split(" ", 1)[0]        # in cases a stray word enters the phrase (all languages should be one word only)
                    language = re.sub(r"[\W_]", "", language)   # remove non-alphanumeric characters
                    if language.isspace() or language =="":     # set empty value to "unknown"
                        language = "unknown"
                else:
                    language = "unknown" # Handle cases where no "(" or ")" are found in the text
          
                # Find the <p> tag containing the author information below the <h2> 
                author_info = book.find("p") 
    
                if author_info:
                    author = author_info.text.strip()
                    author = author.replace("by ", "")
                    author = name_rearranger(author) # Change the name arrangement of the author (from "surname, first name, title" to "title firstname surname")
                else:
                    author = "Unknown"  # Handle cases where author information is missing                
                
                book_dict = {
                    'SourceWebsite': link,
                    'StoredAndProcessed': 0,
                    'Title': title,
                    'Language': language,
                    'Author': author,
                    'WordCount': 0,
                    'CharacterCount': 0,
                }
                book_data.append(book_dict)
    return book_data

# Adds punctuations etc. to input dictionary table - Not very important, but for the sake of having the most used entries at the beginning of the table rows
def _add_punctuation_to_table(cursor, table_name):    
    punctuation_marks = ['.', ',', '_', '!', '?', ';', ':', '-', '—', '(', ')', '[', ']', '{', '}', '"', '\n']
    for mark in punctuation_marks:
        sql = f"INSERT INTO {table_name} (Word, WordCharacterLength) VALUES (%s, %s)" 
        val = (mark, 0)
        cursor.execute(sql, val)
    cursor.execute(sql, val)

# Inserts book data into the 'Book' table in the MySQL database.
def insert_books_into_database(books, db_config):   
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        insert_query = """
        INSERT INTO Book (SourceWebsite, Title, Language, Author)
        VALUES (%s, %s, %s, %s)
        """
        
        for book in books:
            # Check if language exists in languages table
            get_language_id_query = "SELECT id FROM languages WHERE Language = %s"
            cursor.execute(get_language_id_query, (book['Language'],))
            language_id = cursor.fetchone() 
            if language_id is not None:
                language_id = language_id[0]
            
            dictionary_table_name = f"{book['Language'].lower()}dictionary" # Determine dictionary table name based on language
                             
            # Check if author exists in authors table
            get_author_id_query = "SELECT id FROM author WHERE Name = %s"
            cursor.execute(get_author_id_query, (book['Author'],))
            author_id = cursor.fetchone() 
            if author_id is not None:
                author_id = author_id[0]        
                
                # Create Dictionary table if it does not exist. NOTE: why didn't i put this inside "if not language_id"? Any reason not to? figure out later
                create_dictionary_table = f"""
                        CREATE TABLE IF NOT EXISTS {dictionary_table_name} (
                        Id INT AUTO_INCREMENT PRIMARY KEY,
                        Word TINYTEXT,
                        WordCharacterLength INT,
                        WordType INT )"""
                cursor.execute(create_dictionary_table)
            
            # Check if the book's language exist in the database. if not, add it.
            if not language_id:
                insert_language_query = "INSERT INTO languages (Language) VALUES (%s)"
                cursor.execute(insert_language_query, (book['Language'],))
                cnx.commit()
                language_id = (cursor.lastrowid,)
                if language_id is not None:
                    language_id = language_id[0]                
                _add_punctuation_to_table(cursor, dictionary_table_name) # add punctuations etc. as the first entries to the new language table dictionary
                
            # Check if the book's author exist in the database. if not, add them.
            if not author_id:
                insert_author_query = "INSERT INTO author (Name) VALUES (%s)"
                cursor.execute(insert_author_query, (book['Author'],))
                cnx.commit()
                author_id = (cursor.lastrowid,)
                if author_id is not None:
                    author_id = author_id[0]                
            
            values = (book['SourceWebsite'], book['Title'], language_id, author_id)
            cursor.execute(insert_query, values) # add book if it's not already stored.
            
        cnx.commit()
        print(f"Successfully inserted {len(books)} books into the database.")

    except mysql.connector.Error as err:
        print(f"Error inserting books into the database: {err}")
    finally:
        if cnx:
            cnx.close()

