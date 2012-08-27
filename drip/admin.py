from django.contrib import admin
from drip.models import DripAuthor, DripNode

class DripAuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'uid', 'mail')

class DripNodeAdmin(admin.ModelAdmin):
    list_display = ('article', 'nid', 'author')

admin.site.register(DripAuthor, DripAuthorAdmin)
admin.site.register(DripNode, DripNodeAdmin)
