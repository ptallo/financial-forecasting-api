import requests


class IEXHandler:
    def __init__(self):
        self.base_url = "https://sandbox.iexapis.com"
        self.api_key = "Tsk_942768a24d244db38c7a44e32e3bc000"

    def get_historical_data(self, ticker, date_range):
        if date_range not in ["1y", "6m", "3m", "1m"]:
            date_range = "1m"

        request_url = "{}/stable/stock/{}/chart/{}?token={}".format(
            self.base_url,
            ticker,
            date_range,
            self.api_key
        )
        
        response = requests.get(request_url)
        if response.ok:
            return 200, response.json()
        return response.status_code, response.text

    def get_valid_stock_tickers(self):
        request_url = "{}/stable/ref-data/symbols?token={}".format(
            self.base_url,
            self.api_key
        )

        response = requests.get(request_url)

        stock_info = []
        if response.ok:
            for data in response.json():
                stock_info.append((data["symbol"], data["name"]))
            return 200, stock_info
        else:
            return response.status_code, response.text

