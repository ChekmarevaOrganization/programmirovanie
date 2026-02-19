from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from docx import Document
from Levenshtein import distance
import logging
from datetime import datetime
logging.basicConfig(level=logging.INFO, filename="my_log.logg",filemode="w",  format="%(asctime)s %(levelname)s %(message)s")

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)

text1 = extract_text_from_docx('text1.docx')
text2 = extract_text_from_docx('text2.docx')

time_1 = datetime.now().strftime("%H:%M:%S:%f")
print("Начало levenstein",time_1)
def levenstein(str_1, str_2):
    logging.info(f"Starting the cycle levinstein")
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]
logging.info(f"The end of the cycle levinstein")
time_2= datetime.now().strftime("%H:%M:%S:%f")
print(levenstein(text1, text2))
print("Конец levinstein: ",time_2)


time_3 = datetime.now().strftime("%H:%M:%S:%f")
print("Начало fuzzywuzzy",time_3)
logging.info(f"Starting the cycle fuzzywuzzy")
a = fuzz.ratio(text1, text2)
print(a)
logging.info(f"The end of the cycle fuzzywuzzy")
time_4 = datetime.now().strftime("%H:%M:%S:%f")
print("Конец fuzzywuzzy: ",time_4)

a = fuzz.partial_ratio(text1, text2)
print(a)

a = fuzz.token_set_ratio(text1, text2)
print(a)

a = fuzz.WRatio(text1, text2)
print(a)


time_5 = datetime.now().strftime("%H:%M:%S:%f")
print("Начало distance",time_5)
logging.info(f"Starting the cycle distance")
print(distance(text1, text2))
logging.info(f"The end of the cycle distance")
time_6 = datetime.now().strftime("%H:%M:%S:%f")
print("Конец distance: ",time_6)
