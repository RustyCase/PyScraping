# PyScraping\scrapers\__init__.py

import cookielib
import urllib2

class Scraper(object):
    
    __chrome_headers = [
        ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"),
        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
        ("Accept-Language", "en-US,en;q=0.8")
    ]
    
    def __init__(self):
        self.cookie_jar = cookielib.CookieJar() 
    
    def build_opener(self, *args):
        handlers = list(args)
        handlers.append(urllib2.HTTPCookieProcessor(self.cookie_jar))
        self.opener = urllib2.build_opener(*handlers)
        
    def get_html(self, url, data=None):
        
        response = self.opener.open(url, data, 60)
        html = response.read()
        response.close()
        return html