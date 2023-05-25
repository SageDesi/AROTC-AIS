from django.contrib import admin

# Register your models here.
from .models import SuperCOA
admin.site.register(SuperCOA)

from .models import COA 
admin.site.register(COA)