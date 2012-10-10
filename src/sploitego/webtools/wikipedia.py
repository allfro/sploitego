#!/usr/bin/env python

from json.decoder import JSONDecoder
from httplib import HTTPConnection
from urllib import urlencode

from canari.config import config

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class WikipediaError(Exception):
    pass


def usercontribs(**kwargs):
    """Get all edits by a user

    This module requires read rights
    Parameters:
    uclimit             - The maximum number of contributions to return
                        No more than 500 (5000 for bots) allowed
                        Default: 10
    ucstart             - The start timestamp to return from
    ucend               - The end timestamp to return to
    uccontinue          - When more results are available, use this to continue
    ucuser              - The users to retrieve contributions for
    ucuserprefix        - Retrieve contibutions for all users whose names begin with this value. Overrides ucuser
    ucdir               - In which direction to enumerate
                         newer          - List oldest first. Note: ucstart has to be before ucend.
                         older          - List newest first (default). Note: ucstart has to be later than ucend.
                        One value: newer, older
                        Default: older
    ucnamespace         - Only list contributions in these namespaces
                        Values (separate with '|'): 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 100, 101, 108, 109
                        Maximum number of values 50 (500 for bots)
    ucprop              - Include additional pieces of information
                         ids            - Adds the page ID and revision ID
                         title          - Adds the title and namespace ID of the page
                         timestamp      - Adds the timestamp of the edit
                         comment        - Adds the comment of the edit
                         parsedcomment  - Adds the parsed comment of the edit
                         size           - Adds the size of the page
                         flags          - Adds flags of the edit
                         patrolled      - Tags patrolled edits
                         tags           - Lists tags for the edit
                        Values (separate with '|'): ids, title, timestamp, comment, parsedcomment, size, flags, patrolled, tags
                        Default: ids|title|timestamp|comment|size|flags
    ucshow              - Show only items that meet this criteria, e.g. non minor edits only: ucshow=!minor
                        NOTE: if ucshow=patrolled or ucshow=!patrolled is set, revisions older than $wgRCMaxAge (2592000) won't be shown
                        Values (separate with '|'): minor, !minor, patrolled, !patrolled
    uctag               - Only list revisions tagged with this tag
    uctoponly           - Only list changes which are the latest revision
    """

    diff = set(kwargs).difference([
        'uclimit',
        'ucstart',
        'ucend',
        'uccontinue',
        'ucuser',
        'ucuserprefix',
        'ucdir',
        'ucnamespace',
        'ucprop',
        'ucshow',
        'uctag',
        'uctoponly'
    ])

    if diff:
        raise TypeError('Unknown parameter(s): %s' % ', '.join(diff))

    if not any([ i in kwargs for i in ['ucuser', 'ucuserprefix'] ]):
        raise TypeError('Must specify either ucuser or ucuserprefix keyword args.')


    params = {
        'uclimit' : kwargs.get('uclimit', 10),
        'ucdir' : kwargs.get('ucdir', 'older'),
        'ucprop' : kwargs.get('ucprop', 'ids|title|timestamp|comment|parsedcomment|size|flags|tags')
    }

    params.update(kwargs)

    results = []
    headers = { "User-Agent" : "Mozilla Firefox" }

    c = HTTPConnection("en.wikipedia.org")
    c.request(
        "GET",
        "/w/api.php?apihighlimits=true&action=query&format=json&list=usercontribs&%s" % urlencode(params),
        headers=headers
    )

    r = c.getresponse()

    if r.status == 200:
        result = JSONDecoder().decode(r.read())

        if 'error' in result:
            raise WikipediaError('%s: %s' % (result['error']['info'], result['error']['code']))

        results.extend(result['query']['usercontribs'])

        if 'query-continue' in result:
            i = len(result['query']['usercontribs'])
            while 'query-continue' in result and 'uccontinue' in result['query-continue']['usercontribs'] and \
                  i < config['wikipedia/maxresults']:
                params['uccontinue'] = result['query-continue']['usercontribs']['uccontinue']
                c.request(
                    "GET",
                    "/w/api.php?apihighlimits=true&action=query&format=json&list=usercontribs&%s" % urlencode(params),
                    headers=headers
                )
                r = c.getresponse()
                if r.status == 200:
                    result = JSONDecoder().decode(r.read())
                    results.extend(result['query']['usercontribs'])
                    i += len(result['query']['usercontribs'])
                else:
                    break

    return results
