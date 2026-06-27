from django.contrib import admin
from .models import *

admin.site.register([Brand,Category,Product,Firm,Purchases,Sales])
# Register your models here.
