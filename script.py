import pandas as pd
import requests
import os
import sys
import sqlite3
from datetime import datetime
import json

agg_errors_data = []
urls = []

path = sys.argv[1]
file = path
#file = 'resourses/raw_data.xlsx'

xl = pd.read_excel(file)
xl_fetch_true = xl[xl['fetch']==1]


def data_list(response, url, r_time, list=[]):
    ts = response.headers['date']
    status_code = response.status_code
    label = xl[xl['url']==url]['label'].values[0]

    if status_code == 200:
        content_length = response.headers['Content-Length']
    else:
        content_length = None

    urls.append((ts, url, label, r_time, status_code, content_length))


for url in xl_fetch_true['url']:
    try:
        response = requests.get(url)
        r_time = response.elapsed.microseconds
        data_list(response, url, r_time)
    except:
        tb = sys.exc_info()
        now = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
        agg_errors_data.append({
                        		 "timestamp": now,
                        		 "url": url,
                        	     "error": {
                        		       "exception_type": str(tb[0]),
                        		       "exception_value": str(tb[1]),
                        		       "stack_info": str(tb[2])
                    		     }
                                })

        with open('errors.json', 'w') as file:
            json.dump(agg_errors_data, file, indent=2, ensure_ascii=False)


conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS monitoring
                  (ts DATETIME NOT NULL,
	               url TEXT NOT NULL,
	               label TEXT NOT NULL,
	               response_time FLOAT,
	               status_code INTEGER DEFAULT NULL,
	               CONTENT_LENGTH INTEGER DEFAULT NULL)"""
                )

cursor.executemany("INSERT INTO monitoring VALUES (?,?,?,?,?,?)", urls)
conn.commit()
conn.close()

for i in agg_errors_data:
    sys.stdout.write(str(i))
