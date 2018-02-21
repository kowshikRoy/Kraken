from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Region(models.Model):
	name 		= models.CharField(max_length = 120)
	latitude	= models.DecimalField(max_digits=9, decimal_places=6, default = 23.777176)
	longitude	= models.DecimalField(max_digits=9, decimal_places=6, default = 90.399452)
	def __str__(self):
		return self.name


class Product(models.Model):
	name 		= models.CharField(max_length = 120)
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('product', kwargs= {'id': self.id})


class SalesMan(models.Model):
	name		= models.CharField(max_length = 120)
	def __str__(self):
		return self.name


class Client(models.Model):
	name 		= models.CharField(max_length = 120, blank = False, null = False)
	region		= models.ForeignKey(Region, on_delete = models.CASCADE)
	salesman 	= models.ForeignKey(SalesMan, on_delete = models.CASCADE)
	def __str__(self):
		return self.name



class Voucher(models.Model):
	voucher_no	= models.CharField(max_length = 20)
	client 		= models.ForeignKey(Client, on_delete = models.CASCADE, null= True)
	date		= models.DateField()
	def __str__(self):
		return self.voucher_no + " " + str(self.date)


class Transaction(models.Model):
	T_TYPE 		= (
            ('PRIMARY', 'PRIMARY'),
            ('DISCOUNT', 'DISCOUNT'),
            ('RETURN', 'RETURN'),
            ('PURCHASE', 'PURCHASE'),

        )
	t_type	 	= models.CharField(max_length = 20, choices = T_TYPE, default="PRIMARY")
	product 	= models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
	voucher 	= models.ForeignKey(Voucher ,on_delete = models.CASCADE, null= True)
	volume		= models.FloatField(default = 0)
	amount		= models.FloatField(default = 0)
	def __str__(self):
		return  str(self.voucher) + " Volume-" + str(self.volume) + " Amount-" + str(self.amount)
