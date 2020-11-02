import csv
from dataclasses import dataclass
import plotly.express as px


with open('C:/Users/mengh/Desktop/csc110/FINAL PROJECT/dataset/GHG.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
    GHG_lst = []
    for row in reader:
        if count == 29:
            break
        GHG_lst.append(row)
        count +=1 

#sea level data processing
with open('C:/Users/mengh/Desktop/csc110/FINAL PROJECT/dataset/sea_levels.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    sea_level = []
    for row in reader:
        sea_level.append(row)

sea_level = sea_level[5:]

sea_mapping = {}
year_map = {}
year_label = '#title = mean sea level anomaly global ocean (66S to 66N) (Annual signals retained) '
for row in sea_level:
    year = int(float(row[year_label]))
    mean = sum([float(num) for num in row[None] if num != ''])
    if year in year_map:
        year_map[year] = year_map[year] + 1
    else:
        year_map[year] = 1

    if year in sea_mapping:
        sea_mapping[year] = sea_mapping[year] + mean
    else:
        sea_mapping[year] = mean

# averaging out data
for y in year_map:
    sea_mapping[y] = sea_mapping[y] / year_map[y]


GHG_map = {}
for row in GHG_lst:
    GHG_map[int(row['Year'])] = float(row['N2O'])

x_values = list(range(1992, 2019))
x = [GHG_map[year] for year in x_values]
y = [sea_mapping[year] for year in x_values]

fig = px.scatter(x=x, y=y)
fig.show()
