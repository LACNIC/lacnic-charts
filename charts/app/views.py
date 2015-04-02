from django.shortcuts import render
from libs.gviz_api import *
from app.models import Chart


def home(request):
    import numpy

    N = 100
    x = range(N)
    y = numpy.random.rand(N) * 10

    print x
    print y

    json, jscode, javascript = column_chart(x, y)

    context = {'json': json,
               'jscode': jscode,
               'javascript': javascript}

    return render(request, 'app/home.html', context)


def column_chart(x, y):
    chart = Chart()

    zipped = zip(x, y)
    data = []
    for z in zipped:
        data.append({"x": int(z[0]), "y": int(z[1])})

    description = {"x": ("number", chart.xTitle),
                   "y": ("number", chart.yTitle)}

    data_table = DataTable(description)
    data_table.LoadData(data)

    jscode = data_table.ToJSCode("jscode_data",
                                 columns_order=("x", "y"),
                                 order_by="x")

    json = data_table.ToJSonResponse(columns_order=("x", "y"), order_by="x")

    javascript = "google.load('visualization', '1.0', {'packages':['table', 'corechart']});" \
                 "google.setOnLoadCallback(function() {" \
                 " %s " \
                 "var jscode_table = new google.visualization.ColumnChart(document.getElementById('%s'));" \
                 "jscode_table.draw(jscode_data, {showRowNumber: true});" \
                 "});" % (jscode, 'divId')

    return json, jscode, javascript


def hist(request):
    """
       Receives 'data' as the only GET parameter
    """
    import numpy, json

    if request.method != 'GET' and request.method != 'POST':
        return

    if request.method == 'GET':
        data_string = request.GET['data']
    if request.method == 'POST':
        data_string = request.POST['data']

    data = json.loads(data_string)
    y, edges = numpy.histogram(data)

    x = [e + edges[i + 1] / 2.0 for i, e in enumerate(edges[:-1])]

    json, jscode, javascript = column_chart(x, y)
    print x
    print hist

    context = {'json': json,
               'jscode': jscode,
               'javascript': javascript}

    return render(request, 'app/home.html', context)