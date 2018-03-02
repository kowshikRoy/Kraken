from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Region(models.Model):
	name 		= models.CharField(max_length = 120)
	latitude	= models.DecimalField(max_digits=9, decimal_places=6, default = 23.777176)
	longitude	= models.DecimalField(max_digits=9, decimal_places=6, default = 90.399452)
	volume		= models.FloatField(default = 0)
	amount 		= models.FloatField(default = 0)
	def __str__(self):
		return self.name


class Product(models.Model):
	name 		= models.CharField(max_length = 120, unique = True)
	volume		= models.FloatField(default = 0)
	amount 		= models.FloatField(default = 0)
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('product', kwargs= {'id': self.id})


class SalesMan(models.Model):
	name		= models.CharField(max_length = 120)
	volume		= models.FloatField(default = 0)
	amount 		= models.FloatField(default = 0)
	def __str__(self):
		return self.name


class Client(models.Model):
	name 		= models.CharField(max_length = 50, unique = True)
	region		= models.ForeignKey(Region, on_delete = models.CASCADE, related_name= "clients")
	salesman 	= models.ForeignKey(SalesMan, on_delete = models.CASCADE, related_name= "clients")
	volume		= models.FloatField(default = 0)
	amount 		= models.FloatField(default = 0)
	def __str__(self):
		return self.name




class Transaction(models.Model):
	T_TYPE 		= (
            ('PRIMARY', 'PRIMARY'),
            ('DISCOUNT', 'DISCOUNT'),
            ('RETURN', 'RETURN'),
            ('PURCHASE', 'PURCHASE'),

        )
	t_type	 	= models.CharField(max_length = 20, choices = T_TYPE, default="PRIMARY")
	product 	= models.ForeignKey(Product, on_delete = models.CASCADE, null = True, related_name ="transactions")
	client 		= models.ForeignKey(Client, on_delete = models.CASCADE, related_name = "transactions")
	date 		= models.DateField()
	volume		= models.FloatField(default = 0)
	amount		= models.FloatField(default = 0)
	
	def __str__(self):
		return  str(self.t_type) + " " + str(self.date) + " " + str(self.client) + " " + str(self. product)


class PercentileInfo(models.Model):
	T_TYPE 		= (
            ('PRODUCT', 'PRODUCT'),
            ('CLIENT', 'CLIENT'),
            ('REGION', 'REGION'),
            ('SALESMAN', 'SALESMAN'),

        )
	p_type	 	= models.CharField(max_length = 20, choices = T_TYPE, default="PRIMARY")
	number		= models.IntegerField(default = 0)
	amount		= models.IntegerField(default = 0)

	def __str__(self):
		return str(self.number) + " " + self.p_type + "= " + str(self.amount)
	