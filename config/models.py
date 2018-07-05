from django.db import models  


class Ticker(models.Model):
	coin_id = models.IntegerField();
	name = models.CharField(max_length=100);
	symbol = models.CharField(max_length=100);
	website_slug = models.CharField(max_length=100);

class Coin_Data(models.Model):
	coin_id = models.IntegerField(default=None, blank=True, null=True);
	name = models.CharField(max_length=100, default=None, blank=True, null=True);
	symbol = models.CharField(max_length=100, default=None, blank=True, null=True);
	website_slug = models.CharField(max_length=100, default=None, blank=True, null=True);
	rank = models.IntegerField(default=None, blank=True, null=True);
	circulating_supply = models.FloatField(default=None, blank=True, null=True);
	total_supply = models.FloatField(default=None, blank=True, null=True);
	max_supply = models.FloatField(default=None, blank=True, null=True);
	price = models.FloatField(default=None, blank=True, null=True);
	volume_24h = models.FloatField(default=None, blank=True, null=True);
	market_cap = models.FloatField(default=None, blank=True, null=True);
	percent_change_1h = models.FloatField(default=None, blank=True, null=True);
	percent_change_24h = models.FloatField(default=None, blank=True, null=True);
	percent_change_7d = models.FloatField(default=None, blank=True, null=True);
	last_updated = models.IntegerField(default=None, blank=True, null=True);

	