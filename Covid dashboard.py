from IPython.display import clear_output
import ipywidgets as wdg
import pandas as pd
import matplotlib.pyplot as plt
import json
from uk_covid19 import Cov19API

filters_1 = [
    'areaType=nation',
]
structure_1 = {
    'area': 'areaName',
    'date': 'date',
    'hospital': 'newAdmissions',
    'ventilator': 'covidOccupiedMVBeds'
}
api = Cov19API(filters=filters_1, structure=structure_1)
hospitalVentilator = api.get_json()
with open('hospitalVentilator.json', 'wt') as OUTF:
    json.dump(hospitalVentilator, OUTF)


def update_cov19api(button):
    filters_1 = [
        'areaType=nation',
    ]
    structure_1 = {
        'area': 'areaName',
        'date': 'date',
        'hospital': 'newAdmissions',
        'ventilator': 'covidOccupiedMVBeds'
    }
    api = Cov19API(filters=filters_1, structure=structure_1)
    hospitalVentilator = api.get_json()
    with open('hospitalVentilator.json', 'wt') as OUTF:
        json.dump(hospitalVentilator, OUTF)

    apibutton.icon = 'check'
    apibutton.disabled = True


apibutton = wdg.Button(
    description='Refresh',
    disabled=False,
    button_style='danger',
    tooltip='Update the latest Covid-19 data of new admissions and ventilators',
    icon='Download'
)
apibutton.on_click(update_cov19api)
with open('hospitalVentilator.json', 'rt') as INFILE:
    data = json.load(INFILE)
datalist = data['data']
England = []
Scotland = []
Northern_Ireland = []
Wales = []

for i in datalist:
    if i['area'] == 'England':
        England.append(i)
    elif i['area'] == 'Scotland':
        Scotland.append(i)
    elif i['area'] == 'Northern Ireland':
    Northern_Ireland.append(i)
    elif i['area'] == 'Wales':
    Wales.append(i)

dates = [dictionary['date'] for dictionary in datalist]
dates.sort()


def parse_date(datestring):
    return pd.to_datetime(datestring, format="%Y-%m-%d")


startDate = parse_date(dates[0])
endDate = parse_date(dates[-1])
index = pd.date_range(startDate, endDate, freq='D')
hospitalVentilator_df_E = pd.DataFrame(index=index, columns=['area', 'hospital', 'ventilator
                                                             hospitalVentilator_df_S = pd.DataFrame(index=index,
                                                                                                    columns=['area',
                                                                                                             'hospital',
                                                                                                             'ventilator
                                                                                                             hospitalVentilator_df_NI = pd.DataFrame(
    index=index, columns=['area', 'hospital', 'ventilato
                          hospitalVentilator_df_W = pd.DataFrame(index=index, columns=['area', 'hospital', 'ventilator


def df_fill(df, nation):
    for i in nation:
        date = parse_date(i['date'])
    for column in ['area', 'hospital', 'ventilator']:
        if pd.isna(df.loc[date, column]):
            value = i[column] if i[column] != None else 0.0
    df.loc[date, column] = value
    df.fillna(0.0, inplace=True)
    df.to_pickle('%s.pkl' % nation[0]['area'])


df_fill(hospitalVentilator_df_E, England)
df_fill(hospitalVentilator_df_S, Scotland)
df_fill(hospitalVentilator_df_NI, Northern_Ireland)
df_fill(hospitalVentilator_df_W, Wales)
hospitalVentilator_df_E = pd.read_pickle("England.pkl")
hospitalVentilator_df_S = pd.read_pickle("Scotland.pkl")
hospitalVentilator_df_NI = pd.read_pickle("Northern Ireland.pkl")
hospitalVentilator_df_W = pd.read_pickle("Wales.pkl")
nationDict = {
    'England': hospitalVentilator_df_E,
    'Scotland': hospitalVentilator_df_S,
    'Nortern Ireland': hospitalVentilator_df_NI,
    'Wales': hospitalVentilator_df_W
}
series = wdg.SelectMultiple(
    options=['hospital', 'ventilator'],
    value=['hospital', 'ventilator'],
    rows=2,
    description='Data:',
    disabled=False
)
nation = wdg.RadioButtons(
    options=['England', 'Scotland', 'Nortern Ireland', 'Wales'],
    description='Nation:',
    disabled=False
)
scale = wdg.RadioButtons(
    options=['linear', 'log'],
    description='Scale:',
    disabled=False
)


def call_graph(gseries, gnation, gscale):
    if gscale == 'linear':
        logscale = False
    else:
        logscale = True
    for i in list(nationDict.keys()):
        if gnation == i:
            ncols = len(gseries)
    if ncols > 0:
        nationDict[i][list(gseries)].plot(logy=logscale)
    plt.show
    else:
    print("Click to select data for graph")
    print("(CTRL-Click to select more than one category)")
    break
    else:
    next


graph = wdg.interactive_output(call_graph, {'gseries': series, 'gnation': nation, 'gscale': s
                                            controls = wdg.VBox([series, nation, scale, apibutton])
form = wdg.HBox([controls, graph])
display(form)
