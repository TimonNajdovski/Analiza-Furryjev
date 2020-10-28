import csv
import os
import requests
import re

main_directory = 'D:\Faks\Projektna_analiza_podatkov\Analiza-Furryjev'
fursuit_directory = 'D:\Faks\Projektna_analiza_podatkov\Analiza-Furryjev\Fursuits'
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

slovarji_in = furs_from_file(main_directory, content_filename)    

def fur_more_data(Id):
    try:
        url = 'https://db.fursuit.me/index.php?c=viewsuit&id=' + Id
        r = requests.get(url)
        page_content = r.text
    except ConnectionError:
        return None
    return page_content

def save_furs_to_file(directory, filename):
    for fur in slovarji_in:
        Id = fur['Id']
        path = os.path.join(directory, Id)
        content = fur_more_data(Id)
        
        with open(path, 'w', encoding='utf-8') as file_out:
            file_out.write(content)
        
    return None

def get_fursuit_data(fur):
    
    pattern = re.compile(r'Fursuit Name:</td> <td class="input">(?P<Name>.*?)</td> </tr>'
                        r'.*?Added:</td> <td class="input">(?P<Date>.*?)</td> </tr>'
                        r'.*?Fursuits whose species is :  (?P<Species>.*?)" title="'
                        r'.*?Fursuits with gender :  (?P<Fur_Gender>.*?)" title="Search', re.DOTALL)
    
    match = re.search(pattern, fur)

    slovar = match.groupdict() if match is not None else None

    return slovar

def fursuits_from_file(directory):
    slovarji_out = []
    for fur in slovarji_in:
        Id = fur['Id']
        content = read_file_to_string(directory, Id)
        slovar = get_fursuit_data(content)
        slovarji_out.append(slovar)
        slovar['Owner'] = fur['Ime']
        print(slovar)
    return slovarji_out

slovarji = fursuits_from_file(fursuit_directory)