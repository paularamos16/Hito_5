from django.contrib import admin
from main.models import Flan, Contact
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contact, ContactAdmin)

class FlanAdmin(admin.ModelAdmin):
    pass

admin.site.register(Flan, FlanAdmin)