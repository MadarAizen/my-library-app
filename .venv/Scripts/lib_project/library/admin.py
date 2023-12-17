from django.contrib import admin


# Register your models here.
from .models import *
admin.site.register(Book)
# admin.site.register(Readers)
admin.site.register(Appeals)
admin.site.register(Fines)
admin.site.register(Testik)