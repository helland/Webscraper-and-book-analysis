import os, sys
import requests 
from datetime import datetime, timedelta
import numpy as np
import webscraper.init_database as init
import time
import webscraper.setup_scraper as setup
import webscraper.scraper as scraper
import webscraper.utility_functions as utils
import webscraper.book as book
import webscraper.analysis_functions as analysis

# A simple command line text interface meant for testing and debugging the gutenberg webscrapers, the database, utility and analysis functions.
if __name__ == "__main__":    

    # database connection details
    db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pass',
    'database': 'book_project',
    'use_pure': 'True'
    }
   
    info = {
        "init": "Initialize database",
        "setup": "set up the table of content to show which books are possible to add and get the relevant links needed to add them",
        "exit123": "end program",
        
        }
    input_data = ' '
       
    # Receive input_data and process as long as it's not 'exit123'
    while input_data != 'exit123':
        print('\n----------------\nWhat is the name of the book you want to add to the database? type "info123" to see which commands will do something else.') 
        input_data = input("Command: ")
        
        # Initialize database
        if input_data=='info123':
            print("Commands (anything else will attempt to add a book to the database by that name):")
            for item, description in info.items():  
                print("{} ({})".format(item, description))
                
        # Initialize database
        elif input_data=='init123':
            init.create_database(db_config)
            init.create_tables(db_config)
            
        # set up the table of content by scraping the sites listing all books sorted by first letter (going through web archive to prevent us from bothering Gutenberg too much)
        elif input_data == 'setup123':
            
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
                scraped_books = setup.scrape_book_info(url)
                all_books.extend(scraped_books)
                
                # Pause for a bit between requests (in an attempt to not bother gutenberg/internet archive too much)
                time.sleep(5) 
                  
            # Insert books into the database
            setup.insert_books_into_database(all_books, db_config)
                                 
        #  
        elif input_data == '   ':
            print("future command to be added")
            
        # Run data analysis if the command is left blank
        elif input_data == '':
            input_data = input("Simple data analysis mode engaged. \nWhat is the title of the book you want to analyse? ")
            does_book_exist = utils.get_books_with_title(input_data, db_config)    # see if a book by given title exist in the table of content
            
            if does_book_exist[0]['StoredAndProcessed'] == True:                       #for simplicity's sake, only look at the first book found.
                book = book.Book(int(does_book_exist[0]['Id']), db_config)
                filename = f"{book.book_id}.png"
                exclude_values = utils.get_non_alphanumerics(f"{book.language_name}dictionary", db_config)
                punctuations = [1,4, 5, 6, 7] # corresponds to [".","!","?",":",";","\n"] # sentence punctuations
                
                # REWRITE ASAP - this is just some quick and ugly analysis code, done to confirm that everything works
                most_frequent_word = analysis.find_most_frequent_word(book.text, exclude_values)
                most_frequent_words = analysis.find_top_n_most_frequent(book.text, 20, exclude_values)
                words_used_only_once = analysis.find_unique_words(book.text, exclude_values)
                sentences = analysis.split_text_by_sentences(book.text, punctuations)
                longest_sentence = analysis.find_longest_sentences(book.text, punctuations)
                shortest_sentence = analysis.find_shortest_sentences(book.text, punctuations)
                sentence_length = analysis.calculate_average_sentence_length(book.text, punctuations)
                sentences_starting_with = analysis.find_sentences_starting_with(book.text, punctuations, 48200) # the word "Dusk"
                longest_word = analysis.find_longest_words(book.text, book.language, db_config)
               
                
                most_frequent_word = analysis.cipher_decoder([most_frequent_word], book.language, db_config)
                most_frequent_words = analysis.cipher_decoder(most_frequent_words, book.language, db_config)
                words_used_only_once = analysis.cipher_decoder(words_used_only_once, book.language, db_config)
                sentences = analysis.cipher_decoder(sentences, book.language, db_config)
                longest_sentence = analysis.cipher_decoder(longest_sentence, book.language, db_config)
                shortest_sentence = analysis.cipher_decoder(shortest_sentence, book.language, db_config)
                sentences_starting_with = analysis.cipher_decoder(sentences_starting_with, book.language, db_config)
                longest_word = analysis.cipher_decoder(longest_word, book.language, db_config)
                
                print(f"most frequent word:  {most_frequent_word}")
                print(f"most frequent words:  {most_frequent_words}")
                print(f"words used only once ({len(words_used_only_once)} words):  {words_used_only_once[:10]} etc.")
                print(f"sentence 1-10:  {sentences[:10]}")
                print(f"longest sentence 1-10:  {longest_sentence}")
                print(f"shortest sentence 1-10:  {shortest_sentence[:10]}")
                print(f"sentence length:  {sentence_length}")
                print(f"sentences starting with the word 'Dusk':  {len(sentences_starting_with)}")
                print(f"longest word 1:  {longest_word}")
                
                book_text = analysis.cipher_decoder(book.text, book.language, db_config)
                delimiter = " "
                book_text = delimiter.join(book_text)
                analysis.generate_wordcloud(book_text, filename)
                print("word cloud generated")
            else:
                print("Book not found in database.")
                   
        else:
            print(f'Attempting to encode and upload the book {input_data} to the database')
            input_books = utils.get_books_with_title(input_data, db_config)
            
            book = {
                'title'         : '', 
                'text'          : '', 
                'author'        : '', 
                'release_date'  : '', 
                'language'      : '', 
                'word_count'    : '', 
                'character_count':'', 
                'source_website': '' 
                }
            
                       
            # 1 book found by input title. Ask user if they want to store it
            if len(input_books) == 1:
                # Prevent duplicates to be stored in the database
                if input_books[0]['StoredAndProcessed'] == True:
                    print(f"The book '{input_books[0]['Title']}' has already been stored in the database.")
                    break
                else:
                    #book_by_input_title = utils.get_books_with_title(input_data, db_config)
                    print(f"The book {input_books[0]['Title']} by {input_books[0]['Author']} ({input_books[0]['Language']}) was found. Scraping, encoding and storing it in the database.")
                    
                    # Scrape info and store in book dictionary
                    book['title'], book['author'], book['release_date'], book['language'], book['text'], book['word_count'], book['character_count'] = scraper.gutenberg_book_scraper(input_books[0]['SourceWebsite'])
                    book['source_website'] = input_books[0]['SourceWebsite']
                    
                    # Store book in the database
                    scraper.store_books_in_database((book,), db_config)
                           
            # multiple books found with input title. List them for the user.
            elif len(input_books) > 1:
                print(f"multiple books by the title {input_data} was found. Choose which you were looking for.")
                for i, entry in enumerate(input_books):
                    print(f"{i}: {entry['Title']} by {entry['Author']} ({entry['Language']}) at {entry['SourceWebsite']}")
                
                # The user must choose which one should be scraped.   
                input_index = int(input("Which book did you want to scrape? \nNumber: "))
                if input_index >= 0 and input_index <= len(input_books)-1:
                # Prevent duplicates to be stored in the database
                    if input_books[input_index]['StoredAndProcessed'] == True:
                        print(f"The book '{input_books[0]['Title']}' has already been stored in the database.")
                        break  
                    
                    # Scrape info and store in book dictionary                  
                    book['title'], book['author'], book['release_date'], book['language'], book['text'], book['word_count'], book['character_count'] = scraper.gutenberg_book_scraper(input_books[input_index]['SourceWebsite'])
                    book['source_website'] = input_books[input_index]['SourceWebsite']
                    
                    # Store book in the database
                    scraper.store_books_in_database((book,), db_config)
                else: 
                    print("Invalid index.")
                    break
            else:
                print(f"No books by the title {input_data} was found.")
                
            

            
            
            
            
            
            
            
  