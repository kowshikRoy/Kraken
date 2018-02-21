import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
				'myproject.settings')

import django
django.setup()

import time
from datetime import date

from django.contrib.auth.models import User
from main.models import Region, Client,Product,SalesMan,Voucher,Transaction
import random
import string
usernames = ['John', 'Zubaer', 'Repon']
region_names = ['Dhaka','Chittagong', 'Khulna', 'Rajshahi','Barisal','Sylhet','Rangpur','Commilla']
person_name = ['Ahnaf', 'Shamim', 'Sabbir','Rafi', 'Anik', 'Fardin','Sumon','Rubel','Mahir','Saiful']

def randomStr(lim = 10):
	N = random.randint(3,lim)
	return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))


def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y-%m-%d', prop)


def populate():
	#User
	for i in range(len(usernames)):
		username	= usernames[i]
		user 		= User.objects.get_or_create(username= username)[0]
		user.set_password('123456789zr')
		user.save()
	users = User.objects.all()

	#Region Populate
	Region.objects.all().delete()
	for i in range(len(region_names)):
		inp 		= region_names[i]
		region 		= Region.objects.get_or_create(name = inp)[0]
		
		print("{0} - {1}".format(region.id, inp))

	regions = Region.objects.all()

	return



	# #Product Populate
	# Product.objects.all().delete()
	# for i in range(20):
	# 	inp = randomStr()
	# 	company= companies[i % len(companies)]
	# 	product = Product.objects.get_or_create(name = inp, company = company)[0]
	# 	print("{0} - {1}".format(product.id, product.name))

	# products = Product.objects.all()



	# # Client Populate
	# Client.objects.all().delete()
	# for i in range(20):
	# 	name = randomStr(20)
	# 	region = random.choice(regions)
	# 	company= companies[i % len(companies)]
	# 	client =  Client.objects.get_or_create(name = name, company = company, region = region)[0]
	# 	print("{0} - {1}".format( client.id, client.name, client.region.name))


	# clients = Client.objects.all()

	# # SalesMan.objects.all().delete()
	# for i in range(10):
	# 	inp = randomStr()
	# 	company= companies[i % len(companies)]
	# 	salesMan = SalesMan.objects.get_or_create(name = inp, company = company)[0]
	# 	print("{0} - {1}".format(salesMan.id, salesMan.name))

	# sellers	= SalesMan.objects.all()


	# #Voucher Populate
	# Voucher.objects.all().delete()
	# today  = date.today()
	# for i in range(80):
	# 	inp 	= randomStr(10)
	# 	client 	= random.choice(clients)
	# 	company= companies[i % len(companies)]
	# 	dates 	= randomDate("2017-01-01", today.strftime('%Y-%m-%d'), random.random())
	# 	voucher = Voucher.objects.get_or_create(voucher_no = inp, client = client, date = dates)


	# vouchers = Voucher.objects.all()

	# Transaction.objects.all().delete()
	# for i in range(200):
	# 	voucher 	= random.choice(vouchers)
	# 	seller 		= random.choice(sellers.filter(company = voucher.client.company))
	# 	product 	= random.choice(products.filter(company = voucher.client.company))
	# 	volume		= random.randint(1,10)
	# 	amount		= random.randint(0,1000)
	# 	trans 		= Transaction.objects.get_or_create(seller= seller, voucher = voucher, product = product,
	# 		volume=volume, amount = amount)
	# 	print(i)


# Start execution here!
if __name__ == '__main__':
	print("Starting myproject population script...")
	populate()
