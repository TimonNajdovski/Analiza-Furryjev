import csv
import os
import requests
import re

main_directory = 'D:\Faks\Projektna_analiza_podatkov'
fursuit_directory = 'D:\Faks\Projektna_analiza_podatkov\Fursuits'
owner_directory = 'D:\Faks\Projektna_analiza_podatkov\Owo-ners'
main_filename = 'rawr_data.html'
csv_filename ='furs_podatki'

def get_page_initial(directory, filename):
    """Funkcija naloži vsebino glavne spletne strani in jo shrani"""
    try:
        url = 'https://db.fursuit.me/index.php?c=browse&searchtype=Fursuits&fursuit_name=&fursuit_gender=&fursuit_location=&user_gender=&user_country=&fursuit_performing=&fursuit_partial=&fursuit_toonyness_greater=&fursuit_age_greater=&fursuit_toonyness_less=&fursuit_age_less=&suitlist_limit=0&suitlist_start=0'
        r = requests.get(url)
        page_content = r.text
    except ConnectionError:
        return None

    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(page_content)    
        

def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        content = file_in.read()
    return content

def page_to_furs(page_content):
    """Funkcija razdeli glavni html na posamezne fursuite"""
    pattern = re.compile(r'class="browsecelltitle" width="120"><a href=".c=viewsuit&amp;id=(.*?)cellpadding="2" ><tr><td', re.DOTALL)

    furs = [m.group(1) for m in re.finditer(pattern, page_content)]
    return furs

def get_dict_from_fur(fur):
    """Funkcija za posamezen fursuit vrne slovar z imenom uporabnika in identifikacijsko številko fursuita"""

    pattern = re.compile(r'(?P<Id>\d*\d*\d*\d)"'
                        r'.*?href=".c=viewuser&amp;nick=(?P<Owner>.*?)" title=', re.DOTALL)

    match = re.search(pattern, fur)

    slovar = match.groupdict() if match is not None else None
    return slovar

def furs_from_file(directory, filename):
    """Funkcija sestavi seznam imen in Id številk"""
    content = read_file_to_string(directory, filename)
    furs = page_to_furs(content)
    slovarji = [get_dict_from_fur(fur) for fur in furs if fur is not None]

    return slovarji    

def fursuit_more_data(Id):
    """Funkcija naloži stran fursuita z določeno Id številko"""
    try:
        url = 'https://db.fursuit.me/index.php?c=viewsuit&id=' + Id
        r = requests.get(url)
        page_content = r.text
    except ConnectionError:
        return None
    return page_content

def owner_more_data(name):
    """Funkcija naloži stran uporabnika z določenim imenom"""
    name = '+'.join(name.split(' '))
    try:
        url = 'https://db.fursuit.me/index.php?c=viewuser&nick=' + name
        r = requests.get(url)
        page_content = r.text
    except ConnectionError:
        return None
    return page_content

def save_furs_to_file(directory_furs, directory_owo, slovarji_in):
    """Funkcija naloži in v ločeni datoteki shrani strani vseh uporabnikov ter fursuitov"""
    for fur in slovarji_in:
        Id = fur['Id']
        path1 = os.path.join(directory_furs, Id)
        content = fursuit_more_data(Id)
        with open(path1, 'w', encoding='utf-8') as file_out:
            file_out.write(content)
        
        Owner = fur['Owner']
        path2 = os.path.join(directory_owo, Owner)
        content = owner_more_data(Owner)
        with open(path2, 'w', encoding='utf-8') as file_out:
            file_out.write(content)

    return None

def get_fursuit_dict(fur):
    """Funkcija iz strani fursuita sestavi slovar z dodatnimi podatki"""
    pattern = re.compile(r'Fursuit Name:</td> <td class="input">(?P<Name>.*?)</td> </tr>'
                        r'.*?Added:</td> <td class="input">(?P<Date_Fursuit_Added>.*?)</td> </tr>'
                        r'.*?Fursuits whose species is :  (?P<Species>.*?)" title="'
                        r'.*?Fursuits with gender :  (?P<Fur_Gender>.*?)" title="Search', re.DOTALL)
    
    match = re.search(pattern, fur)

    slovar = match.groupdict() if match is not None else None

    return slovar

def get_owner_dict(owner):
    """Funkcija iz strani uporabnika sestavi slovar z dodatnimi podatki"""
    pattern = re.compile(r'title="Search for Users with gender:  (?P<Owner_Gender>.*?)">'
                        r'.*?</td> <td class="input" title="YYYY-MM-DD">(?P<Birthday>.*?)</td> </tr>'
                        r'.*?>Added:</td> <td class="input" title="YYYY-MM-DD">(?P<Date_Account_Added>(\d\d\d\d-\d\d-\d\d)?).*?</td> </tr>'
                        r'.*?;text=Users living in country:  (?P<Country>.*?)"', re.DOTALL)

    match = re.search(pattern, owner)

    slovar = match.groupdict() if match is not None else None

    return slovar

def furs_from_file_main(directory_furs, directory_owo, slovarji_in):
    """Funckija sestavi seznam slovarjev s podatki vseh fursuitov in njihovih lastnikov"""
    slovarji_out = []
    for fur in slovarji_in:
        Id = fur['Id']
        content = read_file_to_string(directory_furs, Id)
        slovar1 = get_fursuit_dict(content)

        owner = fur['Owner']
        content = read_file_to_string(directory_owo, owner)
        slovar2 = get_owner_dict(content)

        slovar1.update(slovar2)
        slovarji_out.append(slovar1)
    
    return slovarji_out

def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return

def write_furs_to_csv(furs, directory, filename):
    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
    parametroma "directory"/"filename". Funkcija predpostavi, da so ključi vseh
    slovarjev parametra ads enaki in je seznam ads neprazen."""
    
    assert furs and (all(j.keys() == furs[0].keys() for j in furs))
    write_csv(furs[0].keys(), furs, directory, filename)

def main(redownload=False, reparse=True):
    """Funkcija izvede celoten del pridobivanja podatkov"""

    
    # Najprej v lokalno datoteko shranimo glavno stran
    if redownload:
        get_page_initial(main_directory, main_filename)
        slovarji_in = furs_from_file(main_directory, main_filename)
        save_furs_to_file(fursuit_directory, owner_directory, slovarji_in)
    
    # Podatke prebermo v lepšo obliko (seznam slovarjev)
    if reparse:
        slovarji_in = furs_from_file(main_directory, main_filename)
        furs = furs_from_file_main(fursuit_directory, owner_directory, slovarji_in)
        #Cleanup
        furs = [fur for fur in furs if fur is not None]

    # Podatke shranimo v csv datoteko
        write_furs_to_csv(furs, main_directory, csv_filename)