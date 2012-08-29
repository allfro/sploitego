#!/usr/bin/env python

from httplib import urlsplit
from Queue import Queue

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class WebHistory(set):

    def has_visited(self, url):
        return url in self


class StateHistory(set):

    def has_visited(self, state):
        return state in self


class CrawlQueue(Queue):

    def __init__(self):
        Queue.__init__(self)
        self.history = WebHistory()

    def put(self, item, block=True, timeout=None):
        if not self.history.has_visited(item[0]):
            self.history.add(item[0])
            Queue.put(self, item, block, timeout)


class CrawlerPlugin(object):

    def __init__(self, crawler):
        self.crawler = crawler


class CrawlerPrePlugin(CrawlerPlugin):

    def run_pre(self, url, depth):
        return NotImplemented


class CrawlerPostPlugin(CrawlerPlugin):

    def run_post(self):
        return NotImplemented


class CrawlerParsePlugin(CrawlerPlugin):

    def run_parse(self):
        return NotImplemented


class CrawlerStartPlugin(CrawlerPlugin):

    def run_start(self):
        return NotImplemented


class CrawlerLifeCycle:

    END = -1
    CONTINUE = 0
    SKIP = 1


class Crawler(object):

    def __init__(self, driver=Firefox):
        self.driver = driver()
        self.action_chain = ActionChains(self.driver)
        self.q = CrawlQueue()
        self.scope = None
        self.depth = -1
        self.maxdepth = 0
        self._start_plugins = []
        self._pre_plugins = []
        self._parse_plugins = []
        self._post_plugins = []

    def register_plugin(self, plugin):
        if not issubclass(plugin, CrawlerPlugin):
            raise AttributeError('Expected CrawlerPlugin not %s', repr(type(plugin)))
        if issubclass(plugin, CrawlerPrePlugin):
            self._pre_plugins.append(plugin(self))
        if issubclass(plugin, CrawlerParsePlugin):
            self._parse_plugins.append(plugin(self))
        if issubclass(plugin, CrawlerPostPlugin):
            self._post_plugins.append(plugin(self))
        if issubclass(plugin, CrawlerStartPlugin):
            self._start_plugins.append(plugin(self))

    def start(self, url, maxdepth=3):
        if not url.startswith('http'):
            raise ValueError('Invalid URL %s; URL must start with either http:// or https://' % repr(url))
        self.maxdepth = maxdepth
        self.scope = urlsplit(url)
        lc = self._exec_start_plugins()
        if lc == CrawlerLifeCycle.END:
            return
        self.queue_crawl(url)
        self._crawl()

    @property
    def crawl_history(self):
        return [u.geturl() for u in self.q.history]

    def _crawl(self):
        lc = CrawlerLifeCycle.CONTINUE
        while not self.q.empty() and lc != CrawlerLifeCycle.END:
            url, self.depth = self.dequeue_crawl()
            print 'Crawling %s at depth %d' % (url.geturl(), self.depth)
            lc = self._exec_pre_plugins(url, self.depth)
            if lc == CrawlerLifeCycle.END:
                break
            elif lc == CrawlerLifeCycle.SKIP:
                continue
            if self.depth <= self.maxdepth:
                self.driver.get(url.geturl())
                lc = self.parse_crawl()
                if lc == CrawlerLifeCycle.END:
                    break
                elif lc == CrawlerLifeCycle.SKIP:
                    continue
            lc = self._exec_post_plugins()

    def parse_crawl(self):
        return self._exec_parse_plugins()

    def has_visited(self, url):
        return self.q.history.has_visited(urlsplit(self._defragment_url(url)))

    def queue_crawl(self, url):
        self.q.put((urlsplit(self._defragment_url(url)), self.depth + 1))

    def dequeue_crawl(self):
        return self.q.get()

    def is_visible(self, e):
        l = e.location
        return l['x'] > 0 and l['y'] > 0 and e.is_displayed()

    def mouse_over(self, e):
        if self.is_visible(e):
            self.action_chain.move_to_element(e)
            self.action_chain.perform()

    def mouse_right_click(self, e):
        if self.is_visible(e):
            self.action_chain.context_click(e)
            self.action_chain.perform()

    def in_scope(self, url):
        url = urlsplit(url)
        return url is not None and url.netloc == self.scope.netloc and url.path.startswith(self.scope.path)

    def _exec_pre_plugins(self, url, depth):
        for p in self._pre_plugins:
            lc = p.run_pre(url, depth)
            if lc != CrawlerLifeCycle.CONTINUE:
                return lc
        return CrawlerLifeCycle.CONTINUE

    def _exec_parse_plugins(self):
        for p in self._parse_plugins:
            lc = p.run_parse()
            if lc != CrawlerLifeCycle.CONTINUE:
                return lc
        return CrawlerLifeCycle.CONTINUE

    def _exec_post_plugins(self):
        for p in self._post_plugins:
            lc = p.run_post()
            if lc != CrawlerLifeCycle.CONTINUE:
                return lc
        return CrawlerLifeCycle.CONTINUE

    def _exec_start_plugins(self):
        for p in self._start_plugins:
            lc = p.run_start()
            if lc != CrawlerLifeCycle.CONTINUE:
                return lc
        return CrawlerLifeCycle.CONTINUE

    def _defragment_url(self, url):
        if '#' in url:
            return url[:url.find('#')]
        return url

    @property
    def anchors(self):
        return self.driver.find_elements(By.TAG_NAME, 'a') or []

    @property
    def frames(self):
        return self.driver.find_elements(By.TAG_NAME, 'frame') or []

    @property
    def links(self):
        return self.driver.find_elements(By.TAG_NAME, 'link') or []

    @property
    def iframes(self):
        return self.driver.find_elements(By.TAG_NAME, 'iframe') or []

    @property
    def objects(self):
        return self.driver.find_elements(By.TAG_NAME, 'object') or []

    @property
    def scripts(self):
        return self.driver.find_elements(By.TAG_NAME, 'script') or []

    @property
    def forms(self):
        return self.driver.find_elements(By.TAG_NAME, 'form') or []

    @property
    def page_source(self):
        return self.driver.page_source

    @property
    def user_agent(self):
        return self.driver.execute_script('return navigator.userAgent;')