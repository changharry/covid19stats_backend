import csv
import os
import numpy as np
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
                'recovered_change': dic_index(recovered_dicts[i], -1) - dic_index(recovered_dicts[i], -2),
                'update_time': list(confirmed_dicts[i].keys())[-1]}
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
        'United Kingdom': [],
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

            def sort_key(e):
                return e['confirmed']

            with_province[c].sort(key=sort_key, reverse=True)
        else:
            node = [{
                'province': '',
                'confirmed': dic_index(r_confirmed_dicts[i], -1),
                'confirmed_change': dic_index(r_confirmed_dicts[i], -1) - dic_index(r_confirmed_dicts[i], -2),
                'deaths': dic_index(r_deaths_dicts[i], -1),
                'deaths_change': dic_index(r_deaths_dicts[i], -1) - dic_index(r_deaths_dicts[i], -2),
                'recovered': dic_index(r_recovered_dicts[i], -1),
                'recovered_change': dic_index(r_recovered_dicts[i], -1) - dic_index(r_recovered_dicts[i], -2)
            }]
            with_province[c] = node
    return with_province


def graph_data_v(lod):
    dict_lod = global_dict(lod)
    values = []
    for i in dict_lod:
        v = list(i.values())[4:]
        v = list(map(int, v))
        values.append(v)
    return [sum(x) for x in zip(*values)]


def graph_data_l(lod):
    dict_lod = global_dict(lod)
    labels = list(dict_lod[0].keys())[4:]
    return labels


def g_total():
    node = {
        'label': graph_data_l(confirmed_dicts),
        'confirmed': graph_data_v(confirmed_dicts),
        'deaths': graph_data_v(deaths_dicts),
        'recovered': graph_data_v(recovered_dicts)
    }
    return node


def difference(data):
    return [(b - a) for a, b in zip(data[::1], data[1::1])]


def g_total_change():
    node = {
        'label': graph_data_l(confirmed_dicts)[1:],
        'confirmed': difference(graph_data_v(confirmed_dicts)),
        'deaths': difference(graph_data_v(deaths_dicts)),
        'recovered': difference(graph_data_v(recovered_dicts))
    }
    return node


def rate_difference(data):
    return [100 * (b - a) / a if a != 0 else 0 for a, b in zip(data[::1], data[1::1])]


def g_total_rate_change():
    node = {
        'label': graph_data_l(confirmed_dicts)[1:],
        'confirmed': rate_difference(graph_data_v(confirmed_dicts)),
        'deaths': rate_difference(graph_data_v(deaths_dicts)),
        'recovered': rate_difference(graph_data_v(recovered_dicts))
    }
    return node


print(confirmed_dicts)


def itr_r(country, dicts):
    for i in dicts:
        if i['Country/Region'] == country:
            return i


def r_total(country):
    c_data = list(itr_r(country, confirmed_dicts).values())[4:]
    d_data = list(itr_r(country, deaths_dicts).values())[4:]
    r_data = list(itr_r(country, recovered_dicts).values())[4:]
    label = list(itr_r(country, confirmed_dicts).keys())[4:]
    node = {
        'label': label,
        'c': c_data,
        'd': d_data,
        'r': r_data
    }
    return node


def r_change(country):
    c_data = difference(list(map(int, list(itr_r(country, confirmed_dicts).values())[4:])))
    d_data = difference(list(map(int, list(itr_r(country, deaths_dicts).values())[4:])))
    r_data = difference(list(map(int, list(itr_r(country, recovered_dicts).values())[4:])))
    label = list(itr_r(country, confirmed_dicts).keys())[4:][1:]
    node = {
        'label': label,
        'c': c_data,
        'd': d_data,
        'r': r_data
    }
    return node


def r_rate_change(country):
    c_data = rate_difference(list(map(int, list(itr_r(country, confirmed_dicts).values())[4:])))
    d_data = rate_difference(list(map(int, list(itr_r(country, deaths_dicts).values())[4:])))
    r_data = rate_difference(list(map(int, list(itr_r(country, recovered_dicts).values())[4:])))
    label = list(itr_r(country, confirmed_dicts).keys())[4:][1:]
    node = {
        'label': label,
        'c': c_data,
        'd': d_data,
        'r': r_data
    }
    return node
