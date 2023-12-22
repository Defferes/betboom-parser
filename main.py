import requests
from loguru import logger

logger.add("logs/parser.log")

class Parser:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-site',
            'Host': 'api-bifrost.oddin.gg',
            'Accept-Language': 'ru',
            'Sec-Fetch-Mode': 'cors',
            'Origin': 'https://bifrost.oddin.gg',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/17.2.1 Safari/605.1.15',
            'Referer': 'https://bifrost.oddin.gg/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'x-locale': 'RU',
            'x-display-resolution': '1905x420',
            'x-api-key': 'b94ac61d-b060-4892-8242-923bf2303a38',
            'x-sbi': '58935287-9304-4d18-a806-ed3d6e90c4dd',
        }
        self.match_ids = self._get_match_ids()

    def get_coefficients(self):
        for match_id in self.match_ids:
            json_data = {
                'operationName': 'match',
                'variables': {
                    'matchId': match_id,
                    'historic': False,
                },
                'extensions': {
                    'persistedQuery': {
                        'version': 1,
                        'sha256Hash': '51213b9a296319a4733927bf8a953c897358be9c5522749b264f44f01798a9f4',
                    },
                },
            }

            response = requests.post('https://api-bifrost.oddin.gg/main/bifrost/query',
                                     headers=self.headers,
                                     json=json_data)
            if response.json()["data"]["match"]["state"] == "STARTED":
                logger.info(f"[LIVE] {response.json()}")
            else:
                logger.info(f"[NOT STARTED] {response.json()}")

    def _get_match_ids(self):
        """
        local method for request info about current matches(match_ids... etc.)
        :return: [match_id_1: int, match_id_2: int]
        """
        json_data = {
            'operationName': 'allMatch',
            'variables': {
                'first': 20,
                'liveOnly': False,
                'historic': False,
                'sports': [
                    'c3BvcnQvb2Q6c3BvcnQ6Mw==',
                ],
            },
            'extensions': {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': 'a0aa26ffe006bc1c6ab169f0b6d5b2780c094ea92ac78bb58728b97b54001280',
                },
            },
        }

        response = requests.post('https://api-bifrost.oddin.gg/main/bifrost/query',
                                 headers=self.headers,
                                 json=json_data)
        # TODO: return others information or/and sending in db
        return [match["node"]["id"] for match in response.json()["data"]["allMatch"]["edges"]]


if __name__ == "__main__":
    pr = Parser()
    pr.get_coefficients()
