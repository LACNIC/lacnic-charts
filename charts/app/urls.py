__author__ = 'agustin'
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^hist$', 'app.views.hist', name='hist'),
    url(r'^hist/code$', 'app.views.javascript', name='hist'),
)
