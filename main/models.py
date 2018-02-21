from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
class Company(models.Model):
	name 		= models.CharField(max_length = 100)
	description = models.CharField(max_length = 1000)
	created_at	= models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.name

class Profile(models.Model):
	user 		= models.OneToOneField(User)
	company 	= models.ForeignKey(Company, on_delete= models.CASCADE, null= True)
	is_admin	= models.BooleanField(default = True)

	def __str__(self):
		return self.user.username


class Region(models.Model):
	name 		= models.CharField(max_length = 120)
	latitude	= models.DecimalField(max_digits=9, decimal_places=6)
	longitude	= models.DecimalField(max_digits=9, decimal_places=6)
	def __str__(self):
		return self.name


class Product(models.Model):
	name 		= models.CharField(max_length = 120)
	company 	= models.ForeignKey(Company, on_delete= models.CASCADE, null= True)
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('product', kwargs= {'id': self.id})


class SalesMan(models.Model):
	name		= models.CharField(max_length = 120)
	company 	= models.ForeignKey(Company, on_delete= models.CASCADE, null= True)
	def __str__(self):
		return self.name


class Client(models.Model):
	name 		= models.CharField(max_length = 120, blank = False, null = False)
	company 	= models.ForeignKey(Company, on_delete= models.CASCADE, null= True)
	region		= models.ForeignKey(Region, on_delete = models.CASCADE)
	salesman 	= models.ForeignKey(SalesMan, on_delete = models.CASCADE)
	def __str__(self):
		return self.name




class Voucher(models.Model):
	voucher_no	= models.CharField(max_length = 20)
	client 		= models.ForeignKey(Client, on_delete = models.CASCADE)
	date		= models.DateField()
	def __str__(self):
		return self.voucher_no + " " + str(self.date)


class Transaction(models.Model):
	T_TYPE 		= (
            ('Primary', 'Primary'),
            ('Secondary', 'Secondary')
        )
	t_type	 	= models.CharField(max_length = 20, choices = T_TYPE, default="Primary")
	product 	= models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
	voucher 	= models.ForeignKey(Voucher ,on_delete = models.CASCADE, null= True)
	volume		= models.IntegerField(default = 0)
	amount		= models.IntegerField(default = 0)
	def __str__(self):
		return  str(self.voucher) + " Volume-" + str(self.volume) + " Amount-" + str(self.amount)
