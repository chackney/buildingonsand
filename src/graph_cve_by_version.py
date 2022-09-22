import plotly.express as px
import pandas as pd
import psycopg2
import datetime

# initializing date - Set Date where we have the last data
test_date = datetime.datetime(2022, 6, 1)

dates = []
# Set last 48 months
for x in range(36):
    test_date += datetime.timedelta(days=-30)
    dates.append(test_date)


conn = psycopg2.connect(
    host="localhost",
    database="buildingonsand",
    user="buildingonsand",
    password="")

query = 'select "RELEASE" , count("RELEASE"), "YEAR" from  buildingonsand."RELEASE_CVE" \
            group by "RELEASE", "YEAR" \
            order by string_to_array("RELEASE", \'.\')::int[] asc'

cursor2 = conn.cursor()
cursor2.execute(query)
cves_by_year = cursor2.fetchall()


for component in ['SPRING-BOOT', 'REACT']:

    cursor3 = conn.cursor()
    cursor3.execute('select "COMPONENT","SOFTWARE_VERSION", "OSS_SUPPORT_END_DATE", "RELEASE_DATE" from buildingonsand."RELEASES" where "COMPONENT"= %s' , [component])
    version_dates = cursor3.fetchall();

    print(cves_by_year)

    df_dates = pd.DataFrame(version_dates,columns=['Component','Release','End Date', 'Release Date'])
    df = pd.DataFrame(cves_by_year, columns=['Release', 'Number', 'Year'])
    print(df)
    df2 = pd.merge(df, df_dates, on = "Release", how = "inner")
    print(df2)
    df2['Days Support'] = df2['End Date'] - df2['Release Date']

    df2.sort_values(by=['Release', 'Year'], inplace=True)

    print(df2)
    fig = px.bar(df2, x="Release", y="Number", color="Year", text="Year", title="{} CVE's per release (as of today, not release date) ".format(component))
    fig.show()



# fig = px.line(df, x="Year", y="Number", color='Release')
# fig.show()
# fig = px.bar(support_dates_all, x='Date', y='Days Support', color="Component", barmode='group', text="version")
# fig.show()

# fig = px.bar(support_dates_all, x='Date', y='Days Support', color="Component", barmode='group', text="version")
# fig.show()