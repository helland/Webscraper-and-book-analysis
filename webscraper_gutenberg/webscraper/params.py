
# database connection details (for when it's not otherwise specified)
db_config = {
'host': 'localhost',
'user': 'helland',
'password': 'Ganymedes8787',
'database': 'book_project',
'use_pure': 'True'
}

# TODO: make a function that finds punctuations in input language dictionary table instead of relying on hardcoded crap like this
punctuations = [1,4, 5, 6, 7, 4248] # corresponds to [".","!","?",":",";", "CHAPTER"] in englishdictionary # sentence punctuations - "CHAPTER" added as a punctuation to avoid errors in the table of content
line_break = 17 # "\n" in the englishdictionay table