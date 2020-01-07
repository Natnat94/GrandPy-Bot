#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import requests

from config import ID_KEY, SECRET_KEY


class Localisation:
    """this class gather all the fonctions needed for the program"""

    def run(self, text="ou se trouve la tours eiffel"):
        """run the program"""
        result = {}
        question = self.parser(text)
        geoloc, address = self.map_api(question, "48.8482,2.3724;r=245799")
        result["here"] = geoloc
        result["address"] = address
        wiki = self.wiki_api(geoloc)
        result["wiki"] = wiki
        result["status"] = "true"
        return result

    def parser(self, text):
        """parse the input text and extract the place researched """
        regex = r"(ou se trouve|comment s'appelle|adresse|situe| \
                    trouve )(\s+)(?P<question>.*\b)?"
        test_str = text
        matches = re.finditer(regex, test_str)
        for r in matches:
            print(r.group("question"))
        return r.group("question")

    def map_api(self, name, zone):
        """send a request to the HERE API for the search's coordinates"""
        session = requests.Session()
        url = "https://places.demo.api.here.com/places/v1/discover/search"
        params = {
            "app_code": SECRET_KEY,
            "app_id": ID_KEY,
            "in": zone,
            "pretty": "True",
            "q": name,
            "result_types": "place"
        }
        request = session.get(url=url, params=params)
        data = request.json()
        address = data["results"]["items"][0]["vicinity"]
        address = address.replace("<br/>", " ")
        data = data["results"]["items"][0]["position"]
        data = [str(data[0]), str(data[1])]
        return data, address

    def wiki_api(self, localisation):
        """send a request to the Wikipedia API to find
            info about a localisation"""
        session = requests.Session()
        url = "https://fr.wikipedia.org/w/api.php"
        localisation = str(localisation[0])+"|"+str(localisation[1])
        params = {
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
        request = session.get(url=url, params=params)
        data = request.json()
        places = data['query']['pages']
        results = []
        for k in places:
            title = places[k]['title']
            abstract = places[k]['extract']
            thumbnail = places[k]['thumbnail']['source'] if \
                "thumbnail" in places[k] else ''
            article_url = places[k]['fullurl']
            place_loc = (places[k]['coordinates'][0]['lat'],
                         places[k]['coordinates'][0]['lon'])
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
