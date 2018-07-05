import json
import requests
from django.http import JsonResponse
from .models import Coin_Data
import threading
from rest_framework.authtoken.models import Token

'''
retrieves the block information
'''
supported_coins = ["BTC", "LTC", "DASH" , "DOGE"];
version = "1"


def get_config(request):
	#Async start
	response = {
				"supported_coins": supported_coins,
				"version": version,
				'price_in_usd': {}
				}

	for coin in supported_coins:				
		if Coin_Data.objects.filter(symbol=coin):
			response['price_in_usd'][coin] = Coin_Data.objects.get(symbol=coin).price
		
	print(response)
	t = threading.Thread(target=storeTickerListingData, args=(), kwargs={})
	t.setDaemon(True)
	t.start()
	return JsonResponse(response, status=200)

'''
    id = models.IntegerField();
	name = models.CharField(max_length=100);
	symbol = models.CharField(max_length=100);
	website_slug = models.CharField(max_length=100);
	rank = models.IntegerField();
	circulating_supply = models.FloatField();
	total_supply = models.FloatField();
	max_supply = models.FloatField();
	last_updated = models.IntegerField();
	price: models.FloatField();
	volume_24h: models.FloatField();
	market_cap: models.FloatField();
	percent_change_1h: models.FloatField();
	percent_change_24h: models.FloatField();
	percent_change_7d: models.FloatField();
'''

'''
{'1': {'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'website_slug': 'bitcoin', 'rank': 1,
 'circulating_supply': 17063587.0, 'total_supply': 17063587.0, 'max_supply': 21000000.0,
  'quotes': 


  {

  'USD': {'price': 7502.66, 'volume_24h': 5616880000.0, 'market_cap': 128022291641.0, 
  'percent_change_1h': 0.18, 'percent_change_24h': 4.02, 'percent_change_7d': -5.07}

  }, 
  'last_updated': 1527675874},

   '1027':

    {'id': 1027, 'name': 'Ethereum', 'symbol': 'ETH', 
  'website_slug': 'ethereum', 'rank': 2, 'circulating_supply': 99757307.0, 'total_supply': 99757307.0, 
  'max_supply': None, 'quotes': {'USD': {'price': 568.957, 'volume_24h': 2373550000.0, 'market_cap': 56757618172.0, 
  'percent_change_1h': 0.93, 'percent_change_24h': 7.14, 'percent_change_7d': -9.27}}, 'last_updated': 1527675858}}
'''

def storeTickerListingData():
	# response_data = json.dumps(response_data)
	# ticker_listing = requests.get('https://api.coinmarketcap.com/v2/listings/')
	ticker_usd = requests.get('https://api.coinmarketcap.com/v2/ticker/?convert=USD')
	# ticker_listing_data = ticker_listing.json()
	response_data = ticker_usd.json()
	data = response_data['data']
	for key, value in data.items():
		# print(key)
		# print(value)
		coin = Coin_Data(
						coin_id = value['id'],
						name = value['name'],
						symbol = value['symbol'],
						website_slug = value['website_slug'],
						rank = value['rank'],
						circulating_supply = value['circulating_supply'],
						total_supply = value['total_supply'],
						max_supply = value['max_supply'],
						last_updated = value['last_updated'],
						price = value['quotes']['USD']['price'],
						volume_24h = value['quotes']['USD']['volume_24h'],
						market_cap = value['quotes']['USD']['market_cap'],
						percent_change_1h = value['quotes']['USD']['percent_change_1h'],
						percent_change_24h = value['quotes']['USD']['percent_change_24h'],
						percent_change_7d = value['quotes']['USD']['percent_change_7d']
						)

		json_coin = { "coin_id" :value['id'],
						"name" : value['name'],
						"symbol" : value['symbol'],
						"website_slug" : value['website_slug'],
						"rank" : value['rank'],
						"circulating_supply" : value['circulating_supply'],
						"total_supply" : value['total_supply'],
						"max_supply" : value['max_supply'],
						"last_updated" : value['last_updated'],
						"price" : value['quotes']['USD']['price'],
						"volume_24h" : value['quotes']['USD']['volume_24h'],
						"market_cap" : value['quotes']['USD']['market_cap'],
						"percent_change_1h" : value['quotes']['USD']['percent_change_1h'],
						"percent_change_24h" : value['quotes']['USD']['percent_change_24h'],
						"percent_change_7d" : value['quotes']['USD']['percent_change_7d']
						}

		count = Coin_Data.objects.filter(symbol=value['symbol']).count()	
		# print(">>>>>"+str(count))
		if(Coin_Data.objects.filter(symbol=value['symbol']).exists() is False):
			# print(">>>>>")
			coin.save()
		else:
			# print(Coin_Data.objects.filter(symbol=value['symbol']).exists() )
			Coin_Data.objects.filter(symbol=value['symbol']).update(rank = value['rank'],
																	circulating_supply = value['circulating_supply'],
																	total_supply = value['total_supply'],
																	last_updated = value['last_updated'],
																	price = value['quotes']['USD']['price'],
																	volume_24h = value['quotes']['USD']['volume_24h'],
																	market_cap = value['quotes']['USD']['market_cap'],
																	percent_change_1h = value['quotes']['USD']['percent_change_1h'],
																	percent_change_24h = value['quotes']['USD']['percent_change_24h'],
																	percent_change_7d = value['quotes']['USD']['percent_change_7d']
																	);

		# Coin_Data.objects.filter(symbol=value['symbol']).update(coin)





