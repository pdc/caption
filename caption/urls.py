from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'caption.views.home', name='home'),
    # url(r'^caption/', include('caption.foo.urls')),

    url(r'^$', 'articles.views.index', {'year': None}, 'article-index'),
    url(r'^(?P<year>20\d\d)/$', 'articles.views.index', {}, 'article-index'),
    url(r'^(?P<year>20\d\d)/(?P<article_id>\d+)$', 'articles.views.article', {}, 'article-detail'),
    url(r'^(?P<year>20\d\d)/(?P<article_id>\d+)-(?P<slug>[\w-]+)$', 'articles.views.article', {}, 'article-detail'),
    url(r'^(?P<year>20\d\d)/(?P<info_name>[a-z][\w-]+)$', 'articles.views.info', {}, 'info-detail'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
