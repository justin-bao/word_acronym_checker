#!/usr/bin/env python3

from word_table_reader import *
from word_acronym_reader import *

if __name__=="__main__":
    import sys

    all_acronyms = get_all_acronyms(sys.argv[1])
    explained_acronyms = get_explained_acronyms(sys.argv[1])

    acronyms_in_table = []
    acronyms_not_in_table = []

    explained_acronyms_in_table = []
    explained_acronyms_not_in_table = []

    unexplained_acronyms = []

    abbreviation_table = []

    for table in get_docx_tables(sys.argv[1]):
        row = get_text_for_table(table)[0]
        if row[0].isupper():
            abbreviation_table = table
            break

    for row in get_text_for_table(abbreviation_table):
        for acronym in all_acronyms:
            if row[0] == acronym:
                acronyms_in_table.append(acronym)
            else:
                acronyms_not_in_table.append(acronym)

        for acronym in explained_acronyms:
            if row[0] == acronym[0] and row[1] == acronym[1]:
                explained_acronyms_in_table.append(acronym)
            else:
                explained_acronyms_not_in_table.append(acronym)

    for acronym in explained_acronyms:
        if acronym[0] not in all_acronyms:
            unexplained_acronyms.append(acronym[0])


    print("Acronyms not in the table: ")
    for acronym in acronyms_not_in_table:
        print(acronym)
    print()

    print("Acronyms that have not been explained: ")
    for acronym in unexplained_acronyms:
        print(acronym)
    print()
