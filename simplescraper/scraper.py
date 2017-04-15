from bs4 import BeautifulSoup

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib.error import URLError
    from urllib.error import HTTPError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    from urllib2 import URLError
    from urllib2 import HTTPError

try:
    # For Python 3.0 and later
    from urllib.parse import urlparse
except ImportError:
    # Fall back to Python 2's urlparse
    from urlparse import urlparse

try:
    from simplejson import loads, dumps
except ImportError:
    from json import loads, dumps


TITLE = "title"
NAME = "name"
ITEMPROP = "itemprop"
URL = "url"
SECURE_URL = "secure_url"
HEIGHT = "height"
WIDTH = "width"
HREF_PROPERTY = "href"
META_TAG = "meta"
LINK_TAG = "link"
SOURCE = "source"
IMAGE = "image"
VIDEO = "video"
TYPE = "type"
CONTENT = "content"
PROPERTY = "property"
DESCRIPTION = "description"
KEYWORDS = "keywords"
THEME_COLOR = "theme-color"
OG = "og:"
DEFAULT_HTML_PARSER = "html5lib"
DEFAULT_HTML5_VIDEO_EMBED = "text/html"
INFORMATION_SPACE = "www."
HTTP_PROTOCOL = "http"
HTTP_PROTOCOL_NORMAL = "http://"
SECURE_HTTP_PROTOCOL = "https://"


class SimpleScraper():
    """docstring for SimpleScraper"""
        
    def get_scraped_data(self, link_to_scrap):
        try:
            result = {}
            if link_to_scrap == "":
                return {
                    "error": "Did not get a valid link"
                }
            try:
                if (link_to_scrap.find(INFORMATION_SPACE) == -1 and link_to_scrap.find(HTTP_PROTOCOL) == -1):
                    link_to_scrap = HTTP_PROTOCOL_NORMAL + INFORMATION_SPACE + link_to_scrap
                    requestResult = self.__get_request_content(link_to_scrap)

                    # try secure protocol
                    request_code = requestResult.getcode()
                    if request_code < 200 and request_code > 400:
                        link_to_scrap = SECURE_HTTP_PROTOCOL + INFORMATION_SPACE + link_to_scrap
                        requestResult = self.__get_request_content(link_to_scrap)

                elif (link_to_scrap.find(HTTP_PROTOCOL) == -1):
                    link_to_scrap = HTTP_PROTOCOL_NORMAL + link_to_scrap
                    requestResult = self.__get_request_content(link_to_scrap)

                    # try secure protocol
                    request_code = requestResult.getcode()
                    if request_code < 200 and request_code > 400:
                        link_to_scrap = SECURE_HTTP_PROTOCOL + link_to_scrap
                        requestResult = self.__get_request_content(link_to_scrap)

                else:
                    requestResult = self.__get_request_content(link_to_scrap)
            except Exception as e:
                return {
                    "error": "cannot scrap the provided url", 
                    "reason": e.args[0]
                }
            request_code = requestResult.getcode()
            if request_code >= 200 and request_code <= 400:
                page = requestResult.read()
                soup = BeautifulSoup(page, DEFAULT_HTML_PARSER)
                all_meta_tags = soup.find_all(META_TAG)
                all_link_tags = soup.find_all(LINK_TAG, {"rel": "canonical"})
                default_title = soup.find(TITLE)
                for tag in all_meta_tags:
                    result = self.__verifyTagName(result, tag)
                    if TITLE not in result and default_title is not None:
                        result[TITLE] = default_title.contents[0]
                result = self.__verifyTagOpenGraph(result, all_meta_tags)
                for tag in all_link_tags:
                    href = tag.get(HREF_PROPERTY)
                    if href is not None:
                        if HTTP_PROTOCOL in href:
                            result[URL] = href
                if URL not in result:
                    result[URL] = link_to_scrap
                result[SOURCE] = urlparse(link_to_scrap).netloc
                if IMAGE in result:
                    if result[IMAGE].find(HTTP_PROTOCOL) == -1:
                        result[IMAGE] = HTTP_PROTOCOL_NORMAL + result[SOURCE] + result[IMAGE]

            return result
        except StandardError as e:
            return {
                "error": "cannot scrap the provided url", 
                "reason": e.args[0]
            }


    def __get_request_content(self, link):
        try:
            return urlopen(link)
        except URLError as e:
            raise Exception (
                    "cannot get url content %s" % str(e.reason)
                )
        except HTTPError as e:
            raise Exception (
                    "cannot make http request %s" % str(e.reason)
                )


    def __verifyTagName(self, result, tag):
        tag_content = tag.get(CONTENT)
        tag_to_search = tag.get(NAME)
        if tag_to_search is None:
            tag_to_search = tag.get(PROPERTY)
        if tag_to_search is None:
            tag_to_search = tag.get(ITEMPROP)
        if tag_to_search is not None and tag_content is not None:
            if TITLE == tag_to_search.lower() and TITLE not in result:
                result[TITLE] = tag_content
            if DESCRIPTION == tag_to_search.lower() and DESCRIPTION not in result:
                result[DESCRIPTION] = tag_content
            if IMAGE == tag_to_search.lower() and IMAGE not in result:
                result[IMAGE] = tag_content
        return result


    def __verifyTagOpenGraph(self, result, all_tags):
        open_graph_objects = {}
        searching_iter_name = first_sub_element = last_sub_element = last_element = None

        for index, tag in enumerate(all_tags):
            tag_content = tag.get(CONTENT)
            tag_to_search = tag.get(PROPERTY)
            if tag_to_search is None:
                tag_to_search = tag.get(NAME)
            if tag_to_search is None:
                tag_to_search = tag.get(ITEMPROP)
            if tag_to_search is not None:
                if OG in tag_to_search:
                    first_iteration = tag_to_search.find(":")
                    second_iteration = tag_to_search.find(":", first_iteration + 1)
                    if second_iteration == -1:
                        tag_og_title = tag_to_search.find(TITLE, first_iteration)
                        if TITLE not in result and tag_og_title != -1 and tag_to_search is not None:
                            result[TITLE] = tag_content
                        tag_og_description = tag_to_search.find(DESCRIPTION, first_iteration)
                        if DESCRIPTION not in result and tag_og_description != -1 and tag_to_search is not None:
                            result[DESCRIPTION] = tag_content
                        tag_og_image = tag_to_search.find(IMAGE, first_iteration)
                        if IMAGE not in result and tag_og_image != -1 and tag_to_search is not None:
                            result[IMAGE] = tag_content
                        if tag_og_title != -1 or tag_og_description != -1 or tag_og_image != -1:
                            open_graph_objects[tag_to_search[first_iteration + 1:]] = tag_content
                    else:
                        iter_name = tag_to_search[first_iteration + 1:second_iteration]
                        if searching_iter_name is None:
                            searching_iter_name = iter_name
                            open_graph_objects[searching_iter_name] = []
                        if iter_name != searching_iter_name:
                            searching_iter_name = first_sub_element = last_element = last_sub_element = None
                        else:
                            sub_element = tag_to_search[second_iteration + 1:]
                            if first_sub_element is None:
                                first_sub_element = sub_element
                                actual_object = {}
                                actual_object[first_sub_element] = tag_content
                            elif first_sub_element == sub_element:
                                open_graph_objects[searching_iter_name].append(actual_object)
                                actual_object = {}
                                actual_object[first_sub_element] = tag_content
                                last_sub_element = last_element
                                last_element = None
                            else:
                                if last_element == last_sub_element and last_sub_element is not None and last_element is not None:
                                    open_graph_objects[searching_iter_name].append(actual_object)
                                    first_sub_element = sub_element
                                    actual_object = {}
                                    actual_object[first_sub_element] = tag_content
                                else:
                                    last_element = sub_element
                                    actual_object[sub_element] = tag_content

        # check for youtube og video properties for embed iframe
        if VIDEO in open_graph_objects:
            for elem in open_graph_objects[VIDEO]:
                if TYPE in elem:
                    if elem[TYPE] == DEFAULT_HTML5_VIDEO_EMBED:
                        if SECURE_URL in elem:
                            iframe = '<iframe src="%s"' % elem[SECURE_URL]
                            if HEIGHT in elem:
                                iframe = iframe + ' height="%s"' % elem[HEIGHT]
                            if WIDTH in elem:
                                iframe = iframe + ' width="%s"' % elem[WIDTH]
                            iframe = iframe + '></iframe>'
                            result["iframe"] = iframe
                        elif URL in elem:
                            iframe = "<iframe src=" + elem[URL]
                            if HEIGHT in elem:
                                iframe = iframe + ' height="%s"' % elem[HEIGHT]
                            if WIDTH in elem:
                                iframe = iframe + ' width="%s"' % elem[WIDTH]
                            iframe = iframe + '></iframe>'
                            result["iframe"] = iframe
        return result
