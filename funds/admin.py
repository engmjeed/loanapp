from django.contrib import admin
from .models import Fund

# Register your models here.

class FundAdmin(admin.ModelAdmin):

    list_display = ('name','description','balance','is_active',)
    # readonly_fields = ('name',)
    # ordering = ('-amount',)
    link_display = ('name',)
    fields = ('name','description','balance','is_active',)

admin.site.register(Fund,FundAdmin)


 