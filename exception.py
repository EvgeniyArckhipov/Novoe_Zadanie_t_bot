import requests
import json
from config import val

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException('Нельзя перевести валюту в валюту')
        try:
            base or quote not in val.keys()
        except KeyError:
            raise APIException('Неизвестная валюта')
        try:
            amount == float(amount)
        except ValueError:
            raise APIException('Введите число')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}')
        otvet = json.loads(r.content)
        con = otvet[quote] * float(amount)
        return con