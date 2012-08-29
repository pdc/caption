#! /usr/bin/env python
# -*-coding: UTF-8-*-

import sys
import os
import re
from pprint import pprint
from datetime import datetime, timedelta


root_dir = os.path.dirname(os.path.dirname(__file__))
if root_dir not in sys.path:
    sys.path[1:1] = [root_dir]
from caption import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.utils.timezone import utc
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from articles.models import Tag, Article
from drip.models import DripNode, DripAuthor


tag_names_by_term = dict(('CAPTION %d' % y, '%d' % y) for y in range(1999, 2013))
tag_names_by_term .update(('Caption %d' % y, '%d' % y) for y in range(1999, 2013))
tag_names_by_term.update(('CAPTION%d' % y, '19%d' % y) for y in range(92, 99))
tag_names_by_term.update({
    u'CAPTION Comics Collective 2008': '2008a',
    u'east oxford community centre': 'eocc',
    u'Jam Factory': 'jam-factory',
    u'CAPTION 2008': '2008b',
    u'Caption 2008': '2008b',
})

other_tags = [
 u'report',
 u'video',
 u'photos',
 u'history',
 u'exhibition',
 u'event',
 u'Current',
 u'Historical',
 u'east oxford community centre',
 u'announcement',
 u'venue',
 u'faq',
 u'table',
 u'parking',
 u'bus',
 u'train',
 u'food',
 u'drink',
 u'venue food',
 u'programme',
 u'auction',
 u'talk',
 u'talks',
 u'archive',
 u'map',
 u'merchandise',
 u'shopping',
 u'CAPTION t-shirt',
 u'Damian Cugley',
 u'Woodrow Phoenix',
 u'Neill Cameron',
 u'game',
 u'Sarah McIntyre',
 u'photos art',
 u'art',
 u'site',
 u'Mad Science',
 u'Guests',
 u'workshop',
 u'guest',
 u'annoucement',
 u'link',
 u'timetable',
 u'Caption 2011',
 u'Austerity',
 u't-shirt',
 ]


# Mentioning isolated brackets in code confuses auto-indent,
# so here are subsitutes!
OPEN_PAREN, CLOSE_PAREN = '()'

data_dir = os.path.dirname(__file__)

needed_tables = set(['node', 'node_revisions', 'term_node', 'term_data', 'users'])
table_columns = {}
tables = {}

integer_start_re  = re.compile(r'[\d-]')
integer_continue_re  = re.compile(r'\d')
float_start_re  = re.compile(r'[.eE]')
float_continue_re = re.compile(r'[\d+-]')

def parse_values_lists(s):
    """Parse a comma-separated sequence of comma-separated values in parentheses.

    Values are SQL scalars: strings in '…', ints, and floats.
    """
    result = []
    state = 'a'
    #print s.encode('UTF-8')
    for (i, c) in enumerate(s):
        #print i, repr(c), state,
        if state == 'a':
            assert c == OPEN_PAREN
            values = []
            state = 'C'
        elif state == 'C':
            if c == "'":
                beg = i + 1
                state = 'Q'
                value = ''
            elif integer_start_re.match(c):
                beg = i
                state = 'N'
            elif c == 'N':
                beg = i
                state = 'K'
            else:
                print i, c, state
                assert c == CLOSE_PAREN, '%d: Expected CLOSE_PAREN, got %r' % (i, c)
                result.append(values)
                state = 'z'
        elif state == 'K':
            if c == ',' or c == ')':
                k = s[beg:i]
                assert k == 'NULL', 'Unklnown keyword %r' % k
                values.append(None)
                if c == ',':
                    state = 'C'
                else:
                    assert c == CLOSE_PAREN
                    result.append(values)
                    state = 'z'
        elif state == "Q":
            if c == "'":
                state = 'E'
            elif c == '\\':
                value += s[beg:i] # store what comes before the escape sequence
                state = 'B'
        elif state == 'E':
            if c == "'":
                # Standard SQL strings representation of single quote.
                state = "Q"
            else:
                value += s[beg:i - 1]
                values.append(value)
                if c == ',':
                    state = 'C'
                else:
                    assert c == CLOSE_PAREN
                    result.append(values)
                    state = 'z'
        elif state == 'B':
            # MySQL uses backslash to quote quotes in strings
            if c == 'r':
                pass
            elif c == 'n':
                value += '\n'
            else:
                value += c
            beg = i + 1
            state = 'Q'
        elif state == 'N':
            if float_start_re.match(c):
                state = 'F'
            elif integer_continue_re.match(c):
                pass
            else:
                values.append(int(s[beg:i]))
                if c == ',':
                    state = 'C'
                else:
                    assert c == CLOSE_PAREN
                    result.append(values)
                    state = 'z'
        elif state == 'F':
            if float_continue_re.match(c):
                pass
            else:
                values.append(float(s[beg:i]))
                if c == ',':
                    state = 'C'
                else:
                    assert c == CLOSE_PAREN
                    result.append(values)
                    state = 'z'
        elif state == 'z':
            assert c == ','
            state = 'a'
        else:
            assert False, 'Unknown state in FSM'
        #print '->', state
    assert state == 'z'
    return result


def slug_from_title(title):
    slug = slugify(title)
    if len(slug) > 50:
        p = slug.rfind('-', 20, 50)
        if p >= 20:
            slug = slug[:p]
        else:
            slug = slug[:50]
    return slug



# FInite-state machine operating one one line at a atime.

create_re = re.compile(r'CREATE\s+TABLE\s+`(?P<table_name>\w+)`\s+\(')
insert_re = re.compile(r'^INSERT INTO `(?P<table_name>\w+)` VALUES (?P<values>.*);$')
values_re = re.compile(r'\(([\w\s,\'-]+)\)')

def when_looking(line):
    global table_name, columns
    m = create_re.match(line)
    if m:
        table_name = m.group('table_name')
        columns = []
        return  when_create
    m = insert_re.match(line)
    if m:
        table_name = m.group('table_name')
        if table_name in needed_tables:
            values_part = m.group('values')
            rows = [dict(zip(table_columns[table_name], values))
                    for values in parse_values_lists(values_part)]
            tables.setdefault(table_name, []).extend(rows)

create_line_end_re = re.compile(r'\)[\w\s=]+;')
create_column_re = re.compile(r'`(?P<column>\w+)`.*,')

def when_create(line):
    global table_name, columns
    if create_line_end_re.match(line):
        table_columns[table_name] = columns
        return when_looking
    m = create_column_re.match(line)
    if m:
        column = m.group('column')
        columns.append(column)


state_func = when_looking
with open(os.path.join(data_dir, 'db-124m.sql'), 'r') as strm:
    for line0 in strm:
        line = line0.decode('UTF-8').strip()
        state_func = state_func(line) or state_func

nodes = tables['node']
node_revisions = tables['node_revisions']
terms = tables['term_data']
term_nodes = tables['term_node']
users = tables['users']

tags_by_term = {}
for term_title, tag_name in set(tag_names_by_term.items()):
    try:
        tag = Tag.objects.get(name=tag_name)
    except Tag.DoesNotExist:
        print 'Creating tag', tag_name
        tag = Tag.objects.create(name=tag_name)
    tags_by_term[term_title] = tag

site_admin = User.objects.get(id=1)

def datetime_from_timestamp(timestamp):
    dt = datetime.utcfromtimestamp(timestamp)
    dt = dt.replace(tzinfo=utc)
    return dt

class Protoarticle(object):
    def __init__(self, node):
        self.nid = node['nid']
        self.uid = node['uid']
        self.title = node['title']
        self.slug = slug_from_title(self.title)
        self.is_published = node['status']
        self.created = datetime_from_timestamp(node['created'])
        self.updated = datetime_from_timestamp(node['changed'])

        term_names = [t['name']
            for tn in term_nodes if tn['vid'] == n['vid']
            for t in terms if t['tid'] == tn['tid']]
        self.tags = set(tags_by_term[x] for x in term_names if x in tags_by_term)

        revision = next(r for r in node_revisions if r['vid'] == node['vid'])
        self.content = revision['body']
        teaser = revision['teaser']
        if teaser and teaser not in self.content:
            self.content = u'{0}\n---\n{1}'.format(teaser, self.content)
        self.format = revision['format']
        self.modified = datetime_from_timestamp(revision['timestamp'])

    def get_or_create_article(self):
        """Create the real article from this protoarticle."""
        try:
            drip_node = DripNode.objects.get(nid=self.nid)
            article = drip_node.article
            article.title = self.title
            article.content = self.content
            article.created = self.created
            article.updated = self.updated
            article.published = (self.created if self.is_published else None)
        except DripNode.DoesNotExist:
            article = Article.objects.create(author=site_admin,
                title=self.title, slug=self.slug,
                content=self.content,
                published=(self.created if self.is_published else None),
                created=self.created, updated=self.updated)
            user = next(u for u in users if u['uid'] == self.uid)
            drip_author, created = DripAuthor.objects.get_or_create(uid=self.uid,
                    defaults={'name': user['name'], 'mail': user['mail']})
            drip_node = DripNode.objects.create(article=article, author=drip_author, nid=self.nid)

        for tag in self.tags:
            if not article.tags.filter(name=tag.name).exists():
                article.tags.add(tag)
        article.save()
        return article


protoarticles = [Protoarticle(n) for n in nodes]

for proto in protoarticles:
    print proto.title, proto.slug, proto.is_published, proto.created, proto.updated,
    article = proto.get_or_create_article()
    print article.pk



print 'The end'