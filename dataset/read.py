import csv
from dataclasses import dataclass
import plotly.express as px

@dataclass
class GreenhouseGas:
    """ dataclass representing greenhouse gas emissions of a province in a given year

    Instance Attributes:
        - year: year of the given data
        - region: province/territory of the given data
        - CO2: amount of CO2 emissions in the given year for the given province
        - CH4: amount of CH4 emissions in the given year for the given province
        - HPCs: amount of HPC emissions in the given year for the given province
        - PFCs: amount of PFC emissions in the given year for the given province
        - SF6: amount of SF6 emissions in the given year for the given province
        - NF3: amount of NF3 emissions in the given year for the given province
        - total: the total amount of greenhouse gas emissions in data
    """
    year: int
    region: str
    CO2: float
    CH4: float
    N2O: float
    HFCs: float
    PFCs: float
    SF6: float
    NF3: float
    total: float


with open('C:/Users/mengh/Desktop/csc110/FINAL PROJECT/dataset/GHG.csv') as csvfile:
    reader = csv.reader(csvfile)
    count = 0
    ghg_lst = []
    ghg_headers = next(reader)
    for row in reader:
        if count == 29:
            break

        ghg_lst.append(GreenhouseGas(year=int(row[0]),
                                      region=row[1],
                                      CO2=float(row[5]),
                                      CH4=float(row[6]),
                                      N2O=float(row[8]),
                                      HFCs=float(row[10]),
                                      PFCs=float(row[11]),
                                      SF6=float(row[12]),
                                      NF3=float(row[13]),
                                      total=float(row[14])))
        count +=1
ghg_lst = ghg_lst[2:]

#sea level data processing
with open('C:/Users/mengh/Desktop/csc110/FINAL PROJECT/dataset/sea_levels.csv') as csvfile:
    reader = csv.reader(csvfile)
    sea_level = []
    for row in reader:
        sea_level.append(row)

# removing headings
sea_level = sea_level[6:]

sea_mapping = {}
year_mapping = {}
for row in sea_level:
    year = int(float(row[0]))
    mean = sum([float(num) for num in row[1:] if num != '']) / (4 - row[1:].count(''))
    
    if year in year_mapping:
        year_mapping[year] = year_mapping[year] + 1
    else:
        year_mapping[year] = 1

    if year in sea_mapping:
        sea_mapping[year] = sea_mapping[year] + mean
    else:
        sea_mapping[year] = mean


# averaging out data
for y in year_mapping:
    sea_mapping[y] = sea_mapping[y] / year_mapping[y]

# sorting the data by greenhouse gas and region
CO2_alberta = [year.CO2 for year in ghg_lst if year.region == 'Alberta']
CH4_alberta = [year.CH4 for year in ghg_lst if year.region == 'Alberta']
N2O_alberta = [year.N2O for year in ghg_lst if year.region == 'Alberta']
HFC_alberta = [year.HFCs for year in ghg_lst if year.region == 'Alberta']
PFC_alberta = [year.PFCs for year in ghg_lst if year.region == 'Alberta']
SF6_alberta = [year.SF6 for year in ghg_lst if year.region == 'Alberta']
NF3_alberta = [year.NF3 for year in ghg_lst if year.region == 'Alberta']
total_alberta = [year.total for year in ghg_lst if year.region == 'Alberta']

y = [sea_mapping[year] for year in range(1992, 2019)]

fig = px.scatter(x=total_alberta, y=y)
fig.show()
