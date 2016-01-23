# PyScraping\scrapers\nfl.py

import os
import urllib2
from os_helpers import ensure_directory
from scrapers import Scraper

class NflScraper(Scraper):
    """Retrieves a NFL stat related pages."""
    
    __base_url = "http://www.nfl.com"
    __stats_url = "/stats/player?seasonId={0}&seasonType={1}&Submit=Go"
    
    def __init__(self, output_directory):
        """
        Initializes a NflScraper object.
        
        Args:
            output_directory (str): The directory path of where downloaded pages should be stored.
        """
        ensure_directory(output_directory)
        super(NflScraper, self).__init__()
        self.output_directory = output_directory
        self.build_opener(urllib2.HTTPSHandler(debuglevel=1))
        
    def scrape(self, year, season_type="REG"):
        """Retrieves a stat page from http://www.nfl.com based on the year and season type.
        
            The html page of statistics will be downloaded and saved as a file named
            "stats_{year}_{season_type}.html" and saved in the output directory taken
            when this scraper is initialized. For example, when retrieving statistical
            leaders for the 2015 regular season, the downloaded file will be written to
            <output_directory>\stats_2015_REG.html.
        
        Args:
            year (int): The year for which stats will be gathered. The year value should be 
                the year when the season started. For example, if you want data for the 
                2015-2016 NFL season, you will use 2015 here.
            season_type (str, optional): This is the type of season for which stats will be gathered. 
                Acceptable values include: ["PRE", "REG", "POST"] which respectively 
                corresponds to preseason, regular season, and post season.
                
        Raises:
            ValueError: If the season_type argument is not an accepted value.
        """
        if not season_type or season_type.upper() not in ["REG", "PRE", "POST"]:
            raise ValueError("season_type must be one of PRE, POST, or REG.")
        url = "{0}{1}".format(self.__base_url, self.__stats_url.format(year, season_type))
        print "Retrieving: [{0}]".format(url)
        html = self.get_html(url)
        outfile = os.path.join(self.output_directory, "stats_{0}_{1}.html".format(year, season_type))
        with open(outfile, "wb+") as f:
            f.write(html)