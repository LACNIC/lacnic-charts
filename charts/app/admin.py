from django.contrib import admin
from itertools import chain
from app.models import *

@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    pass