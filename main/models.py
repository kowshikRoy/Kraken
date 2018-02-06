from django.db import models

# Create your models here.
class Region(models.Model):
	name 		= models.CharField(max_length = 120)
	def __str__(self):
		return self.name


class Product(models.Model):
	name 		= models.CharField(max_length = 120)
	def __str__(self):
		return self.name


class Client(models.Model):
	name 		= models.CharField(max_length = 120, blank = False, null = False)
	region		= models.ForeignKey(Region, on_delete = models.CASCADE)
	def __str__(self):
		return self.name


class SalesMan(models.Model):
	name		= models.CharField(max_length = 120)
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
	seller		= models.ForeignKey(SalesMan, on_delete = models.CASCADE, null = True)
	product 	= models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
	voucher 	= models.ForeignKey(Voucher ,on_delete = models.CASCADE, null= True)
	volume		= models.IntegerField(default = 0)
	amount		= models.IntegerField(default = 0)
	def __str__(self):
		return  str(self.voucher) + " Volume-" + str(self.volume) + " Amount-" + str(self.amount)