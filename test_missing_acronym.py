#!/usr/bin/env python3

from word_table_reader import *
from word_acronym_reader import *
from shutil import copyfile
import pytest
import os

path = "tests/data/test2_invalid.docx"
read_acronyms = []
table_acronyms = []
abbreviation_table = None

for table in get_docx_tables(path):
    row = get_text_for_table(table)[0]
    if row[0].strip().lower() == "acronym":
        abbreviation_table = table
        break

def test_table_exists():
    assert abbreviation_table != None, "acronym table not found"

def test_doc_acronyms():
    read_acronyms = get_all_acronyms(path)
    actual_acronyms = ["TLA", "FLA", "SLA"]

    assert set(read_acronyms) == set(actual_acronyms), "acronyms not read correctly in doc"

def test_table_acronyms():
    for row in get_text_for_table(abbreviation_table):
        if row[0].strip().lower() != "acronym":
            table_acronyms.append(row[0])
    actual_acronyms = ["TLA", "FLA"]

    assert set(table_acronyms) == set(actual_acronyms), "acronyms not read correctly from table"

def test_add_acronym():
    to_add_acronym = "ANA"
    to_add_desc = "A New Anagram"
    temp_path = r'tests/data/temp/test2_add.docx'
    copyfile(path, temp_path)

    document = Document(temp_path)
    document.add_paragraph("Testing an add of " + to_add_desc + " (" + to_add_acronym + ").")
    document.save(temp_path)

    new_read_acronyms = get_all_acronyms(temp_path)
    new_actual_acronyms = ["TLA", "FLA", "SLA", to_add_acronym]
    new_actual_table_acronyms = ["TLA", "FLA", to_add_acronym]

    assert set(new_read_acronyms) == set(new_actual_acronyms), "acronym not added correctly in doc"

    for table in document.tables:
        if table.cell(0, 0) != None and table.cell(0, 0).text.strip().lower() == "acronym":
            new_row = table.add_row()
            new_row.cells[0].text = to_add_acronym
            new_row.cells[1].text = to_add_desc
            break
    document.save(temp_path)

    new_table = None
    for table in get_docx_tables(temp_path):
        row = get_text_for_table(table)[0]
        if row[0].strip().lower() == "acronym":
            new_table = table
            break

    new_table_acronyms = []
    for row in get_text_for_table(new_table):
        if row[0].strip().lower() != "acronym":
            new_table_acronyms.append(row[0])

    assert set(new_table_acronyms) == set(new_actual_table_acronyms), "acronym not added correctly in table"

def test_remove_acronym():
    to_remove = "TLA"
    temp_path = r'tests/data/temp/test2_remove.docx'
    copyfile(path, temp_path)

    document = Document(temp_path)
    for para in document.paragraphs:
        para.text = para.text.replace(to_remove, "")
    document.save(temp_path)

    new_read_acronyms = get_all_acronyms(temp_path)
    new_actual_acronyms = ["FLA", "SLA"]
    new_actual_table_acronyms = ["FLA"]

    assert set(new_read_acronyms) == set(new_actual_acronyms), "acronym not removed correctly in doc"

    for table in document.tables:
        if table.cell(0, 0) != None and table.cell(0, 0).text.strip().lower() == "acronym":
            tbl = table._tbl
            for row in table.rows:
                if row.cells[0].text == to_remove:
                    tbl_row = row._tr
                    tbl.remove(tbl_row)
                    break
    document.save(temp_path)

    new_table = None
    for table in get_docx_tables(temp_path):
        row = get_text_for_table(table)[0]
        if row[0].strip().lower() == "acronym":
            new_table = table
            break

    new_table_acronyms = []
    for row in get_text_for_table(new_table):
        if row[0].strip().lower() != "acronym":
            new_table_acronyms.append(row[0])

    assert set(new_table_acronyms) == set(new_actual_table_acronyms), "acronym not removed correctly in table"

def test_processing():
    read_acronyms = get_all_acronyms(path)
    table_acronyms = []
    for row in get_text_for_table(abbreviation_table):
        if row[0].strip().lower() != "acronym":
            table_acronyms.append(row[0])

    temp_path = r'tests/data/temp/test2_process.docx'
    copyfile(path, temp_path)
    document = Document(temp_path)
    document.save(temp_path)

    for table in document.tables:
        if table.cell(0, 0) != None and table.cell(0, 0).text.strip().lower() == "acronym":
            for acronym in set(read_acronyms) - set(table_acronyms):
                new_row = table.add_row()
                new_row.cells[0].text = acronym
                new_row.cells[1].text = acronym
                break
    document.save(temp_path)

    new_table = None
    for table in get_docx_tables(temp_path):
        row = get_text_for_table(table)[0]
        if row[0].strip().lower() == "acronym":
            new_table = table
            break

    new_table_acronyms = []
    for row in get_text_for_table(new_table):
        if row[0].strip().lower() != "acronym":
            new_table_acronyms.append(row[0])

    assert set(new_table_acronyms) == set(read_acronyms), "document and table acronyms out of sync"
