import csv
import os
import requests
import re

fur_directory = 'D:\Faks\Projektna_analiza_podatkov\Analiza-Furryjev'
content_filename = 'rawr_data.html'
test_filename = 'test.html'

def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        content = file_in.read()
    return content

def page_to_furs(page_content):

    pattern = re.compile(r'border="0" width="120" height="120" alt=(.*?)align="middle', re.DOTALL)

    furs = [m.group(1) for m in re.finditer(pattern, page_content)]

    return furs

def get_dict_from_fur(fur):
    
    pattern = re.compile(r'(?P<Ime>.*?)></a><.*?viewsuit&amp;id=(?P<Id>\d\d*\d*\d*)"', re.DOTALL)

    match = re.search(pattern, fur)

    slovar = match.groupdict() if match is not None else None

    return slovar

def furs_from_file(directory, filename):
    content = read_file_to_string(directory, filename)
    furs = page_to_furs(content)
    slovarji = [get_dict_from_fur(fur) for fur in furs if fur is not None]

    return slovarji

slovar = furs_from_file(fur_directory, content_filename)