
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