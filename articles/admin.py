from django.contrib import admin
from articles.models import Article, Tag

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'
    list_display = ('title', 'author', 'published')
    list_filter = ('tags',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
