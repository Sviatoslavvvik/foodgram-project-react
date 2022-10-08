import csv
import datetime
import os
from pathlib import Path

import psycopg2

connection = psycopg2.connect("host=127.0.0.1 dbname=foodgram user=postgres password=Sayanogorsk1992")
cur = connection.cursor()
cur.execute('SELECT * FROM recipes_ingridient')
# with open(r"C:\!Dev\foodgram-project-react\data\ingredients.csv", 'r', encoding='UTF-8') as csv_file:
    
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     header = next(csv_reader)
#     i=0
#     for row in csv_reader:
#         i+=1
#         cur.execute("INSERT INTO recipes_ingridient VALUES (%s, %s, %s)", (i, row[0], row[1])
#     )
# connection.commit()
#connection.close()
