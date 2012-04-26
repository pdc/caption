from django.db import models
from django.contrib.auth.models import User



class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)

    title = models.CharField(max_length=200, unique_for_year='published')
    slug = models.SlugField()
    content = models.TextField()

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

    class Meta:
        # Reverse chronological order.
        ordering = ('-published', '-created')
