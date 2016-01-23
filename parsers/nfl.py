# PyScraping\parsers\nfl.py

import json
import os
from bs4 import BeautifulSoup
from os_helpers import ensure_directory

class NflParser(object):
    """Parses the html of NflScraper downloaded stat pages into json."""
    
    def __init__(self, data_directory, output_directory):
        """Initializes a NflParser object.
        
        Args:
            data_directory (str): Path to a directory containing downloaded stat pages.
            output_directory(str): Path to a directory where parsed content will 
                be saved.
        """
        ensure_directory(output_directory)
        self.data_directory = data_directory
        self.output_directory = output_directory
        
    def parse(self):
        """Parses all html files found in the data_directory.
        
        This function will output a corresponding *.json
        file for each *.html file found. 
        """
        for htmlfile in os.listdir(self.data_directory):
            if "html" not in htmlfile:
                continue
            # The infile should be a downloaded stat page from http://www.nfl.com
            infile = os.path.join(self.data_directory, htmlfile)
            # We're going to instantiate a dictionary that will
            # hold our player content we're interested in.
            self.players = {}
            # Let's parse some stats from our file...
            self._parse_html(infile)
            # After our file has been parsed we will end up with a much more
            # useable and friendly dictionary of player stat data. It will look
            # something like:
            # {
            #    "receiving-leaders": [
            #        {
            #            "stat": "1681", "name": "Calvin Johnson", "rank": 1, "team": "DET"
            #        },
            #        ...
            #    ],
            #    ...
            # }
            # All that's left is to dump our self.players dict to a json file...
            jsonfile = htmlfile.replace("html", "json")
            outfile = os.path.join(self.output_directory, jsonfile)
            with open(outfile, "wb+") as f:
                json.dump(self.players, f, indent=2)
            
    def  _parse_html(self, infile):
        """Parses the infile, extracting out the stats data
        into a more useable format.
        
        Args:
            infile (str): The path to a HTML file containing the data.
        """
        html = open(infile, "rb+").read()
        # We're going to use the BeautifulSoup library in conjuction with 
        # the "html5lib" parser to pull the data from the html files.
        # More information can be found here: 
        #     http://www.crummy.com/software/BeautifulSoup/bs4/doc/
        soup = BeautifulSoup(html, "html5lib")
        # The stats page groups the stat leaders into containers
        # per the statistical category. Let's get these containers...
        player_containers = self._get_player_containers(soup)
        # As of this writing, the stats page will display the 
        # top five performers in six statistical categories:
        #     1. Passing
        #     2. Rushing
        #     3. Receiving
        #     4. Tackles
        #     5. Sacks
        #     6. Interceptions
        # We are going to to parse the player containers by these categories...
        self._get_stat_leaders(player_containers[0], "passing-leaders")
        print "Parsed: [passing-leaders]"
        self._get_stat_leaders(player_containers[1], "rushing-leaders")
        print "Parsed: [rushing-leaders]"
        self._get_stat_leaders(player_containers[2], "receiving-leaders")
        print "Parsed: [receiving-leaders]"
        self._get_stat_leaders(player_containers[3], "tackle-leaders")
        print "Parsed: [tackle-leaders]"
        self._get_stat_leaders(player_containers[4], "sack-leaders")
        print "Parsed: [sack-leaders]"
        self._get_stat_leaders(player_containers[5], "interception-leaders")
        print "Parsed: [interception-leaders]"

    def _get_player_containers(self, soup):
        """Extracts the player container groups.
        
        Args:
            soup (object): A BeatifulSoup object.
        """
        # When inspecting the source of the downloaded html file, the section we're 
        # interested in is going to look something like:
        #<div class="players" id="yui_3_10_3_1_1453493376158_1167">
        #   <div class="headshot" id="yui_3_10_3_1_1453493376158_1183"><img src="http://static.nfl.com/static/content/public/static/img/getty/headshot/B/R/E/BRE229498.jpg"></div>
        #   <ul class="player-info active" data-headshot="http://static.nfl.com/static/content/public/static/img/getty/headshot/B/R/E/BRE229498.jpg" id="yui_3_10_3_1_1453493376158_1189">
        #      <li class="name" id="yui_3_10_3_1_1453493376158_1222">
        #         1. 
        #         <a href="/player/drewbrees/2504775/profile" onclick="s_objectID=&quot;file:///D:/player/drewbrees/2504775/profile_1&quot;;return this.s_oc?this.s_oc(e):true" id="yui_3_10_3_1_1453493376158_1221">
        #         Drew Brees
        #         </a>
        #      </li>
        #      <li class="team">
        #         NO
        #      </li>
        #      <li class="stat">
        #         4870
        #      </li>
        #   </ul>
        #   ... Section omitted for brevity ...
        #   <div class="clear" id="yui_3_10_3_1_1453493376158_1188"></div>
        #</div>
        # All the information is contained in a div with the .players class. This makes for
        # a convenient filter to use when traversing the html.
        # For more information see:
        #    http://www.crummy.com/software/BeautifulSoup/bs4/doc/#kinds-of-filters
        player_containers = soup.find_all("div", attrs={ "class": "players"})
        print "Player Containers Found: [{0}]".format(len(player_containers))
        return player_containers
    
    def _get_stat_leaders(self, player_container, stat_key):
        """Extracts the stat leaders for the player container.
        
        Args:
            player_container (object): A BeautifulSoup object containing player data.
            stat_key (str): A key that will be used to group these players in
                    the players dict.
        """
        # We can see that each player is contained in an ul within the 
        # player_container.
        #   <ul class="player-info active" data-headshot="http://static.nfl.com/static/content/public/static/img/getty/headshot/B/R/E/BRE229498.jpg" id="yui_3_10_3_1_1453493376158_1189">
        #      <li class="name" id="yui_3_10_3_1_1453493376158_1222">
        #         1. 
        #         <a href="/player/drewbrees/2504775/profile" onclick="s_objectID=&quot;file:///D:/player/drewbrees/2504775/profile_1&quot;;return this.s_oc?this.s_oc(e):true" id="yui_3_10_3_1_1453493376158_1221">
        #         Drew Brees
        #         </a>
        #      </li>
        #      <li class="team">
        #         NO
        #      </li>
        #      <li class="stat">
        #         4870
        #      </li>
        #   </ul>
        # These ul tags are given the .player-info class, so we'll filter on that...
        stat_leaders = player_container.find_all("ul", attrs={ "class", "player-info" })
        self.players[stat_key] = []
        rank_counter = 1
        for pc in stat_leaders:
        # Iterate the stat_leaders and store them in the self.players dict.
            player = self._get_player_stats(pc)
            player["rank"] = rank_counter
            self.players[stat_key].append(player)
            rank_counter = rank_counter + 1

    def _get_player_stats(self, player_container):
        """Extracts the stats from the given player_container.
        
        Args:
            player_container (object): A BeautifulSoup object containing player information.
        """
        # Lets instantiate a dict to house the player's information.
        player = {}
        # Each of the following call will pull a piece of information
        # from the html file that we're interested in...
        player_name = self._get_player_name(player_container)
        player["name"] = player_name
        player_team = self._get_player_team(player_container)
        player["team"] = player_team
        player_stat = self._get_player_stat(player_container)
        player["stat"] = player_stat
        # We now have a dictionary containing the player's information.
        return player
            
    def _get_player_name(self, player_container):
        """Extrancts a player's name from the player_container.
        
        Args:
            player_container (object): A BeautifulSoup object containing player information.
        """
        player_name_container = player_container.find("li", attrs={ "class", "name" }).find("a")
        player_name = player_name_container.string.strip()
        return player_name
        
    def _get_player_team(self, player_container):
        """Extrancts a player's team from the player_container.
        
        Args:
            player_container (object): A BeautifulSoup object containing player information.
        """
        player_team_container = player_container.find("li", attrs={ "class", "team" })
        player_team = player_team_container.string.strip()
        return player_team
        
    def _get_player_stat(self, player_container):
        """Extrancts a player's stat value from the player_container.
        
        Args:
            player_container (object): A BeautifulSoup object containing player information.
        """
        player_stat_container = player_container.find("li", attrs={ "class", "stat" })
        player_stat = player_stat_container.string.strip()
        return player_stat