from django.contrib import admin
from .models import Organisation,Center

# Register your models here.

class OrganisationAdmin(admin.ModelAdmin):

    list_display = ('name','contact_email','contact_phone','address','manager','is_active',)
    # readonly_fields = ('name',)
    # ordering = ('-amount',)
    link_display = ('name',)
    fields = ('name','contact_email','contact_phone','address','manager','is_active','products')


class CenterAdmin(admin.ModelAdmin):

    list_display = ('name','contact_email','contact_phone','address','manager','organisation','is_active',)
    # readonly_fields = ('name',)
    # ordering = ('-amount',)
    # link_display = ('name',)
    list_display_links = ('name',)
    fields = ('name','contact_email','contact_phone','address','manager','is_active','organisation','products')
    
admin.site.register(Organisation,OrganisationAdmin)
admin.site.register(Center,CenterAdmin)

 