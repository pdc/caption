"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from articles.models import Article, Info, Tag


class ArticleBehaviour(TestCase):
    def test_article_redirect_to_slug(self):
        self.given_a_website_visitor()
        self.given_an_article_for_caption_2012()

        self.when_article_requested_sans_slug()

        self.assertRedirects(self.response, '/2012/1-article-slug')

    def test_article_redirect_to_correct_slug(self):
        self.given_a_website_visitor()
        self.given_an_article_for_caption_2012()

        self.when_article_requested_with_wrong_slug()

        self.assertRedirects(self.response, '/2012/1-article-slug')

    def test_article_urls(self):
        self.given_a_website_visitor()
        self.given_an_article_for_caption_2012()

        self.when_article_requested()

        self.assertEqual('http://caption.org/2012/1-article-slug', self.response.context['article_canonical_url'])

    ###

    def given_a_website_visitor(self):
        self.client = Client()

    def given_an_article_for_caption_2012(self):
        self.author = User.objects.create(username='authorname')
        self.tag_2012 = Tag.objects.get(name='2012')
        self.article = Article.objects.create(
            author=self.author,
            title='Article Title',
            slug='article-slug',
            content='Hello, world')
        self.article.tags.add(self.tag_2012)
        self.article.save()

    def when_article_requested_sans_slug(self):
        self.response = self.client.get('/2012/1')

    def when_article_requested_with_wrong_slug(self):
        self.response = self.client.get('/2012/1-wrong-slug')

    def when_article_requested(self):
        self.response = self.client.get('/2012/1-article-slug')