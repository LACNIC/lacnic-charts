# coding=utf-8
from django.shortcuts import render
from django.utils.datastructures import MultiValueDict
from django.views.decorators.csrf import csrf_exempt
from libs.gviz_api import *
from app.models import Chart

KINDS = ['AreaChart', 'ColumnChart']

def generate_javascript(jscode, divId, backgroundColor="'transparent'", stacked=False, kind='ColumnChart', colors="['orange', 'yellow', 'red']"):
    """

    :param jscode:
    :param stacked:
    :param kind:
    :return:
    """

    options = "{showRowNumber: true," \
              "isStacked: %s," \
              "colors : %s," \
              "backgroundColor : %s}" % (str(stacked).lower(), colors, backgroundColor)

    javascript = "google.load('visualization', '1.0', {'packages':['table', 'corechart']});" \
                 "google.setOnLoadCallback(function() {" \
                 " %s " \
                 "var jscode_table = new google.visualization.%s(document.getElementById('%s'));" \
                 "jscode_table.draw(jscode_data, %s);" \
                 "});" % (jscode, kind, divId, options)
    return javascript

@csrf_exempt
def javascript(request):
    """

    :param request:
    :return: JavaScript code to embedd in site
    """
    data, kind, divId, labels, colors = process_request(request)
    jscode = column_jscode(labels, data)
    javascript = generate_javascript(jscode, divId, stacked=False, kind='Histogram', colors=colors)

    context = {
        'javascript': javascript
    }

    return render(request, 'app/javascript.html', context, content_type="text")

def home(request):
    """

    :param request:
    :return:
    """

    data, kind, divId, labels, colors = process_request(request)

    jscode = column_jscode(labels, data)
    javascript = generate_javascript(jscode, divId, stacked=False, kind=kind, colors=colors)

    context = {
        'javascript': javascript
    }

    return render(request, 'app/home.html', context)


def column_jscode(labels=[""], *args):
    """
    :param args: series a graficar.
    Debe ser len(args)>=1
    En caso de que len(args)==1, puede ser para graficar un histograma.

    :return: Código JavaScript para generar la DataTable.
    """
    import string

    series = args
    series = list(*series)
    x = series[0]

    # TODO deben tener el mismo largo
    # TODO len(labels)==len(args)-1

    chart = Chart()
    description = {}
    chars = [] # lista de caracteres que se usan para identificar cada serie
    for i, arg in enumerate(series):
        c = string.ascii_lowercase[i]
        chars.append(c)
        description[str(c)] = ('number', labels[i-1])
    data_table = DataTable(description)

    zipped = zip(*series) # [(a1, b1, c1), (a2, b2, c2), ...]
    data = []
    keys = []
    for z in zipped:
        registro = {}
        for i, c in enumerate(chars):
            if c not in keys: keys.append(c)
            registro[str(c)] = z[i]
        data.append(registro)
    data_table.LoadData(data)

    jscode = data_table.ToJSCode("jscode_data",
                                 columns_order=(keys),  # ("a", "b", "c", ...),
                                 order_by="a")


    return jscode

@csrf_exempt
def hist(request):

    data, kind, divId, labels, colors = process_request(request)

    jscode = column_jscode(labels, data)
    javascript = generate_javascript(jscode, divId, stacked=False, kind='Histogram', colors=colors)

    context = {
        'javascript': javascript
    }

    return render(request, 'app/home.html', context)

def process_request(request):
    import ast

    def get_value(http_method, key):
        from django.utils.datastructures import MultiValueDictKeyError
        try:
            return http_method[key]
        except MultiValueDictKeyError as e:
            return ""
        except:
            return ""

    kind = divId = ""
    data = labels = colors = []

    if request.method == 'GET':
        data = ast.literal_eval(get_value(request.GET, 'data'))
        kind = get_value(request.GET, 'kind')
        divId = get_value(request.GET, 'divId')
        labels = ast.literal_eval(get_value(request.GET, 'labels'))
        colors = ast.literal_eval(get_value(request.GET, 'colors'))

    if request.method == 'POST':
        data = ast.literal_eval(get_value(request.POST, 'data'))
        kind = get_value(request.POST, 'kind')
        divId = get_value(request.POST, 'divId')
        labels = ast.literal_eval(get_value(request.POST, 'labels'))
        colors = ast.literal_eval(get_value(request.POST, 'colors'))

    return data, kind, divId, labels, colors