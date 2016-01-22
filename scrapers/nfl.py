# PyScraping\scrapers\nfl.py

import os
import urllib2
from scrapers import Scraper

class NflScraper(Scraper):
    
    __base_url = "http://www.nfl.com"
    __stats_url = "/stats/player?seasonId={0}&seasonType={1}&Submit=Go"
    
    def __init__(self, output_directory):
        super(NflScraper, self).__init__()
        self.output_directory = output_directory
        self.build_opener(urllib2.HTTPSHandler(debuglevel=1))
        
    def scrape(self, year, season_type="REG"):
        print "{0}::scrape".format(self.__class__.__name__)
        url = "{0}{1}".format(self.__base_url, self.__stats_url.format(year, season_type))
        html = self.get_html(url)
        outfile = os.path.join(self.output_directory, "stats_{0}_{1}.html".format(year, season_type))
        with open(outfile, "wb+") as f:
            f.write(html)