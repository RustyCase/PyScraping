# PyScraping\parsers\nfl.py

import json
import os
from bs4 import BeautifulSoup

class NflParser(object):
    
    def __init__(self, data_directory, output_directory):
        self.data_directory = data_directory
        self.output_directory = output_directory
        
    def parse(self):
        for htmlfile in os.listdir(self.data_directory):
            if "html" not in htmlfile:
                continue
            infile = os.path.join(self.data_directory, htmlfile)
            self.data = {}
            self._parse_html(infile)
            jsonfile = htmlfile.replace("html", "json")
            outfile = os.path.join(self.output_directory, jsonfile)
            with open(outfile, "wb+") as f:
                json.dump(self.players, f, indent=2)
            
    def  _parse_html(self, infile):
        html = open(infile, "rb+").read()
        soup = BeautifulSoup(html, "html5lib")
        self.players = {}
        player_containers = self._get_player_containers(soup)
        self._get_stat_leaders(player_containers[0], "passing-leaders")
        self._get_stat_leaders(player_containers[1], "rushing-leaders")
        self._get_stat_leaders(player_containers[2], "receiving-leaders")
        self._get_stat_leaders(player_containers[3], "tackle-leaders")
        self._get_stat_leaders(player_containers[4], "sack-leaders")
        self._get_stat_leaders(player_containers[5], "interception-leaders")

    def _get_player_containers(self, soup):
        player_containers = soup.find_all("div", attrs={ "class": "players"})
        print "Player Containers Found: [{0}]".format(len(player_containers))
        return player_containers
    
    def _get_stat_leaders(self, player_container, stat_key):
        stat_leaders = player_container.find_all("ul", attrs={ "class", "player-info" })
        self.players[stat_key] = []
        rank_counter = 1
        for pc in stat_leaders:
            player = self._get_player_stats(pc)
            player["rank"] = rank_counter
            self.players[stat_key].append(player)
            rank_counter = rank_counter + 1

    def _get_player_stats(self, player_container):
        player = {}
        player_name = self._get_player_name(player_container)
        player["name"] = player_name
        player_team = self._get_player_team(player_container)
        player["team"] = player_team
        player_stat = self._get_player_stat(player_container)
        player["stat"] = player_stat
        return player
            
            
    def _get_player_name(self, player_container):
        player_name_container = player_container.find("li", attrs={ "class", "name" }).find("a")
        player_name = player_name_container.string.strip()
        print "Name Found: [{0}]".format(player_name)
        return player_name
        
    def _get_player_team(self, player_container):
        player_team_container = player_container.find("li", attrs={ "class", "team" })
        player_team = player_team_container.string.strip()
        print "Team Found: [{0}]".format(player_team)
        return player_team
        
    def _get_player_stat(self, player_container):
        player_stat_container = player_container.find("li", attrs={ "class", "stat" })
        player_stat = player_stat_container.string.strip()
        print "Stat Found: [{0}]".format(player_stat)
        return player_stat