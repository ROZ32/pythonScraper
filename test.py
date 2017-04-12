from simpleScraper import SimpleScraper

test = SimpleScraper()
result = test.get_scraped_data('www.google.com')
print result

print 'test'

# from bs4 import BeautifulSoup
# myHTML = "<html><head></heda><body><strong>Hi</strong></body></html>"
# soup = BeautifulSoup(myHTML, "lxml")