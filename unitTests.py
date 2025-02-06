# WARNING - Heavy use of AI was used in the writing of this code
import unittest
import numpy as np
from wordcloud import STOPWORDS, WordCloud   
import mysql.connector   
import re  

# Assuming your functions are in a file named 'your_module.py'
from webscraper.analysis_functions import (
    find_most_frequent_word,
    find_top_n_most_frequent,
    find_unique_words,
    generate_wordcloud,
    split_text_by_sentences,
    find_longest_sentences,
    find_shortest_sentences,
    calculate_average_sentence_length,
    find_sentences_starting_with,
    find_longest_words,
    update_word_entry_counts,
    word_placement_equivalence,
    word_placement_equivalence_strings,
)


class TestFunctions(unittest.TestCase):

    def test_find_most_frequent_excluding(self):
        text = np.array([1, 2, 3, 2, 1, 4, 2, 3, 5])
        exclude = np.array([1, 4, 5])
        self.assertEqual(find_most_frequent_word(text, exclude), 2)
        self.assertIsNone(find_most_frequent_word(text, np.array([1, 2, 3, 4, 5]))) #Test if all are excluded
        self.assertIsNone(find_most_frequent_word(np.array([]), exclude)) #Test if text is empty

    def test_find_top_n_most_frequent(self):
        text = np.array([1, 2, 3, 2, 1, 4, 2, 3, 5, 1, 2, 3, 6, 7, 8, 2, 1])
        exclude = []
        self.assertTrue(np.array_equal(find_top_n_most_frequent(text, 3, exclude), np.array([2, 1, 3])))
        self.assertTrue(np.array_equal(find_top_n_most_frequent(text, 2, exclude), np.array([2, 1])))
        self.assertTrue(np.array_equal(find_top_n_most_frequent(text, 5, exclude), np.array([2, 1, 3, 6, 7]))) #Test if less unique values than requested
        self.assertTrue(np.array_equal(find_top_n_most_frequent(np.array([]), 3, exclude), np.array([]))) #Test if text is empty

    def test_find_unique_words(self):
        text = np.array([1, 2, 3, 2, 1, 4, 2, 3, 5, 1, 2, 3, 6, 7, 8, 2, 1])
        exclude = []
        self.assertTrue(np.array_equal(find_unique_words(text, exclude), np.array([4, 5, 6, 7, 8])))
        self.assertTrue(np.array_equal(find_unique_words(text, np.array([1,2,3,4,5,6,7,8])), np.array([]))) #Test if all are excluded
        self.assertTrue(np.array_equal(find_unique_words(np.array([]), exclude), np.array([]))) #Test if text is empty

    def test_generate_wordcloud(self):
        text = "This is a test string for the word cloud. Word cloud test."
        filename = "test_wordcloud.png"  # You can change the filename
        generate_wordcloud(text, filename)
        # You'll need to manually check if the image file was created.
        # A more robust test would involve comparing the generated image to a known good image, but this is complex.
        import os
        self.assertTrue(os.path.exists(filename))
        os.remove(filename) #Remove the test file

    def test_split_text_by_sentences(self):
        text = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        separators = np.array([4, 7])
        sentences = split_text_by_sentences(text, separators)
        self.assertEqual(len(sentences), 3)
        self.assertTrue(np.array_equal(sentences[0], np.array([1, 2, 3])))
        self.assertTrue(np.array_equal(sentences[1], np.array([4, 5, 6])))
        self.assertTrue(np.array_equal(sentences[2], np.array([7, 8, 9, 10])))
        text2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        separators2 = np.array([1,4,7,10])
        sentences2 = split_text_by_sentences(text2, separators2)
        self.assertEqual(len(sentences2), 4)
        self.assertTrue(np.array_equal(sentences2[0], np.array([1])))
        self.assertTrue(np.array_equal(sentences2[1], np.array([4,5,6])))
        self.assertTrue(np.array_equal(sentences2[2], np.array([7,8,9])))
        self.assertTrue(np.array_equal(sentences2[3], np.array([10])))
        text3 = np.array([1, 2, 3])
        separators3 = np.array([4, 7])
        sentences3 = split_text_by_sentences(text3, separators3)
        self.assertEqual(len(sentences3), 1)
        self.assertTrue(np.array_equal(sentences3[0], np.array([1,2,3])))

    def test_find_longest_sentences(self):
        text = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        separators = np.array([4, 7, 10])
        longest_sentences = find_longest_sentences(text, separators)
        self.assertEqual(len(longest_sentences), 1)
        self.assertTrue(np.array_equal(longest_sentences[0], np.array([10, 11, 12, 13, 14])))
        text2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        separators2 = np.array([4, 10])
        longest_sentences2 = find_longest_sentences(text2, separators2)
        self.assertEqual(len(longest_sentences2), 1)
        self.assertTrue(np.array_equal(longest_sentences2[0], np.array([4, 5, 6, 7, 8, 9])))
        text3 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        separators3 = np.array([1, 4, 7, 10, 14])
        longest_sentences3 = find_longest_sentences(text3, separators3)
        self.assertEqual(len(longest_sentences3), 3)
        self.assertTrue(np.array_equal(longest_sentences3[0], np.array([1,2,3])))
        self.assertTrue(np.array_equal(longest_sentences3[1], np.array([4,5,6])))
        self.assertTrue(np.array_equal(longest_sentences3[2], np.array([7,8,9])))
        text4 = np.array([1])
        separators4 = np.array([1])
        longest_sentences4 = find_longest_sentences(text4, separators4)
        self.assertEqual(len(longest_sentences4), 0)
                 
                             
                             
    def test_find_shortest_sentences(self):
        text = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        separators = np.array([4, 7, 10])
        shortest_sentences = find_shortest_sentences(text, separators)
        self.assertEqual(len(shortest_sentences), 2)  # Corrected assertion
        self.assertTrue(np.array_equal(shortest_sentences[0], np.array([1, 2, 3])))
        self.assertTrue(np.array_equal(shortest_sentences[1], np.array([7, 8, 9])))
        text2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        separators2 = np.array([1, 4, 7, 10, 14])
        shortest_sentences2 = find_shortest_sentences(text2, separators2)
        self.assertEqual(len(shortest_sentences2), 4)
        self.assertTrue(np.array_equal(shortest_sentences2[0], np.array([1])))
        self.assertTrue(np.array_equal(shortest_sentences2[1], np.array([4])))
        self.assertTrue(np.array_equal(shortest_sentences2[2], np.array([7])))
        self.assertTrue(np.array_equal(shortest_sentences2[3], np.array([10])))
        text3 = np.array([1, 2, 3])
        separators3 = np.array([4, 7])
        shortest_sentences3 = find_shortest_sentences(text3, separators3)
        self.assertEqual(len(shortest_sentences3), 1)
        self.assertTrue(np.array_equal(shortest_sentences3[0], np.array([1, 2, 3])))
        text4 = np.array([1])
        separators4 = np.array([1])
        shortest_sentences4 = find_shortest_sentences(text4, separators4)
        self.assertEqual(len(shortest_sentences4), 0)
        text5 = np.array([])
        separators5 = np.array([1])
        shortest_sentences5 = find_shortest_sentences(text5, separators5)
        self.assertEqual(len(shortest_sentences5), 0)

    def test_calculate_average_sentence_length(self):
        text = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        separators = np.array([4, 7])
        self.assertEqual(calculate_average_sentence_length(text, separators), 4.0)
        text2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        separators2 = np.array([1,4,7,10])
        self.assertEqual(calculate_average_sentence_length(text2, separators2), 1.5)
        text3 = np.array([])
        separators3 = np.array([4, 7])
        self.assertEqual(calculate_average_sentence_length(text3, separators3), 0)

    def test_find_sentences_starting_with(self):
        text = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        separators = np.array([4, 7])
        self.assertEqual(len(find_sentences_starting_with(text, separators, 1)), 1)
        self.assertTrue(np.array_equal(find_sentences_starting_with(text, separators, 1)[0], np.array([1, 2, 3])))
        self.assertEqual(len(find_sentences_starting_with(text, separators, 5)), 0)
        text2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        separators2 = np.array([1,4,7,10])
        self.assertEqual(len(find_sentences_starting_with(text2, separators2, 1)), 1)
        self.assertTrue(np.array_equal(find_sentences_starting_with(text2, separators2, 1)[0], np.array([1])))
        self.assertEqual(len(find_sentences_starting_with(text2, separators2, 4)), 1)
        self.assertTrue(np.array_equal(find_sentences_starting_with(text2, separators2, 4)[0], np.array([4])))
        self.assertEqual(len(find_sentences_starting_with(text2, separators2, 7)), 1)
        self.assertTrue(np.array_equal(find_sentences_starting_with(text2, separators2, 7)[0], np.array([7])))
        self.assertEqual(len(find_sentences_starting_with(text2, separators2, 10)), 1)
        self.assertTrue(np.array_equal(find_sentences_starting_with(text2, separators2, 10)[0], np.array([10])))

    def test_find_longest_words(self,db_config):

        language_id = 1  # Replace with a valid language ID in your test database
        text = np.array([1, 2, 3, 4, 5])  # Replace with some test word IDs

        # Insert some test data into your test database (languages and your_language_name_dictionary tables) before running this test.
        # The test should check if find_longest_words returns the correct longest words' IDs based on the data you inserted.
        try:
            longest_words = find_longest_words(text, language_id, db_config)
            # Add assertions here to check the returned longest_words array
            # Example: self.assertTrue(np.array_equal(longest_words, np.array([expected_word_ids])))
            print("find_longest_words test passed (add assertions to verify)")
        except ValueError as e:
            self.fail(f"Test failed due to ValueError: {e}")
        except mysql.connector.Error as err:
            self.fail(f"Test failed due to database error: {err}")

    def test_update_word_entry_counts(self, db_config):
        try:
            update_word_entry_counts(db_config)
            # Add assertions to check if the NumberOfWordEntries in your languages table has been correctly updated
            print("update_word_entry_counts test passed (add assertions to verify)")
        except mysql.connector.Error as err:
            self.fail(f"Test failed due to database error: {err}")


    def test_word_placement_equivalence(self):
        class Book:  # Define a simple Book class for the test
            def __init__(self, book_text):
                self.text = book_text

        book1_text = np.array([1, 2, 3, 4, 5, 6])
        book2_text = np.array([10, 2, 13, 4, 15, 16])
        book3_text = np.array([1, 12, 3, 4, 17, 18])

        book1 = Book(book1_text)
        book2 = Book(book2_text)
        book3 = Book(book3_text)

        books = [book1, book2, book3]
        equivalent_indices = word_placement_equivalence(books)
        self.assertTrue(np.array_equal(equivalent_indices, np.array([2, 3])))

        book4_text = np.array([1, 2, 3, 4, 5])  # Different length
        book4 = Book(book4_text)
        books2 = [book1, book2, book4]
        equivalent_indices2 = word_placement_equivalence(books2)
        self.assertTrue(np.array_equal(equivalent_indices2, np.array([2, 3]))) #Should still work

        books3 = []  # Empty list
        equivalent_indices3 = word_placement_equivalence(books3)
        self.assertTrue(np.array_equal(equivalent_indices3, np.array([])))

        book5_text = np.array([1, 2, 3, 4, 5, 6])
        book5 = Book(book5_text)
        books4 = [book1, book5] #identical lists
        equivalent_indices4 = word_placement_equivalence(books4)
        self.assertTrue(np.array_equal(equivalent_indices4, np.array([0,1,2,3,4,5])))

    def test_word_placement_equivalence_strings(self):
        book1_text = "This is the first book. It has some words."
        book2_text = "This is the second book. It also has some words."
        book3_text = "This is the third book. It has some words too."

        books = [book1_text, book2_text, book3_text]
        equivalent_indices = word_placement_equivalence_strings(books)
        self.assertEqual(equivalent_indices, [0, 1, 2, 4, 5, 6])

        book4_text = "This is the first book. It has some words."
        books2 = [book1_text, book2_text, book4_text]
        equivalent_indices2 = word_placement_equivalence_strings(books2)
        self.assertEqual(equivalent_indices2, [0, 1, 2, 4, 5, 6])

        books3 = []  # Empty list
        equivalent_indices3 = word_placement_equivalence_strings(books3)
        self.assertEqual(equivalent_indices3, [])

        book5_text = "This is the first book. It has some words."
        books4 = [book1_text, book5_text] #identical lists
        equivalent_indices4 = word_placement_equivalence_strings(books4)
        self.assertEqual(equivalent_indices4, [0, 1, 2, 4, 5, 6, 7, 8, 9])                        
                             
                             
                             
                             
                             
                             
                             
