__author__ = 'agustin'
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'app.views.home', name='home'),
                       url(r'^code$', 'app.views.code', name='code'),

                       url(r'^hist$', 'app.views.hist', name='hist'),
                       url(r'^hist/code$', 'app.views.code_hist', name='hist'),
)
