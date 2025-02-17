# Gutenberg Book Analyzer

This PyQt5-based GUI application provides tools for analyzing books from Project Gutenberg. It allows users to search for books, add them to a local database, and perform various text analysis tasks.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [License](#license) 


## Introduction

This project aims to simplify the process of working with Project Gutenberg texts.  It automates the scraping of book information, storage in a database, and provides basic analytical tools. The command-line interface makes it easy to interact with the system and perform various tasks.


## Features

* **Book Search**	Search Project Gutenberg's table of contents for books by title.
* **Database Integration:** Add selected books to a MySQL database for analysis.
* **Text Analysis:** Perform various examples of text analysis on selected books, including:
    * Finding the most frequent words.
    * Finding the N most frequent words.
    * Identifying words used only once.
    * Generating word clouds.
    * Finding the longest/shortest sentences.
    * Calculating average sentence length.
    * Finding sentences starting with a specific word.
    * Identifying the longest words.
    * Finding words with identical indices across books.
    * Identifying the book with the most distinct word usage.
* **Text Preprocessing:** Options for filtering stop words and lemmatization.
* **User-Friendly Interface:** Intuitive PyQt5 interface with clear labels and controls.
* **Database Configuration:** Allows users to set up database connection details (host, user, password, database).
* **Table of Contents Setup:** Facilitates setting up the table of contents by scraping Gutenberg's website for all available books (using the Web Archive to minimize load on Gutenberg).

 
## Installation

**1. Clone the repository:**

```bash
   git clone [https://github.com/](https://github.com/)[helland]/[Webscraper-and-book-analysis].git   
   cd [Webscraper-and-book-analysis]
```

**2. Create a virtual environment (recommended):**
 
```bash

python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
**3. Install the required packages:**

```bash

pip install    

PyQt5
mysql-connector-python
numpy
functools 
collections
wordcloud
collections  
concurrent.futures
re
fake_useragent
random
nltk
datetime
requests
bs4

```
**4. Optional: Use pyinstaller to create an exe file**

```bash
pip install    

pyinstaller 
```
Go to gui_main.py directory in command line and type:

```bash
pyinstaller --onefile -w exe_filname_of_your_choice.py
```
The exe file will be placed in the "dist" folder.

## Usage
If you created an exe file, simply double click it. Otherwise, run the main script:

```Bash

python gui_main.py
```
   
Database Setup: Go to File -> Setup database to configure your MySQL database connection.  You'll need to provide the host, user, password, and database name.  The GUI will create the database and tables if they don't already exist.

Table of Contents Setup: Go to File -> Setup Table of content to populate the database with information on all books available as well as the basic information about them (author, language etc.) from Gutenberg. Most importantly, it will add the links needed to download the full books.  This may take some time.

Book Search: Use the search bar to find books by title.  Select books from the search results and click "Add to DB" to add them to your database. The book will be encoded thrice. First, as the normal text of the book, second, the normal text with stopwords filtered out, and third, with the text lemmatized. How long it takes to encode and upload each book to the database, depends on the length of the book. The lengthier books can take several minutes if your hardware is somewhat dated.

Book Selection: Select books from the "Books" list widget to perform analysis on them. 

Analysis Selection: Choose the desired analysis type from the dropdown menu.

Enter: Click the "Enter" button to run the selected analysis. The results will be displayed in the main text area. 

It is this word analysis the code has been optimized to run fast and in bulk. While encoding and uploading the books to a database slows down the process of analyzing the text, it allows the analysis itself to run much faster. The idea is that once your analysis functions become sufficiently complex and the amount of books you want to analyze becomes large enough, this roundabout method of storing and encoding the book texts will become increasingly worth it in terms of runtime. After all, the amount of time spent on storing and encoding books increases linearly with the number of books you want to handle, but the analyses can potentially have a runtime that increases exponentially (or at the very least, geometrically / nlogn).

## Code Structure
frontend/: The main script can be found here along with modules for text formatting and other frontend utilities.
	
	frontend/gui_main.py: The main script that initializes and runs the PyQt5 GUI.
	frontend/mField_text_formatting.py: Functions that determine the appearance of text in the main field of the GUI.

webscraper/: Contains modules for web scraping, database interaction, book object definitions, and analysis functions.
	
	webscraper/__init__.py: The main script handling the command-line interface and coordinating the other modules.
	webscraper/init_database.py: Contains functions for database initialization (creating tables).
	webscraper/setup_scraper.py: Contains functions for scraping the table of contents and populating the database.
	webscraper/scraper.py: Contains functions for scraping book data from Project Gutenberg.
	webscraper/utility_functions.py: Contains utility functions for database interaction, string manipulation, etc.
	webscraper/book.py: Defines a Book class to represent book data.
	webscraper/analysis_functions.py: Contains functions for text analysis (word frequency, sentence length, etc.).

misc/: nothing of note, except perhaps some diagrams and generated files (like wordclouds).
	
	misc/database_table_diagram: Mermaid code to show the database table structure.

## License
	public domain	
