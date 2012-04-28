# Create your views here.

from datetime import datetime
from django.http import HttpResponse
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
    articles =  tags[0].article_set.all()
    infos = tags[0].info_set.all()
    return {
        'articles': articles,
        'infos': infos,
        'year': tags[0],
        'tags': tags,
    }

@with_template('articles/article.html')
def article(request, year, article_id, slug=None):
    article =  get_object_or_404(Article, id=article_id)
    if article.slug != slug:
        return redirect(article, year=year, article_id=article.id, slug=article.slug)
    article_url = request.build_absolute_uri(
        reverse('article-detail',
            kwargs={'year': year, 'article_id': article.id, 'slug': article.slug}))
    tags = [get_object_or_404(Tag, name=year)]
    infos = tags[0].info_set.all()
    articles =  tags[0].article_set.all()
    return {
        'article': article,
        'article_url': article_url,
        'articles': articles,
        'infos': infos,
        'year': tags[0],
        'tags': tags,
    }

@with_template('articles/info.html')
def info(request, year, info_name, slug=None):
    tags = [get_object_or_404(Tag, name=year)]
    infos = tags[0].info_set.all()
    info =  get_object_or_404(Info, name=info_name)
    articles =  tags[0].article_set.all()
    return {
        'info': info,
        'infos': infos,
        'articles': articles,
        'year': tags[0],
        'tags': tags,
    }
