from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    url(r'^charts/', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
