import csv
import os
import PyPDF2
import re


def get_files():
    arr = os.listdir('pdf')
    arr.remove('.gitkeep')
    return arr

def get_name(text):
    str = re.search(r'Patient Name:(.*?)Patient ID:', text).group(1)
    str = re.sub(r'\\n', '', str)
    return str[2:-1]

def get_result(text):
    str = re.search(r'TEST RESULT:(.*?)REMARKS:', text).group(1)
    str = re.sub(r'\\n', '', str)
    return str[2:-2]

def get_collection_datetime(text):
    str = re.search(r'Date & Time of Specimen Collection:(.*?)Date & Time of Release of Result:', text).group(1)
    str = re.sub(r'\\n', '', str)
    return str[1:-1]

def get_release_datetime(text):
    str = re.search(r'Date & Time of Release of Result:(.*?)LABORATORY TEST RESULT', text).group(1)
    str = re.sub(r'\\n', '', str)
    return str[1:-1]

def get_agesex(text):
    str = re.search(r'Age/Sex\\n:(.*?)Date of Birth:', text).group(1)
    str = re.sub(r'\\n', '', str)
    return str[2:-1]

def get_birthdate(text):
    str = re.search(r'Date of Birth:(.*?)Date & Time Received:', text)
    if str is None:
        str = re.search(r'Date of Birth:(.*?)Date & \\nTime Received:', text)
    
    str = str.group(1)
    str = re.sub(r'\\n', '', str)
    return str[2:-3]

for file in get_files():
    file_obj = open('pdf/' + file, 'rb')
    reader = PyPDF2.PdfFileReader(file_obj)

    filename = os.path.splitext(file)[0] + '.csv'

    with open('results/' + filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['NAME', 
                                               'RESULT',
                                               'SPECIMEN COLLECTION DATE TIME',
                                               'RELEASE DATE TIME',
                                               'AGE',
                                               'SEX',
                                               'DATE OF BIRTH'])
        writer.writeheader()

        for x in range(reader.numPages):
            page_obj = reader.getPage(x)
            page_text = repr(page_obj.extractText())
            # print(page_text)
            
            name = get_name(page_text).upper()
            result = get_result(page_text)
            collection_datetime = get_collection_datetime(page_text)
            release_datetime = get_release_datetime(page_text)
            age_sex = get_agesex(page_text)
            age = age_sex.split('/')[0]
            sex = age_sex.split('/')[1]
            birthdate = get_birthdate(page_text)

            print('Name: ' + name)                  
            print('Result: ' + result)
            print('Collection Date Time: ' + collection_datetime)  
            print('Release Date Time: ' + release_datetime)
            print('Age: ' + age)
            print('Sex: ' + sex)
            print('Date of Birth: ' + birthdate)
            print('\n')

            writer.writerow({'NAME': name, 
                             'RESULT': result,
                             'SPECIMEN COLLECTION DATE TIME': collection_datetime,
                             'RELEASE DATE TIME': release_datetime,
                             'AGE': age,
                             'SEX': sex,
                             'DATE OF BIRTH': birthdate})
        
        f.close()
 