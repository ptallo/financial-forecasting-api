import requests


class IEXHandler:
    def __init__(self):
        self.base_url = "https://sandbox.iexapis.com"
        self.api_key = "Tsk_942768a24d244db38c7a44e32e3bc000"

    def get_historical_data(self, ticker, drange="3m"):
        request_url = "{}/stable/stock/{}/chart/{}?token={}".format(
            self.base_url,
            ticker,
            drange,
            self.api_key
        )
        response = requests.get(request_url)
        return response.json()