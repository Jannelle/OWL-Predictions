import sqlite3
import pandas as pd
conn = sqlite3.connect('owl.db')
c = conn.cursor()

#Creating a database from the CSVs
# for i in range(1, 21):
#     week.to_csv('Week' + str(i) + '.csv')

x = pd.read_csv('week1.csv')
print(x.head())

print(2)