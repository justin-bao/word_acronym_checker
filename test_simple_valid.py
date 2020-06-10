#!/usr/bin/env python3

from word_acronym_checker import *
from word_table_reader import *
from word_acronym_reader import *
from shutil import copyfile
import pytest
import os

path = "tests/data/test1_valid.docx"
temp_dir = "tests/data/temp/"
actual_doc_acronyms = ["TLA", "FLA"]
actual_table_acronyms = ["TLA", "FLA"]

def test_table_exists():
    assert get_acronym_table(path) != None, "acronym table not found"

def test_doc_acronyms():
    read_acronyms = get_all_acronyms(path)
    assert set(read_acronyms) == set(actual_doc_acronyms), "acronyms not read correctly in doc"

def test_table_acronyms():
    table_acronyms = get_table_acronyms(path)
    assert set(table_acronyms) == set(actual_table_acronyms), "acronyms not read correctly from table"

def test_add_acronym():
    to_add_acronym = "ANA"
    to_add_desc = "A New Anagram"
    temp_path = temp_dir + "test1_add.docx"
    copyfile(path, temp_path)

    document = Document(temp_path)
    document.add_paragraph("Testing an add of " + to_add_desc + " (" + to_add_acronym + ").")
    document.save(temp_path)

    new_read_acronyms = get_all_acronyms(temp_path)
    new_actual_acronyms = actual_doc_acronyms.copy()
    new_actual_acronyms.append(to_add_acronym)

    assert set(new_read_acronyms) == set(new_actual_acronyms), "acronym not added correctly in doc"

    add_table_row(temp_path, to_add_acronym, to_add_desc)

    new_table_acronyms = get_table_acronyms(temp_path)

    if os.path.exists(temp_path):
        os.remove(temp_path)
    else:
        print("The file does not exist")

    assert set(new_table_acronyms) == set(new_actual_acronyms), "acronym not added correctly in table"

def test_remove_acronym():
    to_remove = "TLA"
    temp_path = temp_dir + "test1_remove.docx"
    copyfile(path, temp_path)

    document = Document(temp_path)
    for para in document.paragraphs:
        para.text = para.text.replace(to_remove, "")
    document.save(temp_path)

    new_read_acronyms = get_all_acronyms(temp_path)
    new_actual_acronyms = actual_doc_acronyms.copy()
    new_actual_acronyms.remove(to_remove)

    assert set(new_read_acronyms) == set(new_actual_acronyms), "acronym not removed correctly in doc"

    remove_table_row(temp_path, to_remove)

    new_table_acronyms = get_table_acronyms(temp_path)

    if os.path.exists(temp_path):
        os.remove(temp_path)
    else:
        print("The file does not exist")

    assert set(new_table_acronyms) == set(new_actual_acronyms), "acronym not removed correctly in table"

def test_processing():
    temp_path = temp_dir + "test1_process.docx"
    copyfile(path, temp_path)
    document = Document(temp_path)
    document.save(temp_path)

    read_acronyms = get_all_acronyms(temp_path)
    process(temp_path)

    new_table_acronyms = get_table_acronyms(temp_path)

    if os.path.exists(temp_path):
        os.remove(temp_path)
    else:
        print("The file does not exist")

    assert set(new_table_acronyms) == set(read_acronyms), "document and table acronyms out of sync"
