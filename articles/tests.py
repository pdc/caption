"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from mock import Mock, patch

from datetime import datetime
from django.utils.timezone import utc
from django.contrib.auth.models import User
from articles.models import Article, Info, Tag
from articles import views

class YearTests(TestCase):
    def test_index_for_specified_year(self):
        self.given_a_website_visitor()
        self.given_articles_for_years([2012, 2011, 2010])

        self.when_index_requested_with_year(2011)

        self.then_chosen_articles_should_be([2011])

    def test_index_for_current_year(self):
        self.given_a_website_visitor()
        self.given_articles_for_years([2012, 2011, 2010])

        self.when_index_requested_without_year_when_current_year_is(2012)

        self.then_chosen_articles_should_be([2012, 2011, 2010])

    def test_when_year_specified_base_template_is_for_that_year(self):
        self.given_a_website_visitor()
        self.given_articles_for_years([2012, 2011, 2010])

        self.when_index_requested_with_year(2011)

        self.then_base_template_should_be('articles/2011/base.html')

    def test_when_year_specified_index_template_is_for_that_year(self):
        self.given_a_website_visitor()
        self.given_articles_for_years([2012, 2011, 2010])

        self.when_index_requested_with_year(2011)

        self.then_should_use_template('articles/2011/front.html')

    def test_when_year_unspecified_template_is_for_current_year(self):
        self.given_a_website_visitor()
        self.given_articles_for_years([2012, 2011, 2010])

        self.when_index_requested_without_year_when_current_year_is(2012)

        self.then_base_template_should_be('articles/2012/base.html')

    # helpers for the above tests:

    def given_a_website_visitor(self):
        self.client = Client()

    def given_articles_for_years(self, ys):
        self.author = User.objects.create(username='authorname')
        self.tags = {}
        for y in ys:
            self.tags[y] = Tag.objects.get(name=str(y))
            self.article = Article.objects.create(
                author=self.author,
                title=u'{0} ARTICLE'.format(y),
                slug='{0}-article'.format(y),
                content='CONTENT {0}'.format(y),
                published=datetime(2012,8,21, 8,52,0).replace(tzinfo=utc))
            self.article.tags.add(self.tags[y])
            self.article.save()

    def when_index_requested_with_year(self, y):
        u = '/{0}/'.format(y)
        self.response = self.client.get(u)

    def when_index_requested_without_year_when_current_year_is(self, y):
        u = '/'
        with patch.object(views, 'get_year') as mock_year:
            mock_year.return_value = y
            self.response = self.client.get(u)
            mock_year.assert_called_with()

    def then_chosen_articles_should_be(self, ys):
        article_titles = sorted(x.title for x in self.response.context['articles'])
        expected_titles = ['{0} ARTICLE'.format(y) for y in sorted(ys)]
        self.assertEqual(expected_titles, article_titles)

    def then_base_template_should_be(self, expected):
        self.assertEqual(expected, self.response.context['base_template'])

    def then_should_use_template(self, template_name):
        self.assertTrue(any(t for t in self.response.templates if t.name == template_name),
                'Expected to use the template %r' % template_name)


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