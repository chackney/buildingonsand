import requests
import psycopg2

username = ''
password = ''
def cves(data):
    return requests.post('https://ossindex.sonatype.org/api/v3/component-report',
                         headers={'Accept': 'application/vnd.ossindex.component-report.v1+json'
                             ,'Content-Type': 'application/vnd.ossindex.component-report-request.v1+json'},
                         auth=(username,password),
                         data=data)
def format_pkg(pkg,version):
    return '{ \
    "coordinates": [ \
        "pkg:npm/' + pkg + '@' + version + '" \
    ] }'


conn = psycopg2.connect(
    host="localhost",
    database="buildingonsand",
    user="buildingonsand",
    password="")


conn.cursor().execute('delete  from buildingonsand."RELEASE_CVE" where "COMPONENT"=\'REACT\'')
conn.commit()


query = 'select "SOFTWARE_VERSION" from buildingonsand."RELEASES" \
        where "COMPONENT"=\'{}\' \
        order by string_to_array("SOFTWARE_VERSION", \'.\')::int[] desc '.format('REACT')
cursor2 = conn.cursor()
cursor2.execute(query)
#TODO change this to something else
versions = cursor2.fetchall()

for version in versions:
    formatted_version = version[0].strip()
    response = cves(format_pkg("react", formatted_version))
    cve_payload = response.json()
    for payload in cve_payload:
        if 'vulnerabilities' in payload:
            vulnerabilities = payload['vulnerabilities']

            file_name = 'REACT_' + formatted_version
            for vun in vulnerabilities:
                year = vun['id'].split('-')[1]
                id = payload['coordinates'] + vun['id']
                cve = vun['cve'] if 'cve' in vun else ''
                sql = "INSERT INTO buildingonsand.\"RELEASE_CVE\" (\"ID\", \"RELEASE_NAME\",\"CVE\", \"TITLE\", \"DESCRIPTION\", \"CVSS_SCORE\", \"CWE\", \"REFERENCE\",\"YEAR\",\"SONAR_TYPE_ID\",\"COMPONENT\",\"RELEASE\") values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                print(sql)
                conn.cursor().execute(sql,(id,file_name,cve,vun['title'],vun['description'],vun['cvssScore'],vun['cwe'],vun['reference'],year,vun['id'],'REACT',formatted_version))
                conn.commit()






