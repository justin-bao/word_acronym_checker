#!/usr/bin/env python3

from word_table_reader import *
from word_acronym_reader import *
from shutil import copyfile

def get_acronym_table(path):
    for table in get_docx_tables(path):
        row = get_text_for_table(table)[0]
        if row[0].strip().lower() == "acronym":
            return table

def get_table_acronyms(path):
    table = get_acronym_table(path)

    table_acronyms = []
    for row in get_text_for_table(table):
        if row[0].strip().lower() != "acronym":
            table_acronyms.append(row[0])
    return table_acronyms

def add_table_row(path, acronym, description):
    document = Document(path)
    acronym_table = None
    for table in document.tables:
        if table.cell(0, 0) != None and table.cell(0, 0).text.strip().lower() == "acronym":
            acronym_table = table
            break

    new_row = acronym_table.add_row()
    new_row.cells[0].text = acronym
    new_row.cells[1].text = description
    document.save(path)

def remove_table_row(path, acronym):
    document = Document(path)
    acronym_table = None
    for table in document.tables:
        if table.cell(0, 0) != None and table.cell(0, 0).text.strip().lower() == "acronym":
            acronym_table = table
            break

    tbl = acronym_table._tbl
    for row in table.rows:
        if row.cells[0].text == acronym:
            tbl_row = row._tr
            tbl.remove(tbl_row)
    document.save(path)

def process(path):
    read_acronyms = get_all_acronyms(path)
    table_acronyms = get_table_acronyms(path)

    table = get_acronym_table_docx(path)

    for acronym in set(read_acronyms) - set(table_acronyms):
        add_table_row(path, acronym, acronym)

    for acronym in set(table_acronyms) - set(read_acronyms):
        remove_table_row(path, table, acronym)

    new_table = get_acronym_table(path)
    new_table_acronyms = get_table_acronyms(path)

def get_acronym_table_docx(path):
    document = Document(path)
    for table in document.tables:
        if table.cell(0, 0) != None and table.cell(0, 0).text.strip().lower() == "acronym":
            return table

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
