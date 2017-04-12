from pythonScraper import SimpleScraper

def test_full_https_path():
	test = SimpleScraper()
	result = test.get_scraped_data('https://www.google.com')
	assert len(result) > 0

def test_full_http_path():
	test = SimpleScraper()
	result = test.get_scraped_data('http://www.google.com')
	assert len(result) > 0

def test_full_path():
	test = SimpleScraper()
	result = test.get_scraped_data('www.google.com')
	assert len(result) > 0

def test_path():
	test = SimpleScraper()
	result = test.get_scraped_data('google.com')
	assert len(result) > 0

def test_malformed_path():
	test = SimpleScraper()
	result = test.get_scraped_data('.google.com')
	assert len(result) == 0