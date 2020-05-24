import csv
import os
import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid19stats_backend.settings")
# django.setup()

files_base = "/static/COVID-19/csse_covid_19_data/csse_covid_19_time_series/"
global_recovered_csv = "time_series_covid19_recovered_global.csv"
global_confirmed_csv = "time_series_covid19_confirmed_global.csv"
global_deaths_csv = "time_series_covid19_deaths_global.csv"


def toListOfDict(file):
    f = open(os.path.dirname(os.path.realpath(__file__)) + files_base + file, 'r')
    dict_reader = csv.DictReader(f)
    dict_from_csv = list(dict_reader)
    return dict_from_csv


# return tuples
def array_data(dict_data):
    return list(dict_data.items())


def csv_sorted(list_of_dicts):
    def sort_key(e):
        return e['Country/Region']

    list_of_dicts.sort(key=sort_key)


def global_dict(list_of_dicts):
    formatted_dict = []
    csv_sorted(list_of_dicts)
    for i in range(len(list_of_dicts)):
        if i == len(list_of_dicts) - 1:
            formatted_dict.append(list_of_dicts[i])
            break
        if list_of_dicts[i]['Country/Region'] == list_of_dicts[i + 1]['Country/Region']:
            list_of_dicts[i + 1]['Province/State'] = ''
            for key in list(list_of_dicts[i].keys())[4:]:
                list_of_dicts[i + 1][key] = str(int(list_of_dicts[i][key]) + int(list_of_dicts[i + 1][key]))
        else:
            formatted_dict.append(list_of_dicts[i])
    return formatted_dict


# d: dictionary
# i: index
# return i-th key's (int) value of the dict
def dic_index(d, i):
    return int(d[list(d.keys())[i]])


confirmed_dicts = global_dict(toListOfDict(global_confirmed_csv))
deaths_dicts = global_dict(toListOfDict(global_deaths_csv))
recovered_dicts = global_dict(toListOfDict(global_recovered_csv))


def global_stats():
    result = []
    for i in range(len(confirmed_dicts)):
        node = {'country': confirmed_dicts[i]['Country/Region'],
                'confirmed': dic_index(confirmed_dicts[i], -1),
                'confirmed_change': dic_index(confirmed_dicts[i], -1) - dic_index(confirmed_dicts[i], -2),
                'deaths': dic_index(deaths_dicts[i], -1),
                'deaths_change': dic_index(deaths_dicts[i], -1) - dic_index(deaths_dicts[i], -2),
                'recovered': dic_index(recovered_dicts[i], -1),
                'recovered_change': dic_index(recovered_dicts[i], -1) - dic_index(recovered_dicts[i], -2)}
        result.append(node)

        def sort_key(e):
            return e['confirmed']

        result.sort(key=sort_key, reverse=True)

    return result


def global_total():
    gs_list = global_stats()
    result = []
    tc = tcc = td = tdc = tr = trc = 0
    for i in range(len(global_stats())):
        tc = tc + gs_list[i]['confirmed']
        tcc = tcc + gs_list[i]['confirmed_change']
        td = td + gs_list[i]['deaths']
        tdc = tdc + gs_list[i]['deaths_change']
        tr = tr + gs_list[i]['recovered']
        trc = trc + gs_list[i]['recovered_change']
    node = {'total_confirmed': tc,
            'total_confirmed_change': tcc,
            'total_deaths': td,
            'total_deaths_change': tdc,
            'total_recovered': tr,
            'total_recovered_change': trc}
    result.append(node)
    return node


r_confirmed_dicts = toListOfDict(global_confirmed_csv)
r_deaths_dicts = toListOfDict(global_deaths_csv)
r_recovered_dicts = toListOfDict(global_recovered_csv)


def region_stats():
    with_province = {
        'Australia': [],
        'Canada': [],
        'China': [],
        'Netherlands': [],
        'UK': [],
        'France': [],
        'Denmark': []
    }
    csv_sorted(r_confirmed_dicts)
    csv_sorted(r_deaths_dicts)
    csv_sorted(r_recovered_dicts)
    for i in range(len(r_confirmed_dicts)):
        c = r_confirmed_dicts[i]['Country/Region']
        if c in list(with_province.keys()):
            node = {
                'province': r_confirmed_dicts[i]['Province/State'],
                'confirmed': dic_index(r_confirmed_dicts[i], -1),
                'confirmed_change': dic_index(r_confirmed_dicts[i], -1) - dic_index(r_confirmed_dicts[i], -2),
                'deaths': dic_index(r_deaths_dicts[i], -1),
                'deaths_change': dic_index(r_deaths_dicts[i], -1) - dic_index(r_deaths_dicts[i], -2),
                'recovered': dic_index(r_recovered_dicts[i], -1),
                'recovered_change': dic_index(r_recovered_dicts[i], -1) - dic_index(r_recovered_dicts[i], -2)
            }
            with_province[c].append(node)
    return with_province


def region_total():
    pass