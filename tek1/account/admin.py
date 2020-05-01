from django.contrib import admin
from .models import User
from .models import Temp, Visitor_perma

# Register your models here.
admin.site.register(User)
admin.site.register(Temp)
admin.site.register(Visitor_perma)
