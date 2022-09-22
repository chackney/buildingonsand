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

component_cursor = conn.cursor()
component_cursor.execute('select distinct "COMPONENT" from buildingonsand."RELEASES"')

all_components = component_cursor.fetchall()

support_dates = []
# The averages support date for the products. Not sure this is all that useful
average_length_of_support = []
# Shortest support date
shortest_support_dates = []
# Date when 2 products are out of support.
two_out_of_supports = []

support_dates_averages = []
for start_date in dates:

    total = 0;
    shortest_support_date = 999999
    second_shortest_support_date = 99999
    for component in all_components:
        data_row = {}
        query = 'select "COMPONENT","SOFTWARE_VERSION", "OSS_SUPPORT_END_DATE" from buildingonsand."RELEASES" \
        where "RELEASE_DATE" < \'{}\' \
        and "COMPONENT"=\'{}\' \
        order by string_to_array("SOFTWARE_VERSION", \'.\')::int[] desc \
        limit 1'.format(start_date, component[0])
        cursor2 = conn.cursor()
        cursor2.execute(query)
        support_date = cursor2.fetchone()

        days_support = support_date[2] - start_date.date()
        total += days_support.days
        if days_support.days < shortest_support_date:
            shortest_support_date = days_support.days
        if second_shortest_support_date > days_support.days > shortest_support_date:
            second_shortest_support_date = days_support.days

        data_row = {
            "Date": start_date,
            "Component": component[0],
            "Days Support": days_support.days,
            "version": support_date[1]
        }
        support_dates.append(data_row)

    data_average_support = {
        "Date": start_date,
        "Number of Days": total/len(all_components),
        "Type": "Average Length Of Support"
    }
    data_shortest_support = {
        "Date": start_date,
        "Number of Days": shortest_support_date,
        "Type": "Shortest Support"
    }
    data_two_support = {
        "Date": start_date,
        "Number of Days": second_shortest_support_date,
        "Type": "Two Out of Support"
    }

    average_length_of_support.append(total/len(all_components))
    shortest_support_dates.append(shortest_support_date)
    two_out_of_supports.append(second_shortest_support_date)
    support_dates_averages.append(data_average_support)
    support_dates_averages.append(data_shortest_support)
    support_dates_averages.append(data_two_support)

# Plot Date against Time until support runs out.
# date vs support_date - date
# Bar plot

# release_df = pd.DataFrame(dict(product=products * len(release_date), release_date=release_date))
#
# fig = px.scatter(release_df, x="release_date", y="product",text=release_text)
#
# fig.show(text_position="bottom center")

support_dates_all = pd.DataFrame(support_dates)

print(average_length_of_support)
print(shortest_support_dates)
print(two_out_of_supports)

# fig = px.bar(df, x="medal", y="count", color="nation", text="nation")

fig = px.bar(support_dates_all, x='Date', y='Days Support', color="Component", barmode='group', text="version", title="Days of OSS support, based on start date of sample project")
fig.update()
fig.show()

# Line graph showing average, shortest, two_out of support

# fig = px.bar(support_dates_all, x='Date', y='Days Support', color="Component", barmode='group', text="version")
# fig.show()
support_averages = pd.DataFrame(support_dates_averages)
print(support_averages)
# df = pd.pivot(support_averages, index='Date', columns='player', values='points')
fig2 = px.line(support_averages, x="Date", y="Number of Days", color="Type", markers=True, title="OSS Support days combined")
fig2.show()
