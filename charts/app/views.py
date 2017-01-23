# coding=utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from libs.gviz_api import *


KINDS = ['AreaChart', 'ColumnChart']


def generate_javascript(jscode, divId, backgroundColor="transparent", stacked=False, kind='ColumnChart', colors="['#FAA519', '#009DCA', '#C53425', '#FFE07F', '#4B4B4D']", my_options={}):
    import json
    """

    :param jscode:
    :param divId:
    :param backgroundColor:
    :param stacked:
    :param kind:
    :param colors:
    :return:
    """

    options = dict()
    options["showRowNumber"] = "true"
    options["isStacked"] = str(stacked).lower()
    options["colors"] = colors
    options["backgroundColor"] = backgroundColor
    google_options = {}

    for d in [options, my_options]:
        google_options.update(d)

    dumps_final = json.dumps(google_options)
    javascript = "google.load('visualization', '1.0', {'packages':['table', 'corechart']});" \
                 "google.setOnLoadCallback(function() {" \
                 " %s " \
                 "var jscode_table = new google.visualization.%s(document.getElementById('%s'));" \
                 "jscode_table.draw(jscode_data, %s);" \
                 "});" % (jscode, kind, divId, dumps_final)
    return javascript


@csrf_exempt
def code_hist(request):
    """

    :param request:
    :return: JavaScript code to embed in site (histogram)
    """

    import numpy

    x, ys, kind, divId, labels, colors, stacked, xType, callback, my_options = process_request(request)

    bins = numpy.linspace(start=0, stop=int(max(x)))
    histogram = numpy.histogram(x, bins)
    x = [histogram[1], histogram[0]]
    jscode = column_jscode(labels, xType, x, ys)
    javascript = generate_javascript(jscode, divId, stacked=False, kind='ColumnChart', colors=colors, my_options=my_options)

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

    x, ys, kind, divId, labels, colors, stacked, xType, callback, my_options = process_request(request)

    jscode = column_jscode(labels, xType, x, ys)
    javascript = generate_javascript(jscode, divId, stacked=stacked, kind=kind, colors=colors, my_options=my_options)

    context = {
        'javascript': javascript
    }

    return render(request, 'app/javascript.html', context, content_type="text")


def candlestick(request):
    """

    :param request:
    :return:
    """
    x, ys, kind, divId, labels, colors, stacked, xType, callback = process_request(request)


def home(request):
    """

    :param request:
    :return:
    """

    x, ys, kind, divId, labels, colors, stacked, xType, callback, my_options = process_request(request)

    jscode = column_jscode(labels, xType, x, ys)
    javascript = generate_javascript(jscode, divId, stacked=stacked, kind=kind, colors=colors, my_options=my_options)

    context = {
        'javascript': javascript
    }

    return render(request, 'app/home.html', context)


def column_jscode(labels=[""], xType="number", x=[""], *args):
    """
    :param args: series a graficar.
    Debe ser len(ys)>=0
    En caso de que len(ys)==0, puede ser para graficar un histograma.

    :return: Código JavaScript para generar la DataTable.
    """
    import string, datetime

    # series: [[x-axis], [y1-axis], [y2-axis]]
    args = list(*args)
    series = []
    series.append(x)
    for elem in args:
        series.append(elem)
    # print series
    # series = list(*series)
    # print "series:" + str(series)

    # TODO deben tener el mismo largo
    # TODO len(labels)==len(args)-1

    # chart = Chart()
    description = {}
    chars = []  # lista de caracteres que se usan para identificar cada serie

    for i, arg in enumerate(series):
        c = string.ascii_lowercase[i]
        chars.append(c)
        # print "i:" + str(i)
        # print "arg:" + str(arg)
        # print "c:" + str(c)
        if xType == 'date' and i == 0:  # i==0 --> x-axis
            description[str(c)] = ('date', "")
        elif xType == 'string' and i == 0:   # i==0 --> x-axis
            description[str(c)] = ('string', "")
        else:
            description[str(c)] = ('number', labels[i - 1])
    data_table = DataTable(description)
    # print data_table

    zipped = zip(*series)  # [(a1, b1, c1), (a2, b2, c2), ...]
    # print zipped
    # print chars
    data = []
    keys = []
    for z in zipped:
        registro = {}
        for i, c in enumerate(chars):
            # print i, c
            if c not in keys: keys.append(c)

            if xType == 'date' and i == 0:  # unicode comparison, not string
                registro[str(c)] = datetime.datetime.strptime(z[i], "%Y-%m-%d")
            else:  # normal case
                registro[str(c)] = z[i]
        data.append(registro)

    # print data

    data_table.LoadData(data)
    jscode = data_table.ToJSCode("jscode_data",
                                 columns_order=(keys),  # ("a", "b", "c", ...),
                                 order_by="a")
    return jscode


@csrf_exempt
def hist(request):

    x, ys, kind, divId, labels, colors, stacked, xType, callback, my_options = process_request(request)

    jscode = column_jscode(labels, xType, x, ys)
    javascript = generate_javascript(jscode, divId, stacked=stacked, kind='Histogram', colors=colors, my_options=my_options)

    context = {
        'javascript': javascript
    }

    response = render(request, 'app/home.html', context)
    return response


def process_request(request):
    import ast

    def get_string_value(http_method, key, default):
        try:
            return http_method[key]
        except:
            return default

    def get_python_value(http_method, key, default):
        try:
            return ast.literal_eval(http_method[key])
        except:
            return default

    def get_list_value(http_method, key):
        return get_python_value(http_method=http_method, key=key, default=[])

    def get_dict_value(http_method, key):
        return get_python_value(http_method=http_method, key=key, default={})

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
    xType = "number"
    callback = ""
    x = ys = labels = colors = []
    stacked = False
    my_options = {}

    if request.method == 'GET':
        x = get_list_value(request.GET, 'x')
        ys = get_list_value(request.GET, 'ys')
        kind = get_string_value(request.GET, 'kind', kind)
        divId = get_string_value(request.GET, 'divId', divId)
        xType = get_string_value(request.GET, 'xType', xType)
        callback = get_string_value(request.GET, 'callback', callback)
        labels = get_list_value(request.GET, 'labels')
        colors = get_list_value(request.GET, 'colors')
        stacked = get_boolean_value(request.GET, 'stacked')
        my_options = get_dict_value(request.GET, 'my_options')

    if request.method == 'POST':
        x = get_list_value(request.POST, 'x')
        ys = get_list_value(request.POST, 'ys')
        kind = get_string_value(request.POST, 'kind', kind)
        divId = get_string_value(request.POST, 'divId', divId)
        xType = get_string_value(request.POST, 'xType', xType)
        callback = get_string_value(request.POST, 'callback', callback)
        labels = get_list_value(request.POST, 'labels')
        colors = get_list_value(request.POST, 'colors')
        stacked = get_boolean_value(request.POST, 'stacked')
        my_options = get_dict_value(request.POST, 'my_options')

    if colors == []:
        colors.append("#FAA519")
        colors.append("#009DCA")
        colors.append("#C53425")
        colors.append("#FFE07F")
        colors.append("#4B4B4D")

    return x, ys, kind, divId, labels, colors, stacked, xType, callback, my_options
