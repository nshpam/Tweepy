import re
from unidecode import unidecode

temp_dict = {}
temp_text = ''
regex = re.compile('[^a-zA-Z0-9_\-]')

raw_text = "This is some ◡̈ text that we want to process กกกกก."

for list_word in raw_text.split():

    temp_dict[list_word] = [word.encode('ascii', 'namereplace').decode('utf-8').split('\\N') for word in list_word.split()]

    for word in temp_dict[list_word]:
        if word == '':
            continue

        list_word = regex.sub('', list_word)
        
        if 'THAI' not in list_word and unidecode(list_word).isalnum():
            temp_text += ' ' + unidecode(list_word)

print(temp_text.strip())
