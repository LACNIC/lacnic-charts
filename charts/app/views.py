from django.shortcuts import render
from libs.gviz_api import *
from app.models import Chart

def home(request):

    chart = Chart.objects.get(id=1)

    print chart.x.split(',')
    print chart.y.split(',')

    zipped = zip(chart.x.split(','), chart.y.split(','))
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
          "var jscode_table = new google.visualization.LineChart(document.getElementById('%s'));" \
          "jscode_table.draw(jscode_data, {showRowNumber: true});" \
          "});" % (jscode, 'divId')

    context = {'json' : json,
               'jscode' : jscode,
               'javascript' : javascript}

    return render(request, 'app/home.html', context)