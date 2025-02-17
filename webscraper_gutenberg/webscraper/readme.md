# Gutenberg Book Analyzer

This Python script (the __init__.py in the webscraper folder) provides a command-line interface for scraping, storing, and analyzing books from Project Gutenberg. It allows users to initialize a database, populate a table of contents of available books, scrape book data, store it in the database, and perform basic text analysis. The main purpose of this script is to test the backend code and make sure everything works. For a more user-friendly experience working with this code, use the gui_main.script described in the readme file in the folder above.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
    - [Database Initialization](#database-initialization)    
    - [Populate Table of Contents](#populate-table-of-contents)    
    - [Add Books to the Database](#add-books-to-the-database)    
    - [Data Analysis on the Books](#data-analysis-on-the-books)
- [Code Structure](#code-structure)
- [Dependencies](#dependencies)
- [License](#license) 



## Introduction

This project aims to simplify the process of working with Project Gutenberg texts for the purpose of word analysis. It automates the scraping of book information, storage in a database, and provides basic analytical tools. The command-line interface makes it easy to interact with the system and perform various tasks.

## Features

* **Database Initialization:** 

Creates the necessary database tables.
* **Table of Contents Generation:** 

Scrapes Project Gutenberg's website (via the Internet Archive) to build a local table of contents of available books.
* **Book Scraping and Storage:** 

Downloads book text and metadata from Project Gutenberg and stores it in the database.  Handles cases where multiple books share the same title.
* **Basic Text Analysis:** 

Provides functionalities to analyze the stored book data, including finding the most frequent words, longest/shortest sentences, word clouds, and more.
* **Command-Line Interface:**  

Easy-to-use command-line interface for all functionalities.
* **Book Object:** 

An object meant to handle all stored information on a book while changes or data analysis is being performed on it.

## Installation

1. **Clone the repository:**

	git clone [https://github.com/helland/Webscraper-and-book-analysis.git](https://github.com/helland/Webscraper-and-book-analysis/tree/main/webscraper_gutenberg.git)   

2. **Install dependencies:**

```bash
pip install -r requirements.txt  # (see Dependencies)
```
	
	
3. **Database setup:**
 	Create a MySQL database and user with appropriate permissions.  Update the db_config dictionary in the main script with your database credentials.
   
## Usage 
The script is run from the command line (Note: a GUI will be added in the future):

	python __init__.py   
	
## Database Initialization
To create the database tables:
	
	init123
	
## Populate Table of Contents
To populate the table of contents (That is, it will fill out the "book" table in the database with all available books on Project Gutenberg, with a title, link, author and language, but not the full content or details on the books), use the following command:
	
	setup123
	
## Add Books to the Database
To add a book to the database, enter the book title:
	
	The Time Machine  # Example

The script will search the table of contents and, if found, scrape the book data and store it in the database. If multiple books with the same title are found, you will be prompted to choose which one to add.
	
## Data Analysis on the Books
To perform analysis on a book, leave the command prompt empty, and then enter the title of the book you want to analyze:
	
	(Leave command prompt empty)
	The Adventures of Sherlock Holmes  # Example
	
The script will then perform the analysis and print the results. A word cloud will also be generated and saved as a PNG file. Note: Once the GUI has been made, these analysis functions will be both expanded upon and the user will be given a choice in exactly which kind of analysis they want to perform on the book(s).

## Code Structure
	webscraper/__init__.py: The main script handling the command-line interface and coordinating the other modules.
	webscraper/init_database.py: Contains functions for database initialization (creating tables).
	webscraper/setup_scraper.py: Contains functions for scraping the table of contents and populating the database.
	webscraper/scraper.py: Contains functions for scraping book data from Project Gutenberg.
	webscraper/utility_functions.py: Contains utility functions for database interaction, string manipulation, etc.
	webscraper/book.py: Defines a Book class to represent book data.
	webscraper/analysis_functions.py: Contains functions for text analysis (word frequency, sentence length, etc.).

## Dependencies
	requests
	numpy
	mysql-connector-python  
	functools
	concurrent.futures
	nltk
	fake_useragent

## License
	public domain	