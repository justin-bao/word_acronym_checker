# word_acronym_checker

In order to run the word_acronym_checker, use `python word_acronym_checker.py [document file] [option] [whitelist file]`, where `[whitelist file]` is optional. 

The options for running are
- `remove`: remove acronyms from the acronym table that are not present in the document
- `strikethrough`: strikethrough acronyms from the acronym table that are not present in the document
- `report`: find all acronyms from the acronym table that are not present in the document and place them in a new table for removed acronyms

The whitelist file should be a text file consisting of each acronym to be whitelisted on its own line.
