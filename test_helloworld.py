from parser_man import Localisation as localisation
import requests


def test_parser():
    pars = localisation()
    rien = pars.parser("ou se situe le pantheon")
    assert rien == "le pantheon"

def test_wiki_api(monkeypatch):
    FAKE_API_RESULT={"batchcomplete": "",
                    "query": {
                        "pages": {
                            "1359783": {
                                "pageid": 1359783,
                                "ns": 0,
                                "title": "Tour Eiffel",
                                "index": -1,
                                "coordinates": [
                                    {
                                        "lat": 48.858296,
                                        "lon": 2.294479,
                                        "primary": "",
                                        "globe": "earth"
                                    }
                                ],
                                "thumbnail": {
                                    "source": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Tour_Eiffel_Wikimedia_Commons.jpg/78px-Tour_Eiffel_Wikimedia_Commons.jpg",
                                    "width": 78,
                                    "height": 144
                                },
                                "pageimage": "Tour_Eiffel_Wikimedia_Commons.jpg",
                                "extract": "La tour Eiffel  est une tour de fer puddl\u00e9 de 324 m\u00e8tres de hauteur ",
                                "contentmodel": "wikitext",
                                "pagelanguage": "fr",
                                "pagelanguagehtmlcode": "fr",
                                "pagelanguagedir": "ltr",
                                "touched": "2020-01-05T20:19:17Z",
                                "lastrevid": 166075414,
                                "length": 128888,
                                "fullurl": "https://fr.wikipedia.org/wiki/Tour_Eiffel",
                                "editurl": "https://fr.wikipedia.org/w/index.php?title=Tour_Eiffel&action=edit",
                                "canonicalurl": "https://fr.wikipedia.org/wiki/Tour_Eiffel"
                            }}}}

    class MockRequestsGet:
        def __init__(self, url, params):
            pass
        def json(self):
            return FAKE_API_RESULT

    monkeypatch.setattr('requests.Session.get', MockRequestsGet)
    pars = localisation()
    result = pars.wiki_api([48.85824, 2.2945])
    assert result[0]["title"] == "Tour Eiffel"
    assert result[0]["abstract"] == "La tour Eiffel  est une tour de fer puddl\u00e9 de 324 m\u00e8tres de hauteur "
    assert result[0]["articleUrl"] == "https://fr.wikipedia.org/wiki/Tour_Eiffel"

def test_map_api(monkeypatch):
    FAKE_API_RESULT= {"results": {
        "items": [
            {
                "position": [
                    48.85824,
                    2.2945
                ],
                "distance": 5808,
                "title": "Eiffel Tower",
                "averageRating": 0.0,
                "icon": "https://download.vcdn.cit.data.here.com/p/d/places2_stg/icons/categories/38.icon",
                "vicinity": "5 Avenue Anatole France<br/>75007 Paris",
            }
        ]}
}
    class MockRequestsGet:

        def __init__(self, url, params):
            pass
        def json(self):
            return FAKE_API_RESULT

    monkeypatch.setattr('requests.Session.get', MockRequestsGet)
    pars = localisation ()
    geoloc, address = pars.map_api("Tour Eiffel", "48.8482,2.3724;r=245799")
    assert geoloc  == ['48.85824', '2.2945']
    assert address  == "5 Avenue Anatole France 75007 Paris"
