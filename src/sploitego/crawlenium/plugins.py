#!/usr/bin/env python

from xml.etree.cElementTree import XML
from re import compile, findall
from urlparse import urlsplit
from urllib import urlopen

from sploitego.crawlenium.crawler import CrawlerLifeCycle, CrawlerParsePlugin, CrawlerStartPlugin, CrawlQueue, WebHistory
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from sploitego.xmltools.objectify import stripns

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class FuzzyUrlMatcher(object):

    _qp = compile(r'&?([^=]+)=([^&]+)')
    _qs = compile(r'=([^&]+)')

    @classmethod
    def fuzzy_match(cls, left, right):
        left = cls.normalize(left)
        right = cls.normalize(right)
        return left == right or\
               (
                   left.scheme == right.scheme and
                   left.netloc == right.netloc and
                   (
                       left.path == right.path or
                       (
                           left.path in ['', '/'] and
                           right.path in ['', '/']
                           )
                       )
                   and cls.to_re(left.query).match(right.query) is not None
                   )

    @classmethod
    def normalize(cls, url):
        if isinstance(url, basestring):
            url = urlsplit(url)
        return url

    @classmethod
    def to_re(cls, qs):
        return compile(cls._qs.sub(r'=([^&]+)', qs))


class WebForm(object):

    def __init__(self, driver, e):
        self.driver = driver
        self.id = e.get_attribute('id') or ''
        self.name = e.get_attribute('name') or ''
        self.action = e.get_attribute('action') or ''
        self.method = e.get_attribute('method').upper() or ''
        self.enctype = e.get_attribute('enctype')
        self.selector = None
        self._element = e
        if self.id is not None and self.id:
            self.selector = '//form[@id="%s"]' % self.id
        elif self.name is not None and self.name:
            self.selector = '//form[@name="%s"]' % self.name
        elif self.action is not None and self.action:
            uri = self.uri(self.action)
            self.selector = '//form[@action="%s"]|//form[@action="%s"]|'\
                            '//form[@action="%s"]|//form[@action="%s"]|//form[@action="%s"]' % (
                self.action,
                self.action[self.action.find('/'):],
                uri,
                uri[1:],
                self.fragment(self.action)
                )

    @property
    def text_inputs(self):
        return self.form.find_elements_by_xpath('//input[@type="text"]')

    @property
    def password_inputs(self):
        return self.form.find_elements_by_xpath('//input[@type="password"]')

    @property
    def radio_inputs(self):
        return self.form.find_elements_by_xpath('//input[@type="radio"]')

    @property
    def checkbox_inputs(self):
        return self.form.find_elements_by_xpath('//input[@type="checkbox"]')

    @property
    def hidden_inputs(self):
        return self.form.find_elements_by_xpath('//input[@type="hidden"]')

    @property
    def file_inputs(self):
        return self.form.find_elements_by_xpath('//input[@type="file"]')

    @property
    def button_inputs(self):
        return self.form.find_elements_by_xpath('//input[@type="button"]')

    @property
    def image_inputs(self):
        return self.form.find_elements_by_xpath('//input[@type="image"]')

    @property
    def inputs(self):
        return self.form.find_elements_by_xpath('//input')

    @property
    def form(self):
        if self.selector is not None:
            return self.driver.find_element_by_xpath(self.selector)
        return self._element


    def uri(self, url):
        url = urlsplit(url)
        u = ''
        if url.path:
            u += url.path
        if url.query:
            u += '?%s' % url.query
        if url.fragment:
            u += '#%s' % url.fragment
        return u

    def fragment(self, url):
        url = urlsplit(url)
        if url.fragment:
            return url.fragment
        return '#'

    def submit(self):
        self.form.submit()


class AnchorSpider(CrawlerParsePlugin):

    def run_parse(self):
        print 'Crawling <a>s...'
        for u in self.crawler.anchors:
            url = u.get_attribute('href')
            if url is not None:
                if self.crawler.in_scope(url) and not self.crawler.has_visited(url):
                    print 'Queuing %s for crawl...' % url
                    self.crawler.queue_crawl(url)
        return CrawlerLifeCycle.CONTINUE


class WindowSpider(CrawlerParsePlugin):

    def run_parse(self):
        print 'Crawling <iframe>s...'
        for i in self.crawler.iframes + self.crawler.frames:
            try:
                self.crawler.driver.switch_to_frame(i)
                self.crawler.parse_crawl()
            except WebDriverException, w:
                print str(w)
        self.crawler.driver.switch_to_default_content()
        return CrawlerLifeCycle.CONTINUE


class FormSpider(CrawlerParsePlugin):

    _h = WebHistory()

    def run_parse(self):
        print 'Crawling <form>s'
        self.url = self.crawler.driver.current_url
        for f in [ WebForm(self.crawler.driver, f) for f in self.crawler.forms ]:
            if not self._h.has_visited(f.selector):
                print f.action, self._h
                print 'Fuzzing form %s' % f.selector
                self._h.add(f.selector)
                self.fuzz(f)
        return CrawlerLifeCycle.CONTINUE

    def fuzz(self, f):
        r = set()
        for i in f.inputs:
            if self.crawler.is_visible(i):
                type = i.get_attribute('type')
                name = i.get_attribute('name')
                if type in ['text', 'password']:
                    i.send_keys('test')
                elif type == 'radio' and name not in r:
                    i.click()
                    r.add(name)
                elif type == 'checkbox':
                    i.click()
        f.submit()
        self.crawler.queue_crawl(self.crawler.driver.current_url)
        self.crawler.driver.get(self.url)


class RobotsLinkExtractor(CrawlerStartPlugin):

    def run_start(self):
        print 'Extracting Robots Links'
        r = urlopen('%s://%s/robots.txt' % (self.crawler.scope.scheme, self.crawler.scope.netloc))
        if r.code == 200:
            d = r.read()
            for u in findall(r'^\s*(?:Allow|Disallow)\s*\:\s*(.+)$(?im)', d):
                print 'Queuing %s' % u
                self.crawler.queue_crawl(self.to_url(u))
            for u in findall(r'^\s*(?:Sitemap)\s*\:\s*(.+)$(?im)', d):
                self.parse_sitemap(u)
        return CrawlerLifeCycle.CONTINUE

    def parse_sitemap(self, u):
        print 'Exploring sitemap at %s' % u
        r = urlopen(u)
        if r.code == 200:
            if u.endswith('xml'):
                e = XML(stripns(r.read()))
                for l in e.findall('sitemap/loc/'):
                    self.parse_sitemap(l.text)
                for l in e.findall('url/loc'):
                    self.crawler.queue_crawl(l.text)

    def to_url(self, url):
        if url.startswith('http://') or url.startswith('https://'):
            return url
        return '%s://%s%s' % (self.crawler.scope.scheme, self.crawler.scope.netloc, url)






