

# Created by: PyQt5 UI code generator 5.15.11
from PyQt5 import QtCore, QtGui, QtWidgets
import webscraper.utility_functions as utils
import mysql.connector
import webscraper.database_init as init
import webscraper.analysis_functions as analysis
import webscraper.params as params
import webscraper.book as book
import webscraper.scraper as scraper
import webscraper.setup_scraper as setup
import frontend.mField_text_formatting as mField
from functools import lru_cache
import time
import cgitb 
cgitb.enable(format = 'text')
 
# Code without comments on it is auto-generated with Qt Designer
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # database connection details (default values hard coded in unless the user specifies other details in the File menu) 
        self.db_config = {
        'host': 'localhost',
        'user': 'helland',
        'password': 'Ganymedes8787',
        'database': 'book_project',
        'use_pure': 'True'
        }
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(842, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_allContent = QtWidgets.QVBoxLayout()
        self.verticalLayout_allContent.setObjectName("verticalLayout_allContent")
        self.horizontalLayout_allExcepEnterButton = QtWidgets.QHBoxLayout()
        self.horizontalLayout_allExcepEnterButton.setSpacing(6)
        self.horizontalLayout_allExcepEnterButton.setObjectName("horizontalLayout_allExcepEnterButton")
        self.verticalLayout_mainText_topBar = QtWidgets.QVBoxLayout()
        self.verticalLayout_mainText_topBar.setContentsMargins(5, 5, -1, -1)
        self.verticalLayout_mainText_topBar.setObjectName("verticalLayout_mainText_topBar")
        self.horizontalLayout_topBar = QtWidgets.QHBoxLayout()
        self.horizontalLayout_topBar.setContentsMargins(1, 1, -1, -1)
        self.horizontalLayout_topBar.setObjectName("horizontalLayout_topBar")
        self.verticalLayout_analysis = QtWidgets.QVBoxLayout()
        self.verticalLayout_analysis.setSpacing(4)
        self.verticalLayout_analysis.setObjectName("verticalLayout_analysis")
        self.label_analysis = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_analysis.sizePolicy().hasHeightForWidth())
        self.label_analysis.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_analysis.setFont(font)
        self.label_analysis.setObjectName("label_analysis")
        self.verticalLayout_analysis.addWidget(self.label_analysis)
        self.comboBox_analysis = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_analysis.sizePolicy().hasHeightForWidth())
        self.comboBox_analysis.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        self.comboBox_analysis.setFont(font)
        #self.comboBox_analysis.setSizeAdjustPolicy(QtCore.Qt.QComboBox::SizeAdjustPolicy::AdjustToMinimumContentsLengthWithIcon)
        self.comboBox_analysis.setObjectName("comboBox_analysis")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.comboBox_analysis.addItem("")
        self.verticalLayout_analysis.addWidget(self.comboBox_analysis)
        self.horizontalLayout_topBar.addLayout(self.verticalLayout_analysis)
        self.verticalLayout_N = QtWidgets.QVBoxLayout()
        self.verticalLayout_N.setSpacing(4)
        self.verticalLayout_N.setObjectName("verticalLayout_N")
        self.label_N = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_N.sizePolicy().hasHeightForWidth())
        self.label_N.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_N.setFont(font)
        self.label_N.setScaledContents(False)
        #self.label_N.setAlignment(QtCore.Qt.Qt::AlignmentFlag::AlignCenter)
        self.label_N.setObjectName("label_N")
        self.verticalLayout_N.addWidget(self.label_N)
        self.lineEdit_N = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_N.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_N.sizePolicy().hasHeightForWidth())
        self.lineEdit_N.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.lineEdit_N.setFont(font)
        self.lineEdit_N.setText("")
        #self.lineEdit_N.setAlignment(QtCore.Qt.Qt::AlignmentFlag::AlignCenter)
        self.lineEdit_N.setObjectName("lineEdit_N")
        self.verticalLayout_N.addWidget(self.lineEdit_N)
        self.horizontalLayout_topBar.addLayout(self.verticalLayout_N)
        self.gridLayout_search = QtWidgets.QGridLayout()
        self.gridLayout_search.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_search.setHorizontalSpacing(0)
        self.gridLayout_search.setVerticalSpacing(6)
        self.gridLayout_search.setObjectName("gridLayout_search")
        self.label_search = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_search.sizePolicy().hasHeightForWidth())
        self.label_search.setSizePolicy(sizePolicy)
        self.label_search.setObjectName("label_search")
        self.gridLayout_search.addWidget(self.label_search, 0, 0, 1, 1)
        self.horizontalLayout_search = QtWidgets.QHBoxLayout()
        self.horizontalLayout_search.setSpacing(0)
        self.horizontalLayout_search.setObjectName("horizontalLayout_search")
        self.lineEdit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_search.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_search.sizePolicy().hasHeightForWidth())
        self.lineEdit_search.setSizePolicy(sizePolicy)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout_search.addWidget(self.lineEdit_search)
        self.button_search = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy)
        self.button_search.setObjectName("button_search")
        self.horizontalLayout_search.addWidget(self.button_search)
        self.gridLayout_search.addLayout(self.horizontalLayout_search, 1, 0, 1, 1)
        self.horizontalLayout_topBar.addLayout(self.gridLayout_search)
        self.horizontalLayout_topBar.setStretch(0, 1)
        self.horizontalLayout_topBar.setStretch(1, 1)
        self.horizontalLayout_topBar.setStretch(2, 3)
        self.verticalLayout_mainText_topBar.addLayout(self.horizontalLayout_topBar)
        self.textEdit_mainField = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_mainField.setObjectName("textEdit_mainField")
        self.verticalLayout_mainText_topBar.addWidget(self.textEdit_mainField)
        self.textEdit_mainField.setAcceptRichText(True) # attempt at making the text field strings more easy to customize
        self.horizontalLayout_allExcepEnterButton.addLayout(self.verticalLayout_mainText_topBar)
        self.verticalLayout_rightBar = QtWidgets.QVBoxLayout()
        self.verticalLayout_rightBar.setSpacing(3)
        self.verticalLayout_rightBar.setObjectName("verticalLayout_rightBar")
        self.groupBox_leftSide = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_leftSide.sizePolicy().hasHeightForWidth())
        self.groupBox_leftSide.setSizePolicy(sizePolicy)
        self.groupBox_leftSide.setMinimumSize(QtCore.QSize(170, 55))
        font = QtGui.QFont()
        font.setBold(True)
        self.groupBox_leftSide.setFont(font)
        self.groupBox_leftSide.setObjectName("groupBox_leftSide")
        self.checkBox_filter = QtWidgets.QCheckBox(self.groupBox_leftSide)
        self.checkBox_filter.setEnabled(True)
        self.checkBox_filter.setGeometry(QtCore.QRect(18, 9, 131, 31))
        font = QtGui.QFont()
        font.setBold(False)
        self.checkBox_filter.setFont(font)
        self.checkBox_filter.setChecked(False)
        self.checkBox_filter.setObjectName("checkBox_filter")
        self.checkBox_lemmatization = QtWidgets.QCheckBox(self.groupBox_leftSide)
        self.checkBox_lemmatization.setGeometry(QtCore.QRect(18, 31, 131, 21))
        font = QtGui.QFont()
        font.setBold(False)
        self.checkBox_lemmatization.setFont(font)
        self.checkBox_lemmatization.setObjectName("checkBox_lemmatization")
        self.verticalLayout_rightBar.addWidget(self.groupBox_leftSide)
        self.label_books = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_books.sizePolicy().hasHeightForWidth())
        self.label_books.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_books.setFont(font)
        self.label_books.setObjectName("label_books")
        self.verticalLayout_rightBar.addWidget(self.label_books)
        self.listWidget_books = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.listWidget_books.sizePolicy().hasHeightForWidth())
        self.listWidget_books.setSizePolicy(sizePolicy)
        self.listWidget_books.setMinimumSize(QtCore.QSize(170, 170))
        font = QtGui.QFont()
        font.setBold(True)
        self.listWidget_books.setFont(font)
        #self.listWidget_books.setSelectionMode(QtCore.Qt.QAbstractItemView::SelectionMode::MultiSelection)
        self.listWidget_books.setObjectName("listWidget_books")
        self.verticalLayout_rightBar.addWidget(self.listWidget_books)
                     
        self.populate_book_list() # add all books in the database to the "Books" listwidget items

        
        self.verticalLayout_rightBar.setStretch(2, 1)
        self.horizontalLayout_allExcepEnterButton.addLayout(self.verticalLayout_rightBar)
        self.horizontalLayout_allExcepEnterButton.setStretch(0, 1)
        self.verticalLayout_allContent.addLayout(self.horizontalLayout_allExcepEnterButton)
        self.verticalLayout_enterButton = QtWidgets.QVBoxLayout()
        #self.verticalLayout_enterButton.setSizeConstraint(QtCore.Qt.QLayout::SizeConstraint::SetNoConstraint)
        self.verticalLayout_enterButton.setContentsMargins(1, -1, 1, 5)
        self.verticalLayout_enterButton.setObjectName("verticalLayout_enterButton")
        self.button_enter = QtWidgets.QPushButton(self.centralwidget)
        self.button_enter.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_enter.sizePolicy().hasHeightForWidth())
        self.button_enter.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.button_enter.setFont(font)
        self.button_enter.setAutoFillBackground(False)
        self.button_enter.setObjectName("button_enter")
        self.verticalLayout_enterButton.addWidget(self.button_enter)
        self.verticalLayout_allContent.addLayout(self.verticalLayout_enterButton)
        self.gridLayout.addLayout(self.verticalLayout_allContent, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 842, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.actionSetup_database = QtWidgets.QAction(MainWindow)
        self.actionSetup_database.setObjectName("actionSetup_database")
        self.actionSetup_Table_of_content = QtWidgets.QAction(MainWindow)
        self.actionSetup_Table_of_content.setObjectName("actionSetup_Table_of_content")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionReset)
        self.menuFile.addAction(self.actionSetup_database)
        self.menuFile.addAction(self.actionSetup_Table_of_content)
        self.menubar.addAction(self.menuFile.menuAction())
        self.actionSetup_database.triggered.connect(self.setup_database)
        self.actionSetup_Table_of_content.triggered.connect(self.setup_table_of_content)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # connect enter button to its function
        self.button_enter.clicked.connect(self.enter_button)

        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor(dictionary=True)   
                      
            # Connect search button
            self.button_search.clicked.connect(self.show_search_results(cursor))
            cnx.commit()
        except mysql.connector.Error as err:
            print(f"Error : {err}")
        finally:
            if cnx:
                cnx.close()
     
                   
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_analysis.setText(_translate("MainWindow", "What information about the books do you want?"))
        self.comboBox_analysis.setItemText(0, _translate("MainWindow", "Choose book analysis"))
        self.comboBox_analysis.setItemText(1, _translate("MainWindow", "Most frequent word"))
        self.comboBox_analysis.setItemText(2, _translate("MainWindow", "N most frequent words"))
        self.comboBox_analysis.setItemText(3, _translate("MainWindow", "Words that only appear once"))
        self.comboBox_analysis.setItemText(4, _translate("MainWindow", "Generate wordcloud"))
        self.comboBox_analysis.setItemText(5, _translate("MainWindow", "Find longest sentences"))
        self.comboBox_analysis.setItemText(6, _translate("MainWindow", "Find shortest sentences"))
        self.comboBox_analysis.setItemText(7, _translate("MainWindow", "Calculate Average sentence length"))
        self.comboBox_analysis.setItemText(8, _translate("MainWindow", "Find sentences starting with N"))
        self.comboBox_analysis.setItemText(9, _translate("MainWindow", "Find longest words"))
        self.comboBox_analysis.setItemText(10, _translate("MainWindow", "Find identical indices"))
        self.label_N.setText(_translate("MainWindow", "N"))
        self.label_search.setText(_translate("MainWindow", "Search Gutenberg\'s table of content for book by title:"))
        self.button_search.setText(_translate("MainWindow", ">"))
        self.groupBox_leftSide.setTitle(_translate("MainWindow", "Alter text"))
        self.checkBox_filter.setText(_translate("MainWindow", "Filter Stoppwords"))
        self.checkBox_lemmatization.setText(_translate("MainWindow", "Lemmatization"))
        self.label_books.setText(_translate("MainWindow", "Books"))
        self.button_enter.setText(_translate("MainWindow", "Enter"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionReset.setText(_translate("MainWindow", "Reset"))
        self.actionSetup_database.setText(_translate("MainWindow", "Setup database"))
        self.actionSetup_Table_of_content.setText(_translate("MainWindow", "Setup Table of content"))

    # get all stored books and populate the "Books" list with them
    def populate_book_list(self):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor(dictionary=True)        
            
            self.listWidget_books.clear() # remove all items in order to repopulate the list
            books_in_database = utils.get_stored_and_processed_books(cursor)  
            sorted_books = sorted(books_in_database, key=lambda d: d['Title'])                  # sort books by title name
            self.listWidget_books.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)  # enable selection of multiple items
            
            for book in sorted_books:
                item = QtWidgets.QListWidgetItem(book['Title'])  # Create item
                font = QtGui.QFont()
                font.setBold(True)  # Set the font to bold
                item.setFont(font)  # Apply the font to the item
                item.setFlags(item.flags() | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # Make item selectable
                self.listWidget_books.addItem(book['Title']) # Add book to the list
            
            cnx.commit()
        except mysql.connector.Error as err:
            print(f"error: {err}")
            return []
        finally:
            if cnx:
                cnx.close()
                                    
        
    # What happens when the user hits the search button
    def show_search_results(self, cursor):
   
        search_term = self.lineEdit_search.text()
        if not search_term:  # Handle empty search
            return
        else:
            self.hide_search_widgets() # hide any previous search if the user makes a new search
            
        self.search_results = utils.get_books_with_title(search_term, True, cursor)
        
            
       
        
        # Create listWidget_search
        self.listWidget_search = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_search.setGeometry(self.lineEdit_search.geometry().x(), self.lineEdit_search.geometry().y() + self.lineEdit_search.geometry().height(), self.lineEdit_search.geometry().width(), self.listWidget_books.geometry().height())
        self.listWidget_search.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget_search.setWordWrap(False) # word wrap for title display 

        # Populate listWidget_search
        for i, book_data in enumerate(self.search_results):
            if i < 50:
                item = QtWidgets.QListWidgetItem(book_data['Title'])
                font = QtGui.QFont()
                font.setBold(True)
                item.setFont(font)
                self.listWidget_search.addItem(item)
            else:
                item = QtWidgets.QListWidgetItem(f"{len(self.search_results)} books found with given search term.")
                item.setFlags(QtCore.Qt.ItemIsEnabled)  # Not selectable
                self.listWidget_search.addItem(item)
                break  # Stop adding items after the "Total found" message

        self.listWidget_search.show()

        # Create buttons
        self.button_add_to_db = QtWidgets.QPushButton("Add to DB", self.centralwidget)
        self.button_cancel = QtWidgets.QPushButton("Cancel", self.centralwidget)

        button_width = int(self.lineEdit_search.geometry().width() / 2)  # Divide width for two buttons  
        self.button_add_to_db.setGeometry(self.lineEdit_search.geometry().x(), self.listWidget_search.geometry().y() + self.listWidget_search.geometry().height(), button_width, 30)  # Adjust height as needed
        self.button_cancel.setGeometry(self.lineEdit_search.geometry().x() + button_width, self.listWidget_search.geometry().y() + self.listWidget_search.geometry().height(), button_width, 30)

        self.button_add_to_db.clicked.connect(self.add_selected_books())
        self.button_cancel.clicked.connect(self.hide_search_widgets)

        self.button_add_to_db.show()
        self.button_cancel.show()
            
            
    # Add selected books (in full) from table of content search to the database
    def add_selected_books(self):
        selected_items = self.listWidget_search.selectedItems()
        if not selected_items:
            return  # No books selected

        selected_books = []
        for item in selected_items:
            for book in self.search_results:
                if book['Title'] == item.text():
                    selected_books.append(book)
                    break
        
        added_books_titles, scraped_books = [], []
        for book_data in selected_books:
            try:
                # create dictionary for the book details
                book_dict = {   # TODO: change the scraper functions so that it won't be necessary to reformat these details between the scraper and database storage
                'title'         : '', 
                'text'          : '', 
                'author'        : '', 
                'release_date'  : '', 
                'language'      : '', 
                'word_count'    : '', 
                'character_count':'', 
                'source_website': book_data['SourceWebsite'] 
                }
                # Scrape book text + details
                book_dict['title'], book_dict['author'], book_dict['release_date'], book_dict['language'], book_dict['text'], book_dict['word_count'], book_dict['character_count'] = scraper.gutenberg_book_scraper(book_data['SourceWebsite'])
                added_books_titles.append(book_data['Title'])
                scraped_books.append(book_dict)
  
            except Exception as e:
                print(f"Error adding book {book_data['Title']}: {e}") # Print error to console
        
        self.hide_search_widgets()
        
        # Store book in the database
        self.textEdit_mainField.setText("Storing books in database. Plase wait...")
        scraper.store_books_in_database(scraped_books, params.db_config)
        self.populate_book_list() # add all books in the database to the "Books" listwidget items, including the newly stored books
        self.textEdit_mainField.setText("The following books were added to the database:\n" + "\n".join(added_books_titles))    
        # Show popup message
        QtWidgets.QMessageBox.information(self.centralwidget, "Books Added", "The following books were added to the database:\n" + "\n".join(added_books_titles))

    # remove the search results from view after the user is done with it (or hit cancel)
    def hide_search_widgets(self):
        if hasattr(self, 'listWidget_search'):
            self.listWidget_search.hide()
            self.button_add_to_db.hide()
            self.button_cancel.hide()
            del self.listWidget_search
            del self.button_add_to_db
            del self.button_cancel

    # check which books has been selected by the user
    def get_selected_books(self):    
        try:
            cnx = mysql.connector.connect(**self.db_config)
               
                
            selected_books = self.listWidget_books.selectedItems()
            books = []
              
            for selected_book in selected_books:
                cursor = cnx.cursor(dictionary=True)
                book_ids = utils.get_book_ids_with_title(selected_book.text(), False, cursor) # get the books's id based on title
                cursor = cnx.cursor()  
                for book_id in book_ids: # in case more than one book with the same title was selected, add them all.
                    books.append(book.Book(book_id, self.db_config, cursor, self.checkBox_filter.isChecked(), self.checkBox_lemmatization.isChecked())) # populate Book objects
            
            return books
        
        except mysql.connector.Error as err:
            print(f"error: {err}")
            return []
        finally:
            if cnx:
                cnx.close()
                
    # Returns the selected version of the encoded book the user wants to handle (regular, filtered or lemmatized)
    def get_encoded_text(self, book):
        encoded_text = book.text
         
        if self.checkBox_lemmatization.isChecked() and self.checkBox_filter.isChecked():    # if both boxes are checked, uncheck both and handle the regular text
            encoded_text = book.text
        elif self.checkBox_lemmatization.isChecked():   
            encoded_text = book.lemmatized_text
        elif self.checkBox_filter.isChecked():
            encoded_text = book.filtered_text
        return encoded_text
                    
    # actions taken when "enter" button is clicked.  
    def enter_button(self):
        books = self.get_selected_books()
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()   
                
            # get books from the list selected by the user
            if not books: 
                print("No books selected.")
                return None # The button takes no action if no books are selected
            
            # Decide what type of text analysis you want to do on the selected books
            book_analysis = self.comboBox_analysis.currentIndex()        
            
            # Decide what to do based on which option the user picked in the dropdown menu
            match book_analysis:
                # Find the most frequent word used in the selected books
                case 1:                        
                    most_frequent_word = []
                    for book in books:          
                        word = analysis.find_most_frequent_word(self.get_encoded_text(book), book.exclude)
                        most_frequent_word.append(word)
                    
                    text_words = analysis.cipher_decoder(most_frequent_word, book.language, cursor) # decode cipher back to text
                    displayed_text = mField.books_word(books, text_words)
                    self.textEdit_mainField.setText(displayed_text)
                    cnx.commit()
                    
                # Find the N most frequent words used in the selected books
                case 2:                         
                    most_frequent_words = []
                    for book in books:
                        word = analysis.find_top_n_most_frequent(self.get_encoded_text(book), self.get_N_input(), book.exclude)
                        most_frequent_words.append(word)
          
                    text_words = analysis.cipher_decoder(most_frequent_words, book.language, cursor) # decode cipher back to text
                    displayed_text = mField.books_words(books, text_words)
                    self.textEdit_mainField.setText(displayed_text)
                    cnx.commit()
                    
                # Find all words used only once in selected books    
                case 3:
                    unique_words = []
                    for book in books:
                        words = analysis.find_unique_words(self.get_encoded_text(book), book.exclude)
                        unique_words.append(words)
          
                    text_words = analysis.cipher_decoder(unique_words, book.language, cursor) # decode cipher back to text
                    displayed_text = mField.books_words(books, text_words)
                    self.textEdit_mainField.setText(displayed_text)      
                    cnx.commit()
                    
                # generate a wordcloud for selected books
                case 4:
                    for book in books:
                        book_text = analysis.cipher_decoder(self.get_encoded_text(book), book.language, cursor)
                        delimiter = " "
                        book_text = delimiter.join(book_text)
                        analysis.generate_wordcloud(book_text, f"{book.book_id}.png")
                    cnx.commit()
                        
                # Find the longest sentences_starting_with_N in selected books
                case 5:
                    longest_sentences, sentences_per_book = [], [] 
    
                    for book in books:
                        book.remove_word_from_text(book.line_break) # don't include line breakes in the count
                        sentences_starting_with_N = analysis.find_longest_sentences(self.get_encoded_text(book), params.punctuations)
                        sentences_per_book.append(len(sentences_starting_with_N)) # count how many sentences_starting_with_N the current book had and add it to list (typically only 1, maybe 2 per book)
                        longest_sentences += sentences_starting_with_N
                    
                    text_sentences = analysis.cipher_decoder(longest_sentences, book.language, cursor) # decode cipher back to text
                    displayed_text = mField.books_sentences(books, text_sentences, sentences_per_book)
                    self.textEdit_mainField.setText(displayed_text)                   
                    cnx.commit()
                    
                # Find the shortest sentences_starting_with_N in selected books
                case 6:
                    shortest_sentences, sentences_per_book = [], [] 
                    for book in books:
                        book.remove_word_from_text(book.line_break) # don't include line breakes in the count
                        sentences_starting_with_N = analysis.find_shortest_sentences(self.get_encoded_text(book), params.punctuations)
                        sentences_per_book.append(len(sentences_starting_with_N)) # count how many sentences_starting_with_N the current book had and add it to list (usually single word sentences_starting_with_N, often hundreds)
                        shortest_sentences += sentences_starting_with_N
                        
                             
                    text_sentences = analysis.cipher_decoder(shortest_sentences, book.language, cursor) # decode cipher back to text
                    displayed_text = mField.books_sentences(books, text_sentences, sentences_per_book)
                    self.textEdit_mainField.setText(displayed_text)   
                    cnx.commit()
                                    
                # Calculate Average sentences length for selected books
                case 7:  
                    averages = []  
                    for book in books:
                        book.remove_word_from_text(book.line_break) # don't include line breakes in the count
                        average = analysis.calculate_average_sentence_length(self.get_encoded_text(book), params.punctuations)
                        averages.append(average)
                        
                    rounded_averages =  [str(round(x,1)) for x in averages] 
                    displayed_text = mField.books_word(books, rounded_averages)
                    self.textEdit_mainField.setText(displayed_text)
                    cnx.commit()
                     
                # Find sentences starting with input word from N lineField in selected books
                case 8: 
                    sentences_starting_with_N, sentences_per_book = [], []      
                    for book in books:
                        word = self.get_id_from_word(self.get_N_input(), book, cursor) #NOTE: This needs a better solution. One database connection per book just to get a single word is an unacceptable slowdown...
                        sentences = analysis.find_sentences_starting_with(self.get_encoded_text(book), params.punctuations, word)
                        sentences_per_book.append(len(sentences)) # count how many sentences the current book had and add it to list 
                        sentences_starting_with_N += sentences
                    
                    text_sentences = analysis.cipher_decoder(sentences_starting_with_N, book.language, cursor) # decode cipher back to text
                    displayed_text = mField.books_sentences(books, text_sentences, sentences_per_book)
                    self.textEdit_mainField.setText(displayed_text)
                    cnx.commit()
                                  
                # Find the longest words in selected books
                case 9: 
                    longest_words = []  
                    for book in books:
                        longest_word = analysis.find_longest_words(self.get_encoded_text(book), book.language, cursor)
                        longest_words.append(longest_word)
          
                    text_longest_words = analysis.cipher_decoder(longest_words, book.language, cursor) # decode cipher back to text
                    displayed_text = mField.books_words(books, text_longest_words)
                    self.textEdit_mainField.setText(displayed_text) 
                    cnx.commit()
                     
                # Find all words with identical indices in every selected book (word number 10329 is the same in all books as an exmple)
                case 10:
                    for book in books:
                        book.remove_word_from_text(book.line_break) # don't include line breakes 
                    indices_with_same_words = analysis.word_placement_equivalence(books)  
                    
                    full_book_text = analysis.cipher_decoder(books[0].get_text(), books[0].get_language(), cursor) # decode a full book back to text      
                    displayed_text = mField.indices_words(indices_with_same_words, full_book_text) # get only words at indices and format them
                    self.textEdit_mainField.setText(displayed_text) 
                    cnx.commit()
                     
                # User forgott to choose an option from the dropdown menu    
                case 0:
                    displayed_text = "Choose which analysis you want to perform on the selected books."
                    self.textEdit_mainField.setText(displayed_text)  
                case _:
                    displayed_text = "Something went wrong."
                    self.textEdit_mainField.setText(displayed_text)                       

        except mysql.connector.Error as err:
            print(f"error: {err}")
            return []
    
        finally:
            if cnx:
                cnx.close()
                
        # get whatever was written in the N field.
    def get_N_input(self):    
        N_input = self.lineEdit_N.text()
        if N_input and N_input.isdigit():      
            return int(N_input)
        else:
            return N_input
    
    # get the input word's id value (from dictionary determined by input book's language). NOTE: make a more general function for this outside the gui? maybe later
    @lru_cache(maxsize=1024) 
    def get_id_from_word(self, word, book, cursor):
        #try:
        #    cnx = mysql.connector.connect(**self.db_config)
        #    cursor = cnx.cursor()
                    
        get_word_id_query = f"SELECT Id FROM {book.language_name.lower()}dictionary WHERE BINARY Word = %s" # BINARY for case sensitivity
        cursor.execute(get_word_id_query, (word,))
        word_id = cursor.fetchone()[0]        
        cnx.commit()
        return word_id
        
        #except mysql.connector.Error as err:
        #    print(f"Error finding the id of the word '{word}' from the table {book.language_name.lower()}dictionary: {err}")
        #finally:
        #    if cnx:
        #        cnx.close()
                
    # set database login details 
    def setup_database(self):
        # Create a dialog
        dialog = QtWidgets.QDialog(MainWindow)  # Use MainWindow as parent
        dialog.setWindowTitle("Database Setup")

        # Create input fields and labels
        host_label = QtWidgets.QLabel("Host:")
        host_input = QtWidgets.QLineEdit()
        user_label = QtWidgets.QLabel("User:")
        user_input = QtWidgets.QLineEdit()
        password_label = QtWidgets.QLabel("Password:")
        password_input = QtWidgets.QLineEdit()
        password_input.setEchoMode(QtWidgets.QLineEdit.Password)  # Hide password
        database_label = QtWidgets.QLabel("Database:")
        database_input = QtWidgets.QLineEdit()
        use_pure_checkbox = QtWidgets.QCheckBox("Use Pure")
        use_pure_checkbox.setChecked(True)  # Set default to checked


        # Create buttons
        ok_button = QtWidgets.QPushButton("OK")
        cancel_button = QtWidgets.QPushButton("Cancel")

        # Layout the dialog
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(host_label)
        layout.addWidget(host_input)
        layout.addWidget(user_label)
        layout.addWidget(user_input)
        layout.addWidget(password_label)
        layout.addWidget(password_input)
        layout.addWidget(database_label)
        layout.addWidget(database_input)
        layout.addWidget(use_pure_checkbox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        # Connect buttons
        ok_button.clicked.connect(lambda: self.get_db_config(dialog, host_input, user_input, password_input, database_input, use_pure_checkbox))
        cancel_button.clicked.connect(dialog.reject)  # Close on cancel
        
        # Create the database and tables if they're not already present on the given host 
        init.create_database(self.db_config)
        init.create_tables(self.db_config)
        dialog.exec_()  # Show the dialog


    def get_db_config(self, dialog, host_input, user_input, password_input, database_input, use_pure_checkbox):
        host = host_input.text()
        user = user_input.text()
        password = password_input.text()
        database = database_input.text()
        use_pure = use_pure_checkbox.isChecked()

        if not host or not user or not password or not database: #Check if any field is empty.
            QtWidgets.QMessageBox.critical(MainWindow, "Error", "All fields must be filled.")
            return

        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'use_pure': use_pure
        }

        print("Database config:", self.db_config)
        dialog.accept()  # Close the dialog if OK is clicked and all input fields are filled.
    
    # set up the table of content by scraping the sites listing all books sorted by first letter (going through web archive to prevent us from bothering Gutenberg too much) 
    def setup_table_of_content(self):
        urls = params.bypass_url
        display_text = ""
        
        all_books = []
        for url in urls: 
            display_text += f"<br>requesting data from website: {url}"
            self.textEdit_mainField.setText(display_text)  # update text field to make sure the user sees something happening
            scraped_books = setup.scrape_book_info(url)
            all_books.extend(scraped_books)
            
            # Pause for a bit between requests (in an attempt to not bother gutenberg/internet archive too much or hit their max request limit)
            display_text += "<br>Waiting 5 seconds for next request."
            self.textEdit_mainField.setText(display_text)  # update text field to make sure the user sees something happening  
            time.sleep(5) 
        # Insert books into the database
        setup.insert_books_into_database(all_books, params.db_config)
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
