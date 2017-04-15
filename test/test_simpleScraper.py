from mock import patch, Mock
from simplescraper import SimpleScraper
import os
import codecs
import sys

if sys.version_info[0] < 3:
	callableClass = 'urllib2.urlopen'
else:
	callableClass = 'urllib.request.urlopen'

def get_request_mock(success=True):
	read_data = []
	code_status = []
	request_mock = Mock()
	#set multiple response codes 200 for each call
	if success is True:
		read_data = [codecs.open("test/test.html", 'r').read()]
		code_status = [200,200,200,200,200]
	else:
		read_data = ['error']
		code_status = [404,404,404,404,404]
	request_mock.getcode.side_effect = code_status
	request_mock.read.side_effect = read_data
	return request_mock

@patch(callableClass)
def test_full_https_path(mock_urlopen):
	mock_urlopen.return_value = get_request_mock()
	test = SimpleScraper()
	result = test.get_scraped_data('https://www.google.com')
	assert len(result) > 0

@patch(callableClass)
def test_full_http_path(mock_urlopen):
	mock_urlopen.return_value = get_request_mock()
	test = SimpleScraper()
	result = test.get_scraped_data('http://www.google.com')
	assert len(result) > 0

@patch(callableClass)
def test_full_path(mock_urlopen):
	mock_urlopen.return_value = get_request_mock()
	test = SimpleScraper()
	result = test.get_scraped_data('www.google.com')
	assert len(result) > 0

@patch(callableClass)
def test_path(mock_urlopen):
	mock_urlopen.return_value = get_request_mock()
	test = SimpleScraper()
	result = test.get_scraped_data('google.com')
	assert len(result) > 0

@patch(callableClass)
def test_malformed_path(mock_urlopen):
	mock_urlopen.return_value = get_request_mock(success=False)
	test = SimpleScraper()
	result = test.get_scraped_data('.google.com')
	assert 'error' in result

def test_no_content_provided():
	test = SimpleScraper()
	result = test.get_scraped_data('')
	assert 'error' in result
