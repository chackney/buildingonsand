import psycopg2
import json
import fileinput
import os

conn = psycopg2.connect(
    host="localhost",
    database="buildingonsand",
    user="buildingonsand",
    password="")

# Load Versions
query = 'select "RELEASE_ID" from buildingonsand."RELEASES" \
        where "COMPONENT"=\'{}\' \
        order by string_to_array("SOFTWARE_VERSION", \'.\')::int[] desc '.format('SPRING-BOOT')
cursor2 = conn.cursor()
cursor2.execute(query)
#TODO change this to something else
versions = cursor2.fetchall()
last_version = '2.7.3'

# Change pom Version
for version in versions:
    this_version = version[0].strip('SPRING-BOOT-v')
    with fileinput.FileInput('../sand/pom.xml',
                             inplace = True, backup ='.bak') as f:
        for line in f:
            if '<version>' + last_version + '</version>' in line:
                print('<version>' + this_version + '</version>',
                      end ='\n')
            else:
                print(line, end ='')
    last_version = this_version
    # run mvn goal

    os.chdir('../sand')
    #os.system('mvn  clean package')
    os.system('mvn -s settings.xml ossindex:audit -Dossindex.reportFile=target/out.json')
    # build docker file
    # os.system('docker build . -t totest:app')

    versions_underscores = version[0].replace('.','_')

    # run Trivvy
    #os.system('trivy  image  totest:app > target/trivy.out ')

    # Collect results
    os.system('pwd')
    os.system("mv target/out.json ../src/data/cves/spring_boot_" + versions_underscores + ".json")
    #os.system("mv target/trivy.out ../src/data/cves/trivy_" + versions_underscores + ".json")

    # with open('target/out.json', 'r') as f:
    #     spring_boot_cves = json.load(f)
    #     print(spring_boot_cves)
    #
    # with open('trivy.out', 'r') as f:
    #     trivy_scan = f.readlines()
    #     print(trivy_scan)
