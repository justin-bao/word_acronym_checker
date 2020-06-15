#!/usr/bin/env python3

from word_acronym_checker import *
from shutil import copyfile
import pytest
import os

path = "tests/data/test4_invalid.docx"
temp_dir = "tests/data/temp/"
actual_doc_acronyms = ["TLA", "FLA", "SLA"]
actual_table_acronyms = []

def test_table_exists():
    temp_path = temp_dir + "test4_create.docx"
    copyfile(path, temp_path)
    assert get_acronym_table(temp_path) == None, "acronym table found but doesn't exist yet"
    create_acronym_table(temp_path)
    assert get_acronym_table(temp_path) != None, "acronym table not found"

    if os.path.exists(temp_path):
        os.remove(temp_path)
    else:
        print("The file does not exist")

def test_doc_acronyms():
    read_acronyms = get_all_acronyms(path)
    assert set(read_acronyms) == set(actual_doc_acronyms), "acronyms not read correctly in doc"

def test_table_acronyms():
    temp_path = temp_dir + "test4_table.docx"
    copyfile(path, temp_path)
    create_acronym_table(temp_path)
    table_acronyms = get_table_acronyms(temp_path)
    assert set(table_acronyms) == set(actual_table_acronyms), "acronyms not read correctly from table"

    if os.path.exists(temp_path):
        os.remove(temp_path)
    else:
        print("The file does not exist")

def test_add_acronym():
    to_add_acronym = "ANA"
    to_add_desc = "A New Acronym"
    temp_path = temp_dir + "test4_add.docx"
    copyfile(path, temp_path)
    create_acronym_table(temp_path)

    document = Document(temp_path)
    document.add_paragraph("Testing an add of " + to_add_desc + " (" + to_add_acronym + ").")
    document.save(temp_path)

    new_read_acronyms = get_all_acronyms(temp_path)
    new_actual_acronyms = actual_doc_acronyms.copy()
    new_actual_acronyms.append(to_add_acronym)
    new_actual_table_acronyms = actual_table_acronyms.copy()
    new_actual_table_acronyms.append(to_add_acronym)

    assert set(new_read_acronyms) == set(new_actual_acronyms), "acronym not added correctly in doc"

    get_acronym_table(temp_path)
    add_table_row(temp_path, to_add_acronym, to_add_desc)

    new_table_acronyms = get_table_acronyms(temp_path)

    assert set(new_table_acronyms) == set(new_actual_table_acronyms), "acronym not added correctly in table"

    if os.path.exists(temp_path):
        os.remove(temp_path)
    else:
        print("The file does not exist")

def test_remove_acronym():
    to_remove = "TLA"
    temp_path = temp_dir + "test4_remove.docx"
    copyfile(path, temp_path)
    create_acronym_table(temp_path)

    document = Document(temp_path)
    for para in document.paragraphs:
        para.text = para.text.replace(to_remove, "")
    document.save(temp_path)

    new_read_acronyms = get_all_acronyms(temp_path)
    new_actual_acronyms = actual_doc_acronyms.copy()
    new_actual_acronyms.remove(to_remove)
    new_actual_table_acronyms = actual_table_acronyms.copy()

    assert set(new_read_acronyms) == set(new_actual_acronyms), "acronym not removed correctly in doc"

    get_acronym_table(temp_path)
    remove_table_row(temp_path, to_remove)

    new_table_acronyms = get_table_acronyms(temp_path)

    assert set(new_table_acronyms) == set(new_actual_table_acronyms), "acronym not removed correctly in table"

    if os.path.exists(temp_path):
        os.remove(temp_path)
    else:
        print("The file does not exist")

def test_processing():
    temp_path = temp_dir + "test4_process.docx"
    copyfile(path, temp_path)
    create_acronym_table(temp_path)
    document = Document(temp_path)
    document.save(temp_path)

    read_acronyms = get_all_acronyms(temp_path)
    process(temp_path)

    new_table_acronyms = get_table_acronyms(temp_path)

    assert set(new_table_acronyms) == set(read_acronyms), "document and table acronyms out of sync"

    if os.path.exists(temp_path):
        os.remove(temp_path)
    else:
        print("The file does not exist")
