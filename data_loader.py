import datetime
import sys
import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE','myproject.settings')

import django
django.setup()

import time
from datetime import date
from django.contrib.auth.models import User
from main.models import Region, Client,Product,SalesMan,Transaction
usernames = ['John', 'Zubaer', 'Repon']
region_names = ['Dhaka','Chittagong', 'Khulna', 'Rajshahi','Barisal','Sylhet','Rangpur','Commilla']
person_name = ['Ahnaf', 'Shamim', 'Sabbir','Rafi', 'Anik', 'Fardin','Sumon','Rubel','Mahir','Saiful']


for i in range(len(usernames)):
    username    = usernames[i]
    user        = User.objects.get_or_create(username= username)[0]
    user.set_password('123456789zr')
    user.save()

for i in range(len(person_name)):
    name        = person_name[i]
    salesman    = SalesMan.objects.get_or_create(name = name)[0]


for i in range(len(region_names)):
    inp         = region_names[i]
    region      = Region.objects.get_or_create(name = inp)[0]

user = User.objects.get(username = 'John') #User Account
salesmans = SalesMan.objects.all()
regions = Region.objects.all()
Client.objects.all().delete()
Product.objects.all().delete()
Transaction.objects.all().delete()


dic= {}
ProductDic = {}
VoucherDic = {}

clients = list()
vouchers = list()
products = list()
transactions = list()
def check(s):
    if(s==''): return '0'
    return s 

import datetime
import os
from os import listdir
from os.path import isfile, join

import xlrd

# constants
DATA_LOCATION = os.path.join(os.getcwd(), 'data')

SALES_FILE_LOCATION = os.path.join(DATA_LOCATION, 'sales')
SALES_SHEET_NAME = 'Sales Contact Lens Credit'

SALES_COLUMN_IDX_FOR_INVOICE = 3
SALES_COLUMN_IDX_FOR_DATE = 0
SALES_COLUMN_IDX_FOR_CLIENT_NAME = 2
SALES_COLUMN_IDX_FOR_VOUCHER_NO = 4
SALES_COLUMN_IDX_FOR_PRODUCT_NAME = 0
SALES_COLUMN_IDX_FOR_PRODUCT_AMOUNT = 1
SALES_COLUMN_IDX_FOR_PRODUCT_TOTAL_PRICE = 3

DISCOUNT_FILE_LOCATION = os.path.join(DATA_LOCATION, 'discount')
DISCOUNT_SHEET_IDX = 0
DISCOUNT_COLUMN_IDX_FOR_DATE = 0
DISCOUNT_COLUMN_IDX_FOR_CLIENT_NAME = 2
DISCOUNT_COLUMN_IDX_FOR_VOUCHER_NO = 4
DISCOUNT_COLUMN_IDX_FOR_AMOUNT = 5

RETURN_FILE_LOCATION = os.path.join(DATA_LOCATION, 'return')
RETURN_SHEET_IDX = 0
RETURN_COLUMN_IDX_FOR_DATE = 0
RETURN_COLUMN_IDX_FOR_CLIENT_NAME = 2
RETURN_COLUMN_IDX_FOR_VOUCHER_NO = 4
RETURN_COLUMN_IDX_FOR_AMOUNT = 5

# read sales data
sales_files = [f for f in listdir(SALES_FILE_LOCATION) if isfile(join(SALES_FILE_LOCATION, f))]

for sales_file in sales_files:
    file_location = os.path.join(SALES_FILE_LOCATION, sales_file)
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_name(SALES_SHEET_NAME)
    startRow = 0
    voucherId = -1
    clientId = -1

    client      = None
    date        = None

    while True:
        if sheet.cell_value(startRow, SALES_COLUMN_IDX_FOR_INVOICE) == 'Invoice':
            break
        startRow += 1

    for rowIdx in range(startRow, sheet.nrows):
        if sheet.cell_value(rowIdx, 0) == '':
            break


        if sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_INVOICE) == 'Invoice':
            # clientId = save_client_or_return_client_id_if_exists(
            #                           sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_CLIENT_NAME))
            # provide random salesmanId and locationId

            name = sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_CLIENT_NAME)
            if(name in dic) :
                client = dic[name]
            else :
                client =  Client(
                name = sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_CLIENT_NAME),
                region = random.choice(regions),
                salesman = random.choice(salesmans),)
                dic[name] = client
                clients.append(client)


            time_tuple = xlrd.xldate_as_tuple(sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_DATE), 0)
            date = datetime.datetime(*time_tuple)
            # voucherId = save_voucher(
            #                           sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_VOUCHER_NO),
            #                           clientId, date)
            
        else:
            # assert that clientId and voucherId >= 0
            # productId = save_product_or_return_product_id_if_exists(
            #                           sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_NAME))
            # save_transaction ('PURCHASE', voucherId, productId,
            #                           sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_AMOUNT)
            #                           sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_TOTAL_PRICE))

            name = sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_NAME)
            if name in ProductDic:
                product = ProductDic[name]
            else:
                product = Product(
                    name = sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_NAME),
                )
                ProductDic[name] = product
                products.append(product)

            # #print(sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_TOTAL_PRICE))

            transaction = Transaction(
                t_type  = 'PURCHASE',
                product = product,
                client  = client,
                date    = date,
                volume  = check(sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_AMOUNT)),
                amount  = check(sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_TOTAL_PRICE)),

                )
            transactions.append(transaction)
            
        rowIdx += 1

print("Ended Sales ")



# read discount data
discount_files = [f for f in listdir(DISCOUNT_FILE_LOCATION) if isfile(join(DISCOUNT_FILE_LOCATION, f))]

for discount_file in discount_files:
    file_location = os.path.join(DISCOUNT_FILE_LOCATION, discount_file)
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(DISCOUNT_SHEET_IDX)
    rowIdx = 0
    voucher     = None
    client      = None
    date        = None

    while True:
        if sheet.cell_type(rowIdx, DISCOUNT_COLUMN_IDX_FOR_DATE) == xlrd.XL_CELL_DATE:
            break
        rowIdx += 1

    while True:
        if sheet.cell_type(rowIdx, DISCOUNT_COLUMN_IDX_FOR_DATE) != xlrd.XL_CELL_DATE:
            break

        # clientId = save_client_or_return_client_id_if_exists(
        #                           sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_CLIENT_NAME))
        # provide random salesmanId and locationId

        name = sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_CLIENT_NAME)
        if name in dic :
            client = dic[name]
        else :
            client = Client(
                name = sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_CLIENT_NAME),
                region = random.choice(regions),
                salesman = random.choice(salesmans),
            )
            clients.append(client)
            dic[name] = client


        time_tuple = xlrd.xldate_as_tuple(sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_DATE), 0)
        date = datetime.datetime(*time_tuple)
        print(date)
        # voucherId = save_voucher(
        #                           sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_VOUCHER_NO),
        #                           clientId, date)
        # save_transaction ('DISCOUNT', voucherId, null,
        #                           null,
        #                           sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_AMOUNT))
       
        
        transaction = Transaction(
                t_type  = 'DISCOUNT',
                product = None,
                client  = client,
                date    = date,
                volume  = 0,
                amount  = check(sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_AMOUNT)),

                )
        transactions.append(transaction)
            

        rowIdx += 1
print("Ended DISCOUNT ")





# read return data
return_files = [f for f in listdir(RETURN_FILE_LOCATION) if isfile(join(RETURN_FILE_LOCATION, f))]

for return_file in return_files:
    file_location = os.path.join(RETURN_FILE_LOCATION, return_file)
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(RETURN_SHEET_IDX)
    rowIdx = 0


    
    client      = None
    date        = None
    while True:
        if sheet.cell_type(rowIdx, RETURN_COLUMN_IDX_FOR_DATE) == xlrd.XL_CELL_DATE:
            break
        rowIdx += 1

    while True:
        if sheet.cell_type(rowIdx, RETURN_COLUMN_IDX_FOR_DATE) != xlrd.XL_CELL_DATE or rowIdx > 5:
            break
        # clientId = save_client_or_return_client_id_if_exists(
        #                           sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_CLIENT_NAME))
        # provide random salesmanId and locationId

        name = sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_CLIENT_NAME)
        if name in dic : 
            client = dic[name]
        else: 
            client = Client(
                name = sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_CLIENT_NAME),
                region = random.choice(regions),
                salesman = random.choice(salesmans),
            )
            clients.append(client)
            dic[name] = client

        time_tuple = xlrd.xldate_as_tuple(sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_DATE), 0)
        date = datetime.datetime(*time_tuple)
        print(date)
        # voucherId = save_voucher(
        #                           sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_VOUCHER_NO),
        #                           clientId, date)
        # save_transaction ('RETURN', voucherId, null,
        #                           null,
        #                           sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_AMOUNT))

        
        
        transaction = Transaction(
                t_type = 'RETURN',
                product = None,
                client = client,
                date    =date,
                volume = 0,
                amount = check(sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_AMOUNT)),

                )
        
        transactions.append(transaction)

        rowIdx += 1

print("END")


Client.objects.bulk_create(clients)
Product.objects.bulk_create(products)
Dict_Client = {}
Dict_Product= {}
for x in Client.objects.all():
    Dict_Client[x.name] = x

for x in Product.objects.all():
    Dict_Product[x.name] = x;

for x in transactions:
    if(x is None):
        continue
    if x.product != None:
        x.product = Dict_Product[x.product.name]
    x.client = Dict_Client[x.client.name]
   
    # if x.product != None:
    #     x.product = Dict_Product[x.product.name]
    # x.client = Dict_Client[x.client.name]

print("Key Resolved")
Transaction.objects.bulk_create(transactions)
print("ALl END")