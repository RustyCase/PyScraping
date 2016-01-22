
import os
import urllib2
from scrapers.nfl import NflScraper
from parsers.nfl import NflParser

output_directory = os.path.dirname(os.path.abspath(__file__))
print "Output Directory: [{0}]".format(output_directory)
s = NflScraper(output_directory)
s.scrape(2014)

p = NflParser(output_directory, os.path.join(output_directory, "parsed"))
p.parse()
