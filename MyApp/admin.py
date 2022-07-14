from django.contrib import admin
# Register your models here.
from MyApp.models import *

import inspect,sys

clsmemebers = inspect.getmembers(sys.modules[__name__],inspect.isclass)
for name,cls in clsmemebers:
    admin.site.register(cls)