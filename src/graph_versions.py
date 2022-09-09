import plotly.express as px
import pandas as pd
import psycopg2
import datetime

# initializing date
test_date = datetime.datetime(2022, 9, 1)

dates = []
for x in range(36):
    print(x)
    test_date += datetime.timedelta(days=-30)
    dates.append(test_date)

print(dates)

conn = psycopg2.connect(
    host="localhost",
    database="buildingonsand",
    user="buildingonsand",
    password="")

cursor = conn.cursor()
cursor.execute('select distinct "COMPONENT" from buildingonsand."RELEASES"')

result = cursor.fetchall()

results = []

for start_date in dates:

    for row in result:
        data_row = {}
        print(row[0])
        query = 'select "COMPONENT","SOFTWARE_VERSION", "OSS_SUPPORT_END_DATE" from buildingonsand."RELEASES" \
        where "RELEASE_DATE" < \'{}\' \
        and "COMPONENT"=\'{}\' \
        order by string_to_array("SOFTWARE_VERSION", \'.\')::int[] desc \
        limit 1'.format(start_date, row[0])
        cursor2 = conn.cursor()
        cursor2.execute(query)
        support_date = cursor2.fetchone()
        days_support = support_date[2] - start_date.date()
        print("{} {} {} ".format(start_date, support_date, days_support.days))

        data_row = {
            "Date": start_date,
            "Component": row[0],
            "Days Support": days_support.days
        }
        results.append(data_row);

# Plot Date against Time until support runs out.
# date vs support_date - date
# Bar plot

# release_df = pd.DataFrame(dict(product=products * len(release_date), release_date=release_date))
#
# fig = px.scatter(release_df, x="release_date", y="product",text=release_text)
#
# fig.show(text_position="bottom center")

df = pd.DataFrame(results)
print(df)
print(results)

fig = px.bar(df,x='Date', y='Days Support', color="Component", barmode='group')
fig.show()
