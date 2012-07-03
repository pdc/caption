# Create your views here.

from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from articles.models import Article, Info, Tag

def with_template(template_name):
    def view_decorator(view):
        def decorated_view(request, *args, **kwargs):
            result = view(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            template_vars = result
            return render(request, template_name, template_vars)
        return decorated_view
    return view_decorator


@with_template('articles/index.html')
def index(request, year):
    if year is None:
        year = datetime.now().year
    tags = [get_object_or_404(Tag, name=year)]
    articles =  tags[0].published_articles()
    infos = tags[0].published_infos()
    return {
        'articles': articles,
        'infos': infos,
        'year': tags[0],
        'tags': tags,
    }

@with_template('articles/article.html')
def article(request, year, article_id, slug=None):
    article =  get_object_or_404(Article, id=article_id)
    article_path = reverse('article-detail',
            kwargs={'year': year, 'article_id': article.id, 'slug': article.slug})
    if article.slug != slug:
        return HttpResponseRedirect(article_path)
    article_url = request.build_absolute_uri(article_path)
    article_canonical_url = 'http://caption.org{0}'.format(article_path)
    tags = [get_object_or_404(Tag, name=year)]
    infos = tags[0].published_infos()
    articles =  tags[0].published_articles()
    return {
        'article': article,
        'article_url': article_url,
        'article_canonical_url': article_canonical_url,
        'articles': articles,
        'infos': infos,
        'year': tags[0],
        'tags': tags,
    }

@with_template('articles/info.html')
def info(request, year, info_name, slug=None):
    tags = [get_object_or_404(Tag, name=year)]
    infos = tags[0].published_infos()
    info =  get_object_or_404(Info, name=info_name)
    articles =  tags[0].published_articles()
    return {
        'info': info,
        'infos': infos,
        'articles': articles,
        'year': tags[0],
        'tags': tags,
    }
