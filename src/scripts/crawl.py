#!/usr/bin/env python
from random import randint

from urlparse import urlsplit
from urllib import urlencode

from sploitego.crawlenium.crawler import Crawler, CrawlerParsePlugin, CrawlerLifeCycle
from sploitego.crawlenium.plugins import AnchorSpider, FormSpider, WindowSpider, WebForm, RobotsLinkExtractor

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class HTTPRequest(object):

    def __init__(self, method, url, ua=''):
        self.method = method
        self.url = urlsplit(url)
        if self.url.scheme not in [ 'http', 'https' ]:
            raise NotImplementedError('Unknown scheme provided: %s' % self.url.scheme)
        self.headers = {}
        self.user_agent = ua
        self.params = {}
        self.content_type = ''
        self.cookies = {}

    def build(self):
        if self.method.upper() == 'POST':
            return self._build_post()
        elif self.method.upper() == 'GET':
            return self._build_get()
        raise NotImplementedError('Method %s not implemented yet.' % self.method)

    def _build_post(self):
        r = 'POST %s' % self.url.path
        if self.url.query:
            r += '?%s' % self.url.query
        if self.url.fragment:
            r += '#%s' % self.url.fragment
        r += ' HTTP/1.1\r\n'
        r += 'Host: %s \r\n' % self.url.netloc
        r += 'Cookie: %s\r\n' % '; '.join(['%s=%s' % (n, self.cookies[n]) for n in self.cookies])
        r += 'User-Agent: %s\r\n' % self.user_agent
        if self.content_type == 'application/x-www-form-urlencoded' or not self.content_type:
            r += 'Content-Type: %s\r\n' % self.content_type
            d = urlencode(self.params)
            r += 'Content-Length: %d\r\n\r\n' % len(d)
            r += d
        return r

    def _build_get(self):
        r = 'GET %s?' % self.url.path
        if self.params:
            if self.url.query:
                r += '&'.join([urlencode(self.params), self.url.query])
            else:
                r += urlencode(self.params)
        if self.url.fragment:
            r += '#%s ' % self.url.fragment
        r += ' HTTP/1.1\r\n'
        r += 'Host: %s \r\n' % self.url.netloc
        if self.cookies:
            r += 'Cookie: %s\r\n' % '; '.join(['%s=%s' % (n, self.cookies[n]) for n in self.cookies])
        if self.user_agent:
            r += 'User-Agent: %s\r\n' % self.user_agent
        for h in self.headers:
            r += '%s: %s\r\n' % (h, self.headers[h])
        r += '\r\n'
        return r


class FormRequestExtractor(CrawlerParsePlugin):

    def run_parse(self):
        print 'Extracting forms...'
        for f in [WebForm(self.crawler.driver, f) for f in self.crawler.forms]:
            try:
                self.build_request(f)
            except NotImplementedError:
                pass
        return CrawlerLifeCycle.CONTINUE

    def build_request(self, f):
        m = HTTPRequest(f.method, f.action, self.crawler.user_agent)
        m.params = [
        (
            i.get_attribute('name'),
            i.get_attribute('value')
            ) for i in f.inputs if i.get_attribute('type') in ['hidden', 'text', 'password', 'radio', 'checkbox']
        and i.get_attribute('name')
        ]
        m.cookies = dict(
            [ (c['name'], c['value']) for c in self.crawler.driver.get_cookies() ]
        )

        print m.build()


class SelectSelector(CrawlerParsePlugin):

    def run_parse(self):
        print 'Extracting <select>s'
        self.url = self.crawler.driver.current_url
        for s in self.crawler.driver.find_elements_by_xpath('//select'):
            if self.crawler.is_visible(s):
                name = s.get_attribute('name')
                print 'Selecting drop-down menu %s...' % name
                self.select(name)
        return CrawlerLifeCycle.CONTINUE

    def select(self, name):
        os = self.crawler.driver.find_element_by_xpath(
            '//select[@name="%s"]' % name
        ).find_elements_by_xpath('//option')
        os[randint(0, len(os)-1)].click()
        self.crawler.driver.get(self.url)





c = Crawler()

c.register_plugin(SelectSelector)
c.register_plugin(RobotsLinkExtractor)
c.register_plugin(FormRequestExtractor)
c.register_plugin(FormSpider)
c.register_plugin(AnchorSpider)
c.register_plugin(WindowSpider)

c.start('http://www.ncisl.com/', 1)
print c.crawl_history, len(c.crawl_history)