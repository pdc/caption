# -*-coding: UTF-8-*-

from datetime import datetime
from django.utils.timezone import utc
from django.db import models
from django.contrib.auth.models import User



def get_now():
    return datetime.utcnow()

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __unicode__(self):
        return self.name

    def published_articles(self):
        return self.article_set.filter(published__lte=get_now())

    def published_infos(self):
        return self.info_set.filter(published__lte=get_now())


class Article(models.Model):
    author = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)

    title = models.CharField(max_length=200, unique_for_year='published')
    slug = models.SlugField()
    content = models.TextField()

    # Optional media attachment
    embedded_media = models.TextField(blank=True, help_text='Optional media attachment.')
    poster_src = models.URLField(blank=True, help_text='Optional picture to display above media embed. Ideal width: 220px.')
    poster_credit = models.CharField(max_length=100, blank=True, help_text='Optional credit for the photographer of the poster image')
    poster_href = models.URLField(blank=True, help_text='Optional link to photographer’s web site')

    published = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.title

    def year(self):
        """The CAPTION year this article relates to."""
        for tag in self.tags.all():
            if tag.name.startswith('20'):
                return tag.name
        return str(published.year)

    def unique_id(self):
        return 'tag:caption.org,2012:article:{0},{1}'.format(self.year(), self.id)

    class Meta:
        # Reverse chronological order.
        ordering = ('-published', '-created')


class Info(models.Model):
    """An information page, e.g., about the venue."""
    tags = models.ManyToManyField(Tag)

    name = models.SlugField(help_text='Internal name used in the URL')
    title = models.CharField(max_length=200, unique_for_year='published')
    summary = models.TextField(blank=True, help_text='Shown on the front page linking to the main content. Blank means not shown on the front page.')
    content = models.TextField(blank=True, help_text='Shown on the info page. Blank means there is no separate info page.')
    sequence = models.IntegerField(blank=True, default=0, help_text='Controls the otrder of info items.')

    published = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.title

    class Meta:
        # Reverse chronological order.
        ordering = ('sequence', 'created')