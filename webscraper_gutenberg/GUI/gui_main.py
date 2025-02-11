# Created by: PyQt5 UI code generator 5.15.11
from PyQt5 import QtCore, QtGui, QtWidgets
import webscraper.utility_functions as utils
import mysql.connector
import webscraper.init_database as init
import webscraper.analysis_functions as analysis
import webscraper.params as params
import webscraper.book as book
import cgitb 
cgitb.enable(format = 'text')
 
# Code without comments on it is auto-generated with Qt Designer
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # database connection details - TODO: create function for the user to enter these details, preferably in the "File" menu (Setup database), giving the user a popup with fields to enter the details and an enter button
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
        self.search_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_lineEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_lineEdit.setSizePolicy(sizePolicy)
        self.search_lineEdit.setObjectName("search_lineEdit")
        self.horizontalLayout_search.addWidget(self.search_lineEdit)
        self.search_pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_pushButton.sizePolicy().hasHeightForWidth())
        self.search_pushButton.setSizePolicy(sizePolicy)
        self.search_pushButton.setObjectName("search_pushButton")
        self.horizontalLayout_search.addWidget(self.search_pushButton)
        self.gridLayout_search.addLayout(self.horizontalLayout_search, 1, 0, 1, 1)
        self.horizontalLayout_topBar.addLayout(self.gridLayout_search)
        self.horizontalLayout_topBar.setStretch(0, 1)
        self.horizontalLayout_topBar.setStretch(1, 1)
        self.horizontalLayout_topBar.setStretch(2, 3)
        self.verticalLayout_mainText_topBar.addLayout(self.horizontalLayout_topBar)
        self.textEdit_mainField = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_mainField.setObjectName("textEdit_mainField")
        self.verticalLayout_mainText_topBar.addWidget(self.textEdit_mainField)
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
        
        # get all stored books and populate the "Books" list with them
        books_in_database = utils.get_stored_and_processed_books(self.db_config)  
        sorted_books = sorted(books_in_database, key=lambda d: d['Title'])                  # sort books by title name
        self.listWidget_books.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)  # enable selection of multiple items
        
        for book in sorted_books:
            item = QtWidgets.QListWidgetItem(book['Title'])  # Create item
            font = QtGui.QFont()
            font.setBold(True)  # Set the font to bold
            item.setFont(font)  # Apply the font to the item
            item.setFlags(item.flags() | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # Make item selectable
            self.listWidget_books.addItem(book['Title']) # Add book to the list
        
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
        self.actionToday_s_Temperature = QtWidgets.QAction(MainWindow)
        self.actionToday_s_Temperature.setObjectName("actionToday_s_Temperature")
        self.action24_Hour_Temperature = QtWidgets.QAction(MainWindow)
        self.action24_Hour_Temperature.setObjectName("action24_Hour_Temperature")
        self.actionThis_Week_s_Temperature = QtWidgets.QAction(MainWindow)
        self.actionThis_Week_s_Temperature.setObjectName("actionThis_Week_s_Temperature")
        self.actionThis_Week_s_Percipitation = QtWidgets.QAction(MainWindow)
        self.actionThis_Week_s_Percipitation.setObjectName("actionThis_Week_s_Percipitation")
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
        self.search_pushButton.setText(_translate("MainWindow", ">"))
        self.groupBox_leftSide.setTitle(_translate("MainWindow", "Alter text"))
        self.checkBox_filter.setText(_translate("MainWindow", "Filter Stoppwords"))
        self.checkBox_lemmatization.setText(_translate("MainWindow", "Lemmatization"))
        self.label_books.setText(_translate("MainWindow", "Books"))
        self.button_enter.setText(_translate("MainWindow", "Enter"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionReset.setText(_translate("MainWindow", "Reset"))
        self.actionToday_s_Temperature.setText(_translate("MainWindow", "Today\'s Temperature"))
        self.action24_Hour_Temperature.setText(_translate("MainWindow", "24 Hour Temperature"))
        self.actionThis_Week_s_Temperature.setText(_translate("MainWindow", "This Week\'s Temperature"))
        self.actionThis_Week_s_Percipitation.setText(_translate("MainWindow", "This Week\'s Percipitation"))
        self.actionSetup_database.setText(_translate("MainWindow", "Setup database"))
        self.actionSetup_Table_of_content.setText(_translate("MainWindow", "Setup Table of content"))

    # check which books has been selected by the user
    def get_selected_books(self):    
        selected_books = self.listWidget_books.selectedItems()
        books = []
          
        for selected_book in selected_books:
      
            book_id = [utils.get_book_ids_with_title(selected_book.text(), False, self.db_config)] # get the books's id based on title
       
            books.append(book.Book(book_id, self.db_config, self.checkBox_filter.isChecked(), self.checkBox_lemmatization.isChecked())) # populate Book objects
   
        return books

    # actions taken when "enter" button is clicked.  
    def enter_button(self):
        
        # get books from the list selected by the user
        books = self.get_selected_books()
        if not books: 
            print("No books selected.")
            return None # The button takes no action if no books are selected
        print(f"book text: {books[0].text}")
        print(f"book language: {books[0].language_name}")
        # Select which version of the encoded book you want to handle (regular, filtered or lemmatized)
        encoding_mode = 0
        if self.checkBox_lemmatization.isChecked() and self.checkBox_filter.isChecked():    # if both boxes are checked, uncheck both and handle the regular text
            encoding_mode = 0
        elif self.checkBox_lemmatization.isChecked():   
            encoding_mode = 1
        elif self.checkBox_filter.isChecked():
            encoding_mode = 2
        
        # Decide what type of text analysis you want to do on the selected books
        book_analysis = self.comboBox_analysis.currentIndex()        
        
        # TODO: move finding "exclude values" to a method in the book object and just make a getter/setter so it can be changed if it needs to be customized
        match book_analysis:
            # Find the most frequent word used in the selected books
            case 1:                        
                most_frequent_word = []
                for book in books:
                    exclude_values = utils.get_non_alphanumerics(f"{book.language_name}dictionary", params.db_config) # words and symbols to remove from the analysis
                    word = analysis.find_most_frequent_word(book.text, exclude_values)
                    most_frequent_word.append(word)
        
                displayed_text = str(most_frequent_word)
                self.textEdit_mainField.setText(displayed_text)
            # Find the N most frequent words used in the selected books
            case 2:                         
                most_frequent_words = []
                for book in books:
                    exclude_values = utils.get_non_alphanumerics(f"{book.language_name}dictionary", params.db_config) # words and symbols to remove from the analysis
                    word = analysis.find_top_n_most_frequent(book.text, self.get_N_input(), exclude_values)
                    most_frequent_words.append(word)
      
                displayed_text = str(most_frequent_words)
                self.textEdit_mainField.setText(displayed_text)
            # Find all words used only once in selected books    
            case 3:
                unique_words = []
                for book in books:
                    exclude_values = utils.get_non_alphanumerics(f"{book.language_name}dictionary", params.db_config) # words and symbols to remove from the analysis
                    words = analysis.find_unique_words(book.text, exclude_values)
                    unique_words.append(words)
      
                displayed_text = str(unique_words)
                self.textEdit_mainField.setText(displayed_text)                
                 
            # generate a wordcloud for selected books
            case 4:
                for book in books:
                    book_text = analysis.cipher_decoder(book.text, book.language, params.db_config)
                    delimiter = " "
                    book_text = delimiter.join(book_text)
                    analysis.generate_wordcloud(book_text, f"{book.book_id}.png")
            # Find the longest sentences in selected books
            case 5:
                longest_sentences = [] 
                for book in books:
                    exclude_values = utils.get_non_alphanumerics(f"{book.language_name}dictionary", params.db_config) # words and symbols to remove from the analysis
                    sentences = analysis.find_longest_sentences(book.text, params.punctuations)
                    longest_sentences.append(sentences)
      
                displayed_text = str(longest_sentences)
                self.textEdit_mainField.setText(displayed_text)                  
                
            # Find the shortest sentences in selected books
            case 6:
                shortest_sentences = []  
                for book in books:
                    exclude_values = utils.get_non_alphanumerics(f"{book.language_name}dictionary", params.db_config) # words and symbols to remove from the analysis
                    sentences = analysis.find_shortest_sentences(book.text, params.punctuations)
                    shortest_sentences.append(sentences)
      
                displayed_text = str(shortest_sentences)
                self.textEdit_mainField.setText(displayed_text)  
            # Calculate Average sentence length for selected books
            case 7:  
                averages = []  
                for book in books:
                    exclude_values = utils.get_non_alphanumerics(f"{book.language_name}dictionary", params.db_config) # words and symbols to remove from the analysis
                    average = analysis.calculate_average_sentence_length(book.text, params.punctuations)
                    averages.append(average)
      
                displayed_text = str(averages)
                self.textEdit_mainField.setText(displayed_text) 
            # Find sentences starting with input from N lineField in selected books
            case 8: 
                sentences = []  
                for book in books:
                    exclude_values = utils.get_non_alphanumerics(f"{book.language_name}dictionary", params.db_config) # words and symbols to remove from the analysis
                    sentence = analysis.calculate_average_sentence_length(book.text, params.punctuations, self.get_N_input())
                    sentences.append(sentence)
      
                displayed_text = str(sentences)
                self.textEdit_mainField.setText(displayed_text)                 
            # Find the longest words in selected books
            case 9: 
                longest_words = []  
                for book in books:
                    exclude_values = utils.get_non_alphanumerics(f"{book.language_name}dictionary", params.db_config) # words and symbols to remove from the analysis
                    longest_word = analysis.find_longest_words(book.text, book.language, self.db_config)
                    longest_words.append(longest_word)
      
                displayed_text = str(longest_words)
                self.textEdit_mainField.setText(displayed_text)  
            # Find all words with identical indices in every selected book (word number 10329 is the same in all books as an exmple)
            case 10:
                equivalent_index_words = analysis.word_placement_equivalence(books)
                displayed_text = str(equivalent_index_words)
                self.textEdit_mainField.setText(displayed_text)  
            # User forgott to choose an option from the dropdown menu    
            case 0:
                print("Choose which analysis you want to perform on the selected books.")
            case _:
                print("Something went wrong")
        

    # get whatever was written in the N field.
    def get_N_input(self):    
        N_input = self.lineEdit_N.text()
        if N_input and N_input.isdigit():      
            return int(N_input)
        else:
            return N_input

    # set database login details - TODO: 
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
        
        # Create the database and tables if they're not already present on the given host - NOTE: commented out while debugging, reapply later
        #init.create_database(self.db_config)
        #init.create_tables(self.db_config)
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
    
    # TODO: Implement table of content setup functionality
    def setup_table_of_content(self):
        return None
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
