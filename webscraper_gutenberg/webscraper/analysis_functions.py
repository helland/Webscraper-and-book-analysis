import mysql.connector
import numpy as np 
from wordcloud import WordCloud, STOPWORDS
import re
from functools import lru_cache
from collections import Counter
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# find the word used most often in a text (converted to integer). excluding things like .,!?-_</
def find_most_frequent_word(text, exclude_values):
 
    mask = ~np.isin(text, exclude_values)
    filtered_arr = text[mask]

    if len(filtered_arr) == 0:
        return None

    unique, counts = np.unique(filtered_arr, return_counts=True)
    most_frequent_index = np.argmax(counts)
    return int(unique[most_frequent_index]) 

# Finds the n most frequent words in the text 
def find_top_n_most_frequent(text, number_of_words, exclude_values):
    top_n_values = []
    
    if number_of_words is None or number_of_words == 0:
        number_of_words = 1 # return only 1 value if the "number of words" parameter is handled incorrectly.     
    
    for _ in range(number_of_words):
        most_frequent = find_most_frequent_word(text, exclude_values)
        if most_frequent is None:
            break
        top_n_values.append(most_frequent)
        exclude_values = np.append(exclude_values, most_frequent)  

    return top_n_values 


# find words that only occur once in a text (converted to integers)
def find_unique_words(text, exclude_values):
    mask = ~np.isin(text, exclude_values)
    filtered_arr = text[mask]

    unique, counts = np.unique(filtered_arr, return_counts=True)
    unique_indices = np.where(counts == 1)[0]
    unique_values = unique[unique_indices]
    return unique_values.tolist()

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

    for word in text:   
        if word in separators:                          # if the current word is a sentence breaker
            if current_sentence:
                current_sentence.append(int(word))      # add the separator to end the sentence
                sentences.append(current_sentence)      # add sentence to list of sentences 
            current_sentence = []                       # reset sentence
        else:
            current_sentence.append(int(word))          # otherwise, add the word to the sentence

    if current_sentence:
        sentences.append(current_sentence)
    return sentences

# Finds the longest sentences in a text 
def find_longest_sentences(text, separators):
    sentences = split_text_by_sentences(text, separators)
    if not sentences:  # Handle empty sentences 
        return []
    longest_sentence_length = max(len(sentence) for sentence in sentences)
    longest_sentences = [sentence for sentence in sentences if len(sentence) == longest_sentence_length]
    return longest_sentences   

# Finds the shortest sentences in a text
def find_shortest_sentences(text, separators):  
    sentences = split_text_by_sentences(text, separators)

    valid_sentences = [sentence for sentence in sentences if len(sentence) > 1]
    if not valid_sentences:
        return []

    shortest_sentence_length = min(len(sentence) for sentence in valid_sentences)
    shortest_sentences = [sentence for sentence in valid_sentences if len(sentence) == shortest_sentence_length]
    return shortest_sentences

# find the average number of words in a sentence for input text
def calculate_average_sentence_length(text_array, separator_array):
    sentences = split_text_by_sentences(text_array, separator_array)
    sentence_lengths = [len(sentence) for sentence in sentences]

    if not sentence_lengths:
        return 0

    return sum(sentence_lengths) / len(sentence_lengths)

# find all sentences that begins with a given word
def find_sentences_starting_with(text_array, separator_array, first_word_in_sentence):
    if first_word_in_sentence is None:
        return 0   # return 0 if the "first word" parameter is handled incorrectly.
    sentences = split_text_by_sentences(text_array, separator_array)
    result_sentences = [sentence for sentence in sentences if sentence and sentence[0] == first_word_in_sentence]  # Check if sentence is not empty
    return result_sentences



@lru_cache(maxsize=350000)   
def _get_all_word_lengths_from_dict(cursor, dictionary_table_name):
    get_word_lengths_query = f"SELECT Id, WordCharacterLength FROM {dictionary_table_name}"
    cursor.execute(get_word_lengths_query)
    word_lengths_dict = dict(cursor.fetchall())
    return word_lengths_dict

def find_longest_words(text, language_id, db_config):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        get_language_query = "SELECT Name FROM languages WHERE id = %s"
        cursor.execute(get_language_query, (language_id,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Language with ID {language_id} not found.")
        language_name = result[0].lower()

        dictionary_table_name = f"{language_name.lower()}dictionary"

        word_lengths = _get_all_word_lengths_from_dict(cursor, dictionary_table_name)

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

        return list(dict.fromkeys(longest_words_in_text)) # remove duplicates

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if cnx:
            cnx.close()       
       

# Returns a list of all words that are the same in all input books at the same placement (eg. word number 10034 = "this" in all books would add 10034 to the return array).
def word_placement_equivalence(books):
    if not books:
        return np.array([], dtype=int)  # Handle empty input
    
    start_time = time.time()
    
    min_len = min(len(book.text) for book in books)  # Find the shortest book length

    equivalent_indices = []
    for i in range(min_len):  # Iterate up to the shortest length
        word = books[0].text[i]  # Get the word from the first book
        if all(book.text[i] == word for book in books[1:]):  # Check other books
            equivalent_indices.append(i)
    
    print(f"idex comparison took: {round(time.time() - start_time, 2)} seconds")
    
    return equivalent_indices #np.array(, dtype=int)   

# cout occurrence of words in list of books
def count_word_occurrences(book):   
    counts = defaultdict(int)
    for word in book.text:
        counts[word] += 1
    return dict(counts)

# Calculates the deviation of word counts for a single book from the total counts of all books used.
def calculate_deviation(book_counts, total_counts, book_length, total_length):
    deviation = 0
    all_words = set(book_counts.keys()).union(total_counts.keys())

    for word in all_words:
        book_count = book_counts.get(word, 0)
        total_count = total_counts.get(word, 0)

        # Calculate relative frequencies:
        book_freq = book_count / book_length if book_length > 0 else 0
        total_freq = total_count / total_length if total_length > 0 else 0

        deviation += abs(book_freq - total_freq)  # Deviation is the absolute difference in frequencies

    return deviation

# Finds the book with the highest deviation in word counts.
def find_book_with_highest_deviation(books):
    total_counts = defaultdict(int)
    total_length = 0

    book_counts_list = []  # Store individual book counts

    for book in books:
        book_counts = count_word_occurrences(book)  # Calculate for each book individually
        book_counts_list.append(book_counts)
        book_length = len(book.text)
        total_length += book_length

        for word, count in book_counts.items(): # Add to the total count
            total_counts[word] += count

    total_counts = dict(total_counts)  # Convert to regular dict

    highest_deviation = -1
    book_with_highest_deviation = None

    for i, book in enumerate(books):        # Iterate through books
        book_counts = book_counts_list[i]   # Retrieve pre-calculated counts
        book_length = len(book.text)
        deviation = calculate_deviation(book_counts, total_counts, book_length, total_length)

        if deviation > highest_deviation:
            highest_deviation = deviation
            book_with_highest_deviation = book

    return book_with_highest_deviation, highest_deviation

# fetch all words and IDs from relevant dictionary in the database
@lru_cache(maxsize=350000)
def _get_all_words_from_dict(cursor, dictionary_table_name):
    get_words_query = f"SELECT Id, Word FROM {dictionary_table_name}"  # Select both Id and Word
    cursor.execute(get_words_query)
    complete_dictionary = dict(cursor.fetchall()) # Convert to dictionary for fast lookup
    return complete_dictionary

# Decodes an array (or array of arrays) of integers (word IDs) into a list of words by taking the whole dictionary from the database and comparing IDs  
def cipher_decoder(encoded_text, language_id, db_config):
    max_threads = 1 # Increase threads to potentially speed up the function. My poor, ancient laptop prefers only 1.
    
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        # Find the right language dictionary table in the database where the IDs in encoded_text correspond to a string word. 
        get_language_query = "SELECT Name FROM languages WHERE id = %s"
        cursor.execute(get_language_query, (language_id,))
        language_name = cursor.fetchone()[0].lower()
        dictionary_table_name = f"{language_name.lower()}dictionary"

        word_dict = _get_all_words_from_dict(cursor, dictionary_table_name)
        
        # Helper function to decode a single item (int or list)
        def decode_item(item):
            if isinstance(item, list):
                return [word_dict.get(int(inner_item), f"[ID {inner_item} not found]") for inner_item in item]
            else:
                return word_dict.get(int(item), f"[ID {item} not found]")

        # Convert encoded text to a list if it's a NumPy array
        if isinstance(encoded_text, np.ndarray):
            if encoded_text.ndim == 1 or encoded_text.ndim == 2:
                encoded_text = encoded_text.tolist()
            else:
                raise ValueError("Numpy array must be 1D or 2D")

        if not isinstance(encoded_text, list):
            raise TypeError("encoded_text must be a list or a list of lists")

        decoded_words = []
        with ThreadPoolExecutor(max_workers=max_threads) as executor:  # Correct placement of max_workers
            futures = [executor.submit(decode_item, item) for item in encoded_text]

            for future in as_completed(futures):
                decoded_words.append(future.result())
                
        return decoded_words

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        if cnx:
            cnx.close()
