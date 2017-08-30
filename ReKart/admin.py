
from django.contrib import admin
from models import *
from django.apps import apps

# Register your models here.
models = apps.get_models()
admin.site.register(states)
admin.site.register(cities)
admin.site.register(item_details)
admin.site.register(category)

