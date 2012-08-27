# Create your views here.

from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from articles.models import Article, Info, Tag

def with_template(template_name):
    """A decorator for attaching a template to a view function.

    The function returns a dictionary which is used
    as the templat3e context.
    """
    def view_decorator(view):
        def decorated_view(request, *args, **kwargs):
            result = view(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            template_vars = result
            return render(request, template_name, template_vars)
        return decorated_view
    return view_decorator


def get_year():
    """Return the current year, used on the index page.

    Split out as a separate function to allow for testing.
    """
    return datetime.now().year

def get_now():
    return datetime.now()


@with_template('articles/index.html')
def index(request):
    year_tag = Tag.objects.get(name=get_year())
    tags = []
    articles =  Article.objects.filter(published__lte=get_now())
    infos = year_tag.published_infos()
    return {
        'articles': articles,
        'infos': infos,
        'year': year_tag,
        'tags': tags,
    }

@with_template('articles/index.html')
def year_index(request, year):
    year_tag = get_object_or_404(Tag, name=year)
    tags = [year_tag]
    articles =  tags[0].published_articles()
    infos = tags[0].published_infos()
    return {
        'articles': articles,
        'infos': infos,
        'year': year_tag,
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
