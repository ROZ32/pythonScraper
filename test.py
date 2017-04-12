from simpleScraper import SimpleScraper
import io
import codecs
import os
import sys

test = SimpleScraper()
result = test.get_scraped_data('google.com')
print result

here = os.path.abspath(os.path.dirname(__file__))
print here