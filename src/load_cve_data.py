import psycopg2
import json
import csv
import os
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    database="buildingonsand",
    user="buildingonsand",
    password="")


conn.cursor().execute('delete  from buildingonsand."RELEASE_CVE" where COMPONENT="SPRING-BOOT"')
conn.commit()


def load_cve_data():
    files = os.listdir('data/cves/spring')
    for file in files:
        file_name = file.strip('spring_boot_').strip('.json')
        f = open('data/cves/spring/' + file,'r')
        json_file = json.load(f)
        print(file)
        if 'vulnerable' in json_file:
            vunerable = json_file['vulnerable']
            for key in vunerable.keys():
                vunerabilites = vunerable[key]['vulnerabilities']
                release_version = file_name.strip('SPRING-BOOT-v').strip("_RELEASE").replace('_', '.')
                for vun in vunerabilites:
                    year = vun['id'].split('-')[1]
                    id = key + '_' + vun['id']
                    cve = vun['cve'] if 'cve' in vun else ''
                    sql = "INSERT INTO buildingonsand.\"RELEASE_CVE\" (\"ID\", \"RELEASE_NAME\",\"CVE\", \"TITLE\", \"DESCRIPTION\", \"CVSS_SCORE\", \"CWE\", \"REFERENCE\",\"YEAR\",\"SONAR_TYPE_ID\",\"COMPONENT\",\"RELEASE\") values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    print(sql)
                    conn.cursor().execute(sql,(id,file_name,cve,vun['title'],vun['description'],vun['cvssScore'],vun['cwe'],vun['reference'],year,vun['id'],'SPRING-BOOT',release_version))
                    conn.commit()


load_cve_data()
