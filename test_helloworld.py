import parser_man as parser
import requests


def test_parser():
    pars = parser.parser("ou se situe le pantheon")
    assert pars == "le pantheon"

def test_wiki_api(monkeypatch):
    FAKE_API_RESULT= {'batchcomplete': '','query': {'pages': {'18618509': {'coordinates': [{'globe': 'earth',
                                                   'lat': 37.7891838,
                                                   'lon': -122.4033522,
                                                   'primary': ''}],
                                  'ns': 0,
                                  'pageid': 18618509,
                                  'title': 'Wikimedia Foundation'}}}}

    class MockRequestsGet:

        @staticmethod
        def json(self):
            return FAKE_API_RESULT

    monkeypatch.setattr('requests.get', MockRequestsGet)
    result = parser.wiki_api("Wikimedia Foundation")
    assert result == FAKE_API_RESULT

def test_map_api(monkeypatch):
    FAKE_API_RESULT= [48.85824, 2.2945]

    class MockRequestsGet:

        @staticmethod
        def json(self):
            return FAKE_API_RESULT

    monkeypatch.setattr('requests.get', MockRequestsGet)
    result = parser.map_api("Tour Eiffel", "48.8482,2.3724;r=245799")
    assert result['results']['items'][0]['position']  == FAKE_API_RESULT
