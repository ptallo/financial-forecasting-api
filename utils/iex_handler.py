import requests


class IEXHandler:
    def __init__(self):
        self.base_url = "https://sandbox.iexapis.com"
        self.api_key = "Tsk_942768a24d244db38c7a44e32e3bc000"
        self.stock_tickers = []
        self.populate_info()

    def get_historical_data(self, ticker, drange="3m"):
        request_url = "{}/stable/stock/{}/chart/{}?token={}".format(
            self.base_url,
            ticker,
            drange,
            self.api_key
        )
        response = requests.get(request_url)
        if response.ok:
            return response.json()
        raise Exception("Bad response from get historical data code: {} reason: {}".format(response.status_code, response.text))

    def populate_info(self):
        if not self.stock_tickers:
            request_url = "{}/stable/ref-data/symbols?token={}".format(
                self.base_url,
                self.api_key
            )

            response = requests.get(request_url)

            if response.ok:
                for data in response.json():
                    self.stock_tickers.append((data["symbol"], data["name"]))
                return

            raise Exception("Bad response from populate stock info data code: {} reason: {}".format(response.status_code, response.text))

