"""simplescraper
simplescraper uses a pluggable XML or HTML parser to parse a
(possibly invalid) document into a tree representation and get the content
OG tags, meta tags and link tags. simplescraper provides method that make it easy to
get the content of the scraped website

simplescraper works with Python 2.7 It works better if lxml
and/or html5lib is installed.

For more than you ever wanted to know about simplescraper, see the
documentation:
TODO
"""

__author__ = "Oscar Sanchez"
__authormail__ = "hmax dot bf4 at gmail dot com"
__version__ = "0.1.2"
__copyright__ = "Copyright (c) 2017 Oscar Sanchez"
__license__ = "MIT License"

from .scraper import SimpleScraper

__all__ = ['SimpleScraper']