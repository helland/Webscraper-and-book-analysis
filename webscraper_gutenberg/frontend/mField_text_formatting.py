from webscraper.book import Book as book
import re

# formats the text output with one word per book
def books_word(books, words):
    output_string = "<table>"
    
    for i, book in enumerate(books):
        output_string += f"<tr><td><b>{words[i]} </b></td> <td> ({book.title}) </td></tr>"   
    output_string += "</table>"
    return output_string


# formats the text output with multiple words per book
def books_words(books, words):
    output_string = ""
        
    for i, book in enumerate(books):
        output_string += f"<b>{book.title}</b><br>"
        for j in range(len(words[i])):
            output_string += f"{words[i][j]}, "
        output_string = output_string[:-2]
        output_string += "<br><br>"
    
    return output_string

# formats the text output with one index next each word
def indices_words(indices, words):
    output_string = ""
    
    for index, word in enumerate(words):
        if index in indices:
            output_string += f"At {index}:  <b>{word}</b><br>" 
    if output_string == "":
        output_string = "<br><br><h2>No words have the same index in all the selected books.</h2>"  
    else:
        output_string = f"<h3>{len(indices)} words with the same index found:</h3><br>"+output_string
    return output_string

# formats the text output with a single sentence per book
def books_sentence(books, sentences):
    output_string = ""
        
    for i, book in enumerate(books):
        output_string += f"<b>{book.title}</b><br>"
        for j in range(len(sentences[i])):
            output_string += f"{sentences[i][j]}<br>"
        output_string = output_string[:-2]
        output_string += "<br><br>"
    
    return output_string

# formats the text output with multiple sentence per book, the number of sentences each book is allocated is equal to the number in sentences_per_book at the book's index
def books_sentences(books, sentences, sentences_per_book):
    output_string = ""
    sentence_count = 0
    
    for i, book in enumerate(books):
        output_string += f"<b>{book.title}</b><br>"

        num_sentences_to_print = sentences_per_book[i]  # Get the number of sentences for this book
        for j in range(sentence_count, sentence_count+num_sentences_to_print):  # Iterate through the sentences, up to the limit
            sentence = ' '.join(sentences[j])  # Join the words 
            sentence = re.sub(r"\s([.,:;!?])$", r"\1", sentence)  # Remove space before punctuation at end
            sentence = re.sub(r"\s,", ",", sentence)  # Remove space before commas
            output_string += f"{sentence}<br>"
        sentence_count +=num_sentences_to_print
        output_string += "<br>"
        
    return output_string
     
# Removes duplicate word based on case sensitivity #NOTE: no longer in use. remove?    
def remove_duplicates(word_list):
    unique_words = []
    seen_words = set()

    for word in word_list:
        if word not in seen_words:
            unique_words.append(word)
            seen_words.add(word)

    return unique_words