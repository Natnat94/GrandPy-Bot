#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import json
from pprint import pprint

class Localisation:

    def run(self, text = "ou se trouve la tours eiffel"):
        result = {}
        question = self.parser(text)
        geoloc, address = self.map_api(question, "48.8482,2.3724;r=245799")
        result["here"] = geoloc
        result["address"] = address
        wiki = self.wiki_api(geoloc)
        result["wiki"] = wiki
        # pprint(result)
        with open("result.json", "w") as write_file:
            json.dump(result, write_file)
        return result
    
    def parser(self, text = "ou se trouve la tours eiffel"):
        regex = r"(ou se trouve|comment s'apelle|adresse|situe)(\s+)(?P<question>.*\b)?"
        test_str = text
        matches = re.finditer(regex, test_str)
        for r in matches:
            print(r.group("question"))
        return r.group("question")

    def map_api(self, name, zone):
        S = requests.Session()
        URL = "http://places.demo.api.here.com/places/v1/discover/search"
        PARAMS = {
            "app_code": "AJKnXv84fjrb0KIHawS0Tg",
            "app_id": "DemoAppId01082013GAL",
            "in": zone,
            "pretty": "True",
            "q": name,
            "result_types": "place"
        }
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        pprint(DATA)
        address = DATA["results"]["items"][0]["vicinity"]
        address = address.replace("<br/>"," ")
        DATA = DATA["results"]["items"][0]["position"]
        DATA = [str(DATA[0]), str(DATA[1])]
        return DATA, address

    def wiki_api(self, localisation):

        S = requests.Session()
        URL = "https://fr.wikipedia.org/w/api.php"
        localisation = str(localisation[0])+"|"+str(localisation[1])
        PARAMS = {
        "format": "json",
        "generator": "geosearch",
        "prop": "coordinates|pageimages|extracts|info",
        "inprop": "url",
        "pithumbsize": 144,
        "ggscoord": localisation,
        "ggslimit": "5",
        "ggsradius": "10000",
        "action": "query",
        "exintro": "True",
        "explaintext": "True",
        }
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        with open("data_file.json", "w") as write_file:
            json.dump(DATA, write_file)
        places = DATA['query']['pages']
        results = []
        for k in places:
            title = places[k]['title']
            abstract = places[k]['extract']
            thumbnail = places[k]['thumbnail']['source'] if "thumbnail" in places[k] else ''
            article_url = places[k]['fullurl']
            place_loc = (places[k]['coordinates'][0]['lat'], places[k]['coordinates'][0]['lon'])

            results.append({
                'title': title,
                'abstract': abstract,
                'thumbnail': thumbnail,
                'articleUrl': article_url,
                'localisation': place_loc})
        return results

if __name__ == "__main__":
    app = Localisation()
    app.run()