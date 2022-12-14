import psycopg2
import json
import csv
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    database="buildingonsand",
    user="buildingonsand",
    password="")


cursor = conn.cursor()
conn.cursor().execute('delete  from buildingonsand."RELEASES"')
conn.commit()


def load_spring_data():
    f = open("data/spring_boot_releases.json", "r")
    spring_boot_releases = json.load(f)

    version_dates = {}
    with open('data/spring_support_dates.txt', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            version = row[0].strip('.x')
            dates = {"eofSupport": row[2], "eodCommercialSupport": row[3]}
            version_dates[version] = dates


    for item in spring_boot_releases:
        release_name = item['version']
        version_number = release_name
        if not (spring_invalid_versions(version_number)):
            if version_number.endswith('.RELEASE'):
                version_number = version_number.strip('.RELEASE')

            # The pre spring 2.0 release has dots in the wrong place.
            version_number = version_number.strip('v').strip('.')
            release_id = "SPRING-BOOT-" + item['version']
            if version_number:
                version_lookup = version_number[0:3]
                print("Looking up value {}", release_name)
                support_dates = version_dates[version_lookup]
                sql = "INSERT INTO buildingonsand.\"RELEASES\" (\"RELEASE_ID\",\"SOFTWARE_VERSION\", \"COMPONENT\", \"RELEASE_DATE\", \"OSS_SUPPORT_END_DATE\", \"SUPPORT_END_DATE\") values ('{}','{}','{}','{}','{}','{}')".format(release_id,version_number,'SPRING-BOOT',item['date'], support_dates['eofSupport'],support_dates['eodCommercialSupport'])
                print(sql)
                conn.component_cursor().execute(sql)
                conn.commit()


def load_react_data():
    f = open("data/react_releases.json", "r")
    react_releases = json.load(f)
    # React - Assume support ended when new version came out
    # Set initial date 1 year in the future
    last_release_version_date = datetime.now() + timedelta(days=365)
    last_major_version = 18
    previous_date = datetime.now()
    for item in react_releases:
        release_name = item['version']
        version_number = release_name.strip('v')

        if not (react_invalid_versions(version_number)):
            version_number = version_number.split('(')[0]

            # The pre spring 2.0 release has dots in the wrong place.
            version_number = version_number.strip('v').strip('.')
            release_id = "REACT-" + release_name

            if version_number:
                split = version_number.split('.')
                major_version = int(split[0]) if int(split[0]) != 0 else int(split[2])
                if major_version < last_major_version:
                    last_major_version = major_version
                    last_release_version_date = previous_date

                sql = "INSERT INTO buildingonsand.\"RELEASES\" (\"RELEASE_ID\",\"SOFTWARE_VERSION\", \"COMPONENT\", \"RELEASE_DATE\", \"OSS_SUPPORT_END_DATE\", \"SUPPORT_END_DATE\") values ('{}','{}','{}','{}','{}','{}')".format(release_id,version_number,'REACT',item['date'], last_release_version_date, last_release_version_date)
                print(sql)
                conn.component_cursor().execute(sql)
                conn.commit()

                previous_date = item['date']



def spring_invalid_versions(version_number):
    return (version_number.__contains__('M') | version_number.__contains__('RC'))

def react_invalid_versions(version_number):
    return (version_number.__contains__('alpha') | version_number.__contains__('RC'))
## Load Alpine Data:

def load_alpine_data():

    with open('data/alpine.txt', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        previous_release_date = '2024-05-23'
        for row in reader:
            print(row)
            # alpine_releases = row[3].split("|")
            # for alpine_release in alpine_releases:
            #     striped_release = alpine_release.strip()
            #     if !striped_release.endswith('-stable'):
            #         alpine_releases_by_version[striped_release] = {}

            alpine_release = row[0]
            alpine_striped = alpine_release.strip('v')

            release_id = 'ALPINE_' + alpine_release
            sql = "INSERT INTO buildingonsand.\"RELEASES\" (\"RELEASE_ID\",\"SOFTWARE_VERSION\", \"COMPONENT\", \"RELEASE_DATE\", \"OSS_SUPPORT_END_DATE\", \"SUPPORT_END_DATE\") values ('{}','{}','{}','{}','{}','{}')".format(release_id,alpine_striped,'ALPINE',row[1], previous_release_date, row[3])
            print(sql)
            conn.component_cursor().execute(sql)
            conn.commit()
            previous_release_date = row[1]

def load_k8s_data():
    f = open("data/kubernetes_releases.json", "r")
    kube_releases = json.load(f)

    version_dates = {}
    with open('data/kubernetes_support_data.txt', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            dates = {"eofSupport": row[2], "eodCommercialSupport": row[2]}
            version_dates[row[0]] = dates


    for item in kube_releases:
        release_name = item['version']
        version_number = release_name.strip("Kubernetes v")
        version_number = version_number.strip("Release v")
        print(item['date'])
        date = datetime.strptime(item['date'],'%Y-%m-%dT%H:%M:%SZ')
        first_date = datetime(2016, 3, 16)
        if not (version_number.__contains__('RC') \
                | version_number.__contains__('-') \
                | ( date < first_date)):
            release_id = "KUBERNETES-" + item['version']
            if version_number:
                split = version_number.split('.')
                version_lookup = split[0] + '.' + split[1]
                print("Looking up value {}", version_lookup)
                support_dates = version_dates[version_lookup]
                sql = "INSERT INTO buildingonsand.\"RELEASES\" (\"RELEASE_ID\",\"SOFTWARE_VERSION\", \"COMPONENT\", \"RELEASE_DATE\", \"OSS_SUPPORT_END_DATE\", \"SUPPORT_END_DATE\") values ('{}','{}','{}','{}','{}','{}')".format(release_id,version_number,'KUBERNETES',item['date'], support_dates['eofSupport'],support_dates['eodCommercialSupport'])
                print(sql)
                conn.component_cursor().execute(sql)
                conn.commit()


load_spring_data()
load_alpine_data()
load_k8s_data()
load_react_data()