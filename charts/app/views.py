# coding=utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from libs.gviz_api import *

KINDS = ['AreaChart', 'ColumnChart']


def generate_javascript(jscode, divId, backgroundColor="'transparent'", stacked=False, kind='ColumnChart', colors="['orange', 'yellow', 'red']"):
    """

    :param jscode:
    :param divId:
    :param backgroundColor:
    :param stacked:
    :param kind:
    :param colors:
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
def code_hist(request):
    """

    :param request:
    :return: JavaScript code to embed in site (histogram)
    """


    # from charts.settings import ALLOWED_HOSTS as ORIGINS

    data, kind, divId, labels, colors, stacked, xAxis, callback = process_request(request)

    print len(data)

    jscode = column_jscode(labels, xAxis, data)
    javascript = generate_javascript(jscode, divId, stacked=False, kind='Histogram', colors=colors)

    print javascript

    if callback != "":
        javascript = "%s(%s)" % (callback, javascript)

    context = {
        'javascript': javascript
    }

    response = render(request, 'app/javascript.html', context, content_type="text")
    response['Access-Control-Allow-Methods'] = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

    return response

@csrf_exempt
def code(request):
    """

    :param request:
    :return: JavaScript code to embed in site
    """

    data, kind, divId, labels, colors, stacked, xAxis, callback = process_request(request)

    jscode = column_jscode(labels, xAxis, data)
    javascript = generate_javascript(jscode, divId, stacked=stacked, kind=kind, colors=colors)

    context = {
        'javascript': javascript
    }

    return render(request, 'app/javascript.html', context, content_type="text")


def candlestick(request):
    """

    :param request:
    :return:
    """
    data, kind, divId, labels, colors, stacked, xAxis, callback = process_request(request)


def home(request):
    """

    :param request:
    :return:
    """

    data, kind, divId, labels, colors, stacked, xAxis, callback = process_request(request)

    jscode = column_jscode(labels, xAxis, data)
    javascript = generate_javascript(jscode, divId, stacked=stacked, kind=kind, colors=colors)

    context = {
        'javascript': javascript
    }

    return render(request, 'app/home.html', context)


def column_jscode(labels=[""], xAxis="number", *args):
    """
    :param args: series a graficar.
    Debe ser len(args)>=1
    En caso de que len(args)==1, puede ser para graficar un histograma.

    :return: Código JavaScript para generar la DataTable.
    """
    import string, datetime

    series = args   
    series = list(*series)

    # TODO deben tener el mismo largo
    # TODO len(labels)==len(args)-1

    # chart = Chart()
    description = {}
    chars = []  # lista de caracteres que se usan para identificar cada serie

    for i, arg in enumerate(series):
        c = string.ascii_lowercase[i]
        chars.append(c)
        if xAxis == 'date' and i == 0:
            description[str(c)] = ('date', "")
        elif xAxis == 'string' and i == 0:
            description[str(c)] = ('string', "")
        else:
            description[str(c)] = ('number', labels[i - 1])
    data_table = DataTable(description)

    zipped = zip(*series)  # [(a1, b1, c1), (a2, b2, c2), ...]
    data = []
    keys = []
    for z in zipped:
        registro = {}
        for i, c in enumerate(chars):
            if c not in keys: keys.append(c)

            if xAxis == 'date' and i == 0:  # unicode comparison, not string
                registro[str(c)] = datetime.datetime.strptime(z[i], "%d/%m/%Y")
            else:  # normal case
                registro[str(c)] = z[i]
        data.append(registro)

    data_table.LoadData(data)
    jscode = data_table.ToJSCode("jscode_data",
                                 columns_order=(keys),  # ("a", "b", "c", ...),
                                 order_by="a")
    return jscode


@csrf_exempt
def hist(request):
    from django import http
    # from charts.settings import ALLOWED_HOSTS as ORIGINS

    data, kind, divId, labels, colors, stacked, xAxis, callback = process_request(request)

    jscode = column_jscode(labels, xAxis, data)
    javascript = generate_javascript(jscode, divId, stacked=stacked, kind='Histogram', colors=colors)

    context = {
        'javascript': javascript
    }

    response = render(request, 'app/home.html', context)
    # response['Access-Control-Allow-Origin'] = ORIGINS
    return response


def process_request(request):
    import ast

    def get_string_value(http_method, key, default):
        try:
            return http_method[key]
        except:
            return default

    def get_list_value(http_method, key):
        try:
            return ast.literal_eval(http_method[key])
        except:
            return []

    def get_boolean_value(http_method, key):
        try:
            if http_method[key].lower() == "true":
                return True
            else:
                return False
        except:
            return False

    kind = "ColumnChart"
    divId = ""
    xAxis = "number"
    callback = ""
    data = labels = colors = []
    stacked = False

    if request.method == 'GET':
        data = get_list_value(request.GET, 'data')
        kind = get_string_value(request.GET, 'kind', kind)
        divId = get_string_value(request.GET, 'divId', divId)
        xAxis = get_string_value(request.GET, 'xAxis', xAxis)
        callback = get_string_value(request.GET, 'callback', callback)
        labels = get_list_value(request.GET, 'labels')
        colors = get_list_value(request.GET, 'colors')
        stacked = get_boolean_value(request.GET, 'stacked')

    if request.method == 'POST':
        data = get_list_value(request.POST, 'data')
        kind = get_string_value(request.POST, 'kind', kind)
        divId = get_string_value(request.POST, 'divId', divId)
        xAxis = get_string_value(request.POST, 'xAxis', xAxis)
        callback = get_string_value(request.POST, 'callback', callback)
        labels = get_list_value(request.POST, 'labels')
        colors = get_list_value(request.POST, 'colors')
        stacked = get_boolean_value(request.POST, 'stacked')

    return data, kind, divId, labels, colors, stacked, xAxis, callback