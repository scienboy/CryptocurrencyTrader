from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import csv

class CoinmarketcapAPI():
    def __init__(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '5000',
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'a4af3c31-d0fc-4ceb-8b1c-89c6479e230a',
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)

            # status = data['status']
            # data_list = data['data']
            # for data_val in data_list:
            #     try:
            #         with open('.\\data\\CoinMarketCap\\mycsvfile_2105062227.csv', 'a') as csvfile:
            #             writer = csv.DictWriter(csvfile, fieldnames=data_val.keys())
            #             writer.writeheader()
            #             for data in data_val:
            #                 writer.writerow(data)
            #     except IOError:
            #         print("I/O error")
            #
            #
            # try:
            #     with open('.\\data\\CoinMarketCap\\mycsvfile_2105062227.csv', 'w') as csvfile:
            #         writer = csv.DictWriter(csvfile, fieldnames=data.data.keys())
            #         writer.writeheader()
            #         for data in data.data:
            #             writer.writerow(data.data)
            # except IOError:
            #     print("I/O error")


            print(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        pass


