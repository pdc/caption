# -*-coding: UTF-8-*-

from django.db import models
from django.contrib.auth.models import User
from articles.models import Article

class DripAuthor(models.Model):
    uid = models.IntegerField(editable=False, primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    mail = models.EmailField(max_length=64, blank=True)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.uid)

class DripNode(models.Model):
    article = models.OneToOneField(Article, null=False, editable=False, related_name='drip')
    author = models.ForeignKey(DripAuthor)

    nid = models.IntegerField(editable=False, primary_key=True)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.article.title, self.nid)

