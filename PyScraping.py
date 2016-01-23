# PyScraping.py
"""A simple driver file demonstrating web scraping and parsing in Python."""

import os
from datetime import date
from parsers.nfl import NflParser
from scrapers.nfl import NflScraper

# =============================================================================
# Scraping NFL Stat pages
# 
# 1. Define the output directory where scraped stat files will be saved.
current_directory = os.path.dirname(os.path.abspath(__file__))
nfl_directory = os.path.join(current_directory, "nfl_example")
# 2. Initialize the scraper
nfl_scraper = NflScraper(nfl_directory)
# 3. For this demonstration, we're going to going to get the regular season
#    stat leaders for the last 5 years.
current_year = date.today().year
for cy in range(current_year-5, current_year):
    nfl_scraper.scrape(cy)
# 4. Define the directory where parsed content will be saved.
nfl_parsed_dir = os.path.join(nfl_directory, "parsed")
# 5. Initialize the parser
nfl_parser = NflParser(nfl_directory, nfl_parsed_dir)
# 6. Parse the downloaded content into a more useable format.
nfl_parser.parse()