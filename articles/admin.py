from django.contrib import admin
from articles.models import Article, Info, Tag

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'
    list_display = ('title', 'author', 'published')
    list_filter = ('tags',)
    prepopulated_fields = {"slug": ("title",)}

class InfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'sequence', 'published')
    list_editable = ('title', 'sequence')
    list_filter = ('tags',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(Tag)
