#!/usr/bin/env python3

# Program for syncing a table of acronyms with the acronyms in the Word doc.
from .word_table_reader import *
from .word_acronym_reader import *

def create_acronym_table(path):
    """
    Creates an empty acronym table in the given doc.
    """

    document = Document(path)
    new_table = document.add_table(rows=1, cols=2, style='Table Grid')
    new_table.cell(0, 0).text = "ACRONYM"
    new_table.cell(0, 1).text = "MEANING"
    document.save(path)

def get_acronym_table(path):
    """
    Get the table (for word_table_reader) in the given doc with the acronyms and meanings.
    """

    acronym_table = None
    for table in get_docx_tables(path):
        row = get_text_for_table(table)[0]
        if row[0].strip().lower() == "acronym":
            acronym_table = table
            break
    return acronym_table

def get_acronym_table_docx(path):
    """
    Get the table (for docx) in the given doc with the acronyms and meanings.
    """

    document = Document(path)
    for table in document.tables:
        if table.cell(0, 0) != None and table.cell(0, 0).text.strip().lower() == "acronym":
            return table

def get_table_acronyms(path):
    """
    Get all the acronyms from the acronym table in the given doc, or throw a ValueError if the table is missing.
    """

    table = get_acronym_table(path)
    if table == None:
        raise ValueError("Acronym table not found")

    table_acronyms = []
    for row in get_text_for_table(table):
        if row[0].strip().lower() != "acronym":
            table_acronyms.append(row[0])
    return table_acronyms

def add_table_row(path, acronym, description):
    """
    Add a row with given acronym and meaning to the acronym table in the given doc, or throw a ValueError if the table is missing.
    If an acronym has not been explained yet, print this missing acronym to the console.
    """

    document = Document(path)
    acronym_table = None
    for table in document.tables:
        if table.cell(0, 0) != None and table.cell(0, 0).text.strip().lower() == "acronym":
            acronym_table = table
            break

    if acronym_table == None:
        raise ValueError("Acronym table not found")

    new_row = acronym_table.add_row()
    new_row.cells[0].text = acronym
    new_row.cells[1].text = description
    document.save(path)

def remove_table_row(path, acronym):
    """
    Remove a row with given acronym from the acronym table in the given doc, or throw a ValueError if the table is missing.
    """

    document = Document(path)
    acronym_table = None
    for table in document.tables:
        if table.cell(0, 0) != None and table.cell(0, 0).text.strip().lower() == "acronym":
            acronym_table = table
            break

    if acronym_table == None:
        raise ValueError("Acronym table not found")

    tbl = acronym_table._tbl
    for row in table.rows:
        if row.cells[0].text == acronym:
            tbl_row = row._tr
            tbl.remove(tbl_row)
    document.save(path)

def process(path):
    """
    Process the given doc by adding all acronyms to the acronym table that are in the doc (if not already in the table)
    and removing all acronyms from the acronym table that aren't in the doc.
    """

    read_acronyms = get_all_acronyms(path)
    table_acronyms = get_table_acronyms(path)
    explained_acronyms = get_explained_acronyms(path)

    table = get_acronym_table_docx(path)

    for acronym in set(read_acronyms) - set(table_acronyms):
        if acronym in explained_acronyms:
            add_table_row(path, acronym, explained_acronyms[acronym])
        else:
            print("Acronym " + acronym + " never explained")
            add_table_row(path, acronym, "(Meaning Missing)")

    for acronym in set(table_acronyms) - set(read_acronyms):
        remove_table_row(path, acronym)

    new_table = get_acronym_table(path)
    new_table_acronyms = get_table_acronyms(path)

if __name__=="__main__":
    """
    Processes the given doc and reports which acronyms have been added and deleted from the table.
    """

    import sys
    path = sys.argv[1]

    if get_acronym_table(path) == None:
        create_acronym_table(path)

    acronyms_in_table = get_table_acronyms(path)

    print("Processing " + path + "...")
    print("")
    process(path)

    new_acronyms_in_table = get_table_acronyms(path)


    print("Acronyms added to the table: ")
    for acronym in set(acronyms_in_table) - set(new_acronyms_in_table):
        print(acronym)
    print("")

    print("Acronyms removed from the table: ")
    for acronym in set(new_acronyms_in_table) - set(acronyms_in_table):
        print(acronym)
    print("")
